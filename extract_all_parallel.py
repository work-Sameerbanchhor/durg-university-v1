import os
import json
import glob
import time
import random
import shutil
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

# Load environment variables
load_dotenv()

# Parse API keys from .env
keys_str = os.environ.get("GEMINI_API_KEYS", "")
if keys_str:
    API_KEYS = [k.strip() for k in keys_str.split(",") if k.strip()]
else:
    # Fallback to single key if multiple keys not found
    single_key = os.environ.get("GEMINI_API_KEY", "")
    API_KEYS = [single_key] if single_key else []

if not API_KEYS:
    print("[Error] No Gemini API keys found in .env. Please set GEMINI_API_KEYS or GEMINI_API_KEY.")
    exit(1)

print(f"Loaded {len(API_KEYS)} API keys for rotation.")

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[Error] google-genai is not installed.")
    exit(1)

# Pydantic schema for structured output
class CourseRollNumbers(BaseModel):
    course_name: str = Field(
        description="Full name of the course or exam (e.g. 'B.C.A. Part-I', 'M.Sc. Mathematics 1st Semester')"
    )
    roll_numbers: List[str] = Field(
        description="List of roll numbers belonging to this course found in the document"
    )

class ExtractionResult(BaseModel):
    courses: List[CourseRollNumbers] = Field(
        description="Extracted courses and their corresponding lists of roll numbers"
    )

# Shared state variables and locks
results = {}
results_lock = Lock()
failed_files = []
failed_lock = Lock()

# Key manager to handle rotation and 429 cooldowns
class KeyManager:
    def __init__(self, keys):
        self.keys = keys
        self.lock = Lock()
        # Map key -> cooldown expiration timestamp (0 means active)
        self.cooldowns = {k: 0.0 for k in keys}
        
    def get_key(self):
        """Get an active key. If all keys are on cooldown, wait until the first one cools down."""
        while True:
            with self.lock:
                now = time.time()
                # Find keys not on cooldown
                active_keys = [k for k, cooldown_end in self.cooldowns.items() if now >= cooldown_end]
                
                if active_keys:
                    # Pick a key randomly to distribute request load
                    return random.choice(active_keys)
                
                # All keys are on cooldown, find the one that will finish first
                next_available = min(self.cooldowns.values())
                wait_time = next_available - now
                
            if wait_time > 0:
                print(f"[KeyManager] All keys are rate-limited. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time + 0.5)
                
    def put_on_cooldown(self, key, duration=60):
        """Put a key on cooldown for rate limit violation"""
        with self.lock:
            self.cooldowns[key] = time.time() + duration
            key_suffix = key[-6:] if len(key) > 6 else key
            print(f"[KeyManager] Key ...{key_suffix} put on cooldown for {duration} seconds.")

key_manager = KeyManager(API_KEYS)

def process_single_pdf(pdf_path, max_retries=6):
    filename = os.path.basename(pdf_path)
    model_name = "gemini-3.1-flash-lite"
    
    # Check size
    file_size = os.path.getsize(pdf_path)
    
    for attempt in range(1, max_retries + 1):
        api_key = key_manager.get_key()
        client = genai.Client(api_key=api_key)
        
        uploaded_file = None
        # Create temporary ASCII path to avoid non-ASCII encoding errors in google-genai upload
        temp_pdf_path = f"temp_upload_{uuid.uuid4().hex}.pdf"
        try:
            shutil.copy2(pdf_path, temp_pdf_path)
            # Upload PDF
            uploaded_file = client.files.upload(file=temp_pdf_path)
            
            # Clean up temp file immediately after upload starts
            try:
                os.remove(temp_pdf_path)
            except Exception:
                pass
            
            prompt = (
                "Analyze this exam result notification document. "
                "Extract every course/subject name listed in the document, and for each course, "
                "extract the list of roll numbers of students associated with it."
            )
            
            response = client.models.generate_content(
                model=model_name,
                contents=[uploaded_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExtractionResult,
                    temperature=0.1,
                ),
            )
            
            # Parse structured JSON response
            extracted_data = json.loads(response.text)
            
            # Delete remote file immediately
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass
                
            return filename, extracted_data, True
            
        except Exception as e:
            # Clean up local temp file if it still exists
            try:
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
            except Exception:
                pass
                
            # Clean up uploaded file if it was created
            if uploaded_file:
                try:
                    client.files.delete(name=uploaded_file.name)
                except Exception:
                    pass
            
            err_str = str(e)
            # Handle rate limiting (429)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                key_manager.put_on_cooldown(api_key, duration=60)
                # Random jitter backoff
                time.sleep(random.uniform(1.0, 3.0))
            else:
                # Other error (e.g., connection issue or size limits)
                print(f"[Error] PDF {filename} failed (attempt {attempt}/{max_retries}): {err_str}")
                time.sleep(random.uniform(2.0, 5.0))
                
    return filename, None, False

def main():
    pdf_dir = "downloaded_pdfs"
    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    total_files = len(pdf_files)
    
    print(f"Total PDFs found to process: {total_files}")
    
    # We can process in parallel. Since we have 10 keys, 15 concurrent threads is safe.
    max_workers = min(15, len(API_KEYS) * 2)
    print(f"Starting ThreadPoolExecutor with {max_workers} concurrent threads...")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_pdf, path): path
            for path in pdf_files
        }
        
        completed = 0
        for future in as_completed(futures):
            path = futures[future]
            filename, extracted_data, success = future.result()
            completed += 1
            
            if success:
                # Check if there are roll numbers extracted
                has_rolls = any(len(c.get("roll_numbers", [])) > 0 for c in extracted_data.get("courses", []))
                
                with results_lock:
                    results[filename] = extracted_data
                    
                print(f"[Progress] {completed}/{total_files} - {filename} successfully processed ({'found roll numbers' if has_rolls else 'empty / notice only'}).")
            else:
                with failed_lock:
                    failed_files.append(filename)
                print(f"[Progress] {completed}/{total_files} - {filename} FAILED after all retries.")
                
    # Save the output results
    output_file = "all_extracted_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    duration = time.time() - start_time
    print(f"\nExtraction complete!")
    print(f"Total successfully processed: {len(results)}")
    print(f"Failed: {len(failed_files)}")
    print(f"Time taken: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"All results saved to {output_file}")
    
    if failed_files:
        print("Failed files list:")
        for fn in failed_files:
            print(f"  - {fn}")

if __name__ == "__main__":
    main()
