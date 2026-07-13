import os
import json
import argparse
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

# Load environment variables from .env file
load_dotenv()

# Check if GEMINI_API_KEY is available
if not os.environ.get("GEMINI_API_KEY"):
    print("[Warning] GEMINI_API_KEY not found in environment or .env file.")
    print("Please set the GEMINI_API_KEY variable in your .env file.")

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[Error] google-genai is not installed. Please install it using: pip install google-genai")
    exit(1)

# Define structured schema for extraction using Pydantic
class CourseRollNumbers(BaseModel):
    course_name: str = Field(
        description="Full name of the course or exam (e.g., 'P.G.D.C.A. 1ST Semester', 'M.Sc. Mathematics 1st Semester', 'L.L.B 1st Semester')"
    )
    roll_numbers: List[str] = Field(
        description="List of roll numbers belonging to this course found in the document"
    )

class ExtractionResult(BaseModel):
    courses: List[CourseRollNumbers] = Field(
        description="Extracted courses and their corresponding lists of roll numbers"
    )

def extract_roll_numbers(pdf_path, model_name="gemini-2.5-flash"):
    print(f"Initializing Gemini Client using model: {model_name}...")
    
    # Initialize the client. It automatically picks up GEMINI_API_KEY from environment/dotenv
    client = genai.Client()
    
    print(f"Uploading PDF file to Gemini API: {pdf_path}...")
    # Upload the PDF file
    uploaded_file = client.files.upload(file=pdf_path)
    print(f"File uploaded. Remote URI: {uploaded_file.uri}")
    
    prompt = (
        "Analyze this exam result notification document. "
        "Extract every course/subject name listed in the document, and for each course, "
        "extract the list of roll numbers of students associated with it."
    )
    
    print("Sending request to Gemini for structured roll number extraction...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[uploaded_file, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractionResult,
                temperature=0.1,  # Low temperature for deterministic extraction
            ),
        )
        
        # Parse the structured JSON response
        result_json = json.loads(response.text)
        return result_json
    except Exception as e:
        print(f"[Error] Gemini API call failed: {e}")
        return None
    finally:
        # Cleanup the uploaded file from Gemini storage
        try:
            print("Cleaning up remote file from Gemini storage...")
            client.files.delete(name=uploaded_file.name)
            print("Cleanup complete.")
        except Exception as e:
            print(f"[Warning] Failed to delete remote file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract Course Roll Numbers from Durg University PDF using Gemini")
    parser.add_argument("pdf_path", help="Path to the local PDF file")
    parser.add_argument("--model", default="gemini-2.0-flash", help="Gemini model name to use (default: gemini-2.0-flash)")
    parser.add_argument("--output", help="Path to save the JSON output (default: print to stdout)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"[Error] File not found: {args.pdf_path}")
        exit(1)
        
    result = extract_roll_numbers(args.pdf_path, model_name=args.model)
    
    if result:
        formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(formatted_json)
            print(f"Successfully saved extracted data to {args.output}")
        else:
            print("\n--- Extracted Data ---")
            print(formatted_json)
            print("----------------------")
    else:
        print("Failed to extract data.")

if __name__ == "__main__":
    main()
