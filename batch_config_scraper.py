import os
import json
import re
import random
import time
import queue
import threading
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==========================================
#        MASTER CONFIGURATION
# ==========================================
MAX_WORKERS = 30                 # Default parallel workers
CONSECUTIVE_FAIL_LIMIT = 200     # Sequential failures before stopping a college scan
PROGRESS_FILE = 'scraping_progress.json'
RESULTS_DIR = 'Htmls/Results'
LINKS_FILE = 'source_code/batch_config.json'
AJAX_URL = "https://durg.ucanapply.com/get-result-details"

# Hardcoded colleges list to probe
COLLEGE_CODES = [
    '303', '304', '305', '307', '331', '332', '333', '334', '335',
    '337', '338', '339', '340', '341', '344', '352', '366', '381', '386'
]

# Course Indicator Codes for Scheme B (11/12-digit)
COURSE_INDICATORS = {
    "BCA": "013",
    "B.C.A": "013",
    "B.COM": "004",
    "BCOM": "004",
    "COMMERCE": "004",
    "B.SC": "007",
    "BSC": "007",
    "SCIENCE": "007",
    "B.A": "001",
    "BA": "001",
    "ARTS": "001",
    "M.COM": "036",
    "MCOM": "036",
    "M.A. ENGLISH": "041",
    "ENGLISH": "041",
    "M.A. ECONOMICS": "049",
    "ECONOMICS": "049",
    "M.A. GEOGRAPHY": "053",
    "GEOGRAPHY": "053",
    "M.A. HINDI": "037",
    "HINDI": "037",
    "M.A. HISTORY": "046",
    "HISTORY": "046",
    "M.A. POLITICAL": "057",
    "POLITICAL": "057",
    "M.A. SOCIOLOGY": "051",
    "SOCIOLOGY": "051",
    "PGDCA": "083",
    "DCA": "081",
    "LLB": "067",
    "L.L.B": "067",
    "BBA": "093",
    "B.ED": "097",
}

# Thread-safe locks and state
progress_lock = threading.Lock()
print_lock = threading.Lock()
progress_data = {}

# ==========================================
#        PROXY MANAGER
# ==========================================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.lock = threading.Lock()
        self.index = 0
        
    def fetch_proxies(self):
        with self.lock:
            if self.proxies:
                return
            print("[ProxyManager] Fetching proxy list from ProxyScrape...")
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all"
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    lines = [l.strip() for l in r.text.split("\n") if l.strip()]
                    random.shuffle(lines)
                    self.proxies = lines
                    print(f"[ProxyManager] Loaded {len(self.proxies)} proxies.")
            except Exception as e:
                print(f"[ProxyManager] Error fetching proxies: {e}")
                
    def get_proxy(self):
        with self.lock:
            if not self.proxies:
                return None
            p = self.proxies[self.index % len(self.proxies)]
            self.index += 1
            return {"http": f"http://{p}", "https": f"http://{p}"}

proxy_manager = ProxyManager()

# ==========================================
#        PROGRESS TRACKING
# ==========================================
def load_progress():
    global progress_data
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                progress_data = json.load(f)
        except Exception:
            progress_data = {}
    if "link_indexes" not in progress_data:
        progress_data["link_indexes"] = {}

def save_progress():
    with progress_lock:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress_data, f, indent=2)

# ==========================================
#        ROLL NUMBER GENERATION
# ==========================================
def get_course_details(desc):
    desc_upper = desc.upper()
    
    # 1. Determine level
    level = "UG"
    if any(x in desc_upper for x in ["MASTER OF", "M.A.", "M.SC", "M.COM", "PGDCA", "DCA"]):
        level = "PG"
        
    # 2. Get course folder
    course_folder = "Other"
    for key in ["BCA", "BCOM", "BSC", "BA", "LLB", "BBA", "B.ED"]:
        if key in desc_upper or (key == "BCOM" and "COMMERCE" in desc_upper) or (key == "BSC" and "SCIENCE" in desc_upper) or (key == "BA" and "ARTS" in desc_upper):
            course_folder = key
            break
            
    # 3. Determine study year / semester offset
    offset = 0
    if "FIRST YEAR" in desc_upper or "1ST YEAR" in desc_upper or "PART - I" in desc_upper or "PART-I" in desc_upper or "PART I" in desc_upper or "SEM - 1" in desc_upper or "PREVIOUS" in desc_upper:
        offset = 0
    elif "SECOND YEAR" in desc_upper or "2ND YEAR" in desc_upper or "PART - II" in desc_upper or "PART-II" in desc_upper or "PART II" in desc_upper or "SEM - 2" in desc_upper or "SEM - 3" in desc_upper or "SEM - 4" in desc_upper:
        offset = 1
    elif "FINAL YEAR" in desc_upper or "3RD YEAR" in desc_upper or "THIRD YEAR" in desc_upper or "PART - III" in desc_upper or "PART-III" in desc_upper or "PART III" in desc_upper or "PART - IV" in desc_upper or "PART-IV" in desc_upper or "PART IV" in desc_upper or "SEM - 5" in desc_upper or "SEM - 6" in desc_upper or "FINAL" in desc_upper:
        offset = 2
        
    # 4. Find Course Indicator
    indicator = "001"
    for k, v in COURSE_INDICATORS.items():
        if k in desc_upper:
            indicator = v
            break
            
    return level, course_folder, offset, indicator

def generate_rolls_to_probe(desc, year, college_code):
    level, course_folder, offset, indicator = get_course_details(desc)
    
    # Calculate approximate admission year
    admission_year = year - offset
    
    rolls = []
    # If 2024 or 2025 admission, generate 8-digit simplified roll
    if admission_year >= 2024:
        y_code = "4" if admission_year == 2024 else "5"
        for i in range(1, 10000):
            rolls.append(f"{y_code}{college_code}{i:04d}")
    else:
        # Generate 11-digit or 12-digit roll
        y_code_11 = "3" if admission_year == 2023 else ("2" if admission_year in [2021, 2022] else "9")
        y_code_12 = "23" if admission_year == 2023 else ("22" if admission_year == 2022 else "21")
        
        for i in range(1, 10000):
            rolls.append(f"{y_code_11}{college_code}{indicator}{i:04d}")
            
        # Also support 12-digit format as alternate probe for 2022/2023 PG/UG admissions
        if admission_year in [2022, 2023]:
            for i in range(1, 10000):
                rolls.append(f"{y_code_12}{college_code}{indicator}{i:04d}")
                
    return rolls, level, course_folder, admission_year

# ==========================================
#        SCRAPING SESSION INITIALIZATION
# ==========================================
def get_csrf_session(url):
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
    })
    
    # Rotate proxy until we get a valid response
    for _ in range(10):
        proxy = proxy_manager.get_proxy()
        if not proxy:
            return None, None, None
        s.proxies.update(proxy)
        try:
            r = s.get(url, timeout=12)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                token_el = soup.find('input', {'name': '_token'})
                if token_el:
                    token = token_el['value']
                    payload = {
                        'COURSECD':   soup.find('input', {'name': 'COURSECD'})['value'],
                        'SEMCODE':    soup.find('input', {'name': 'SEMCODE'})['value'],
                        'RESULTTYPE': soup.find('input', {'name': 'RESULTTYPE'})['value'],
                        'session':    soup.find('input', {'name': 'session'})['value'],
                        'tcc':        soup.find('input', {'name': 'tcc'})['value'],
                        'p1': '', 'all': ''
                    }
                    return s, payload, token
        except Exception:
            pass
    return None, None, None

# ==========================================
#        SINGLE COLLEGE SCANNER
# ==========================================
def scan_college(entry_idx, desc, year, link_url, college_code):
    rolls, level, course_folder, adm_year = generate_rolls_to_probe(desc, year, college_code)
    
    # Define output folder path
    college_dir = os.path.join(RESULTS_DIR, level, course_folder, f"Year_{year}", f"College_{college_code}")
    os.makedirs(college_dir, exist_ok=True)
    
    # Initialize CSRF session
    s, payload, token = get_csrf_session(link_url)
    if not token:
        with print_lock:
            print(f"  [Error] Session initialization failed for College {college_code} - skipping.")
        return False
        
    consecutive_fails = 0
    total_found = 0
    
    # Helper to probe a single roll number
    def check_roll(roll):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-TOKEN': token,
            'Referer': link_url,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        data = payload.copy()
        data['EXAMROLLNUMBER'] = roll
        data['_token'] = token
        
        try:
            r = s.post(AJAX_URL, data=data, headers=headers, timeout=6)
            if r.status_code == 200:
                rj = r.json()
                if 'html' in rj and len(rj['html']) > 200:
                    return roll, rj['html']
        except Exception:
            pass
        return roll, None

    # Thread pool for scanning the rolls inside this college
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # We submit roll scans in small batches to monitor the Early Stopping threshold
        chunk_size = 50
        for chunk_start in range(0, len(rolls), chunk_size):
            chunk = rolls[chunk_start:chunk_start + chunk_size]
            futures = {executor.submit(check_roll, r): r for r in chunk}
            
            # Read futures as they complete
            chunk_results = {}
            for fut in as_completed(futures):
                roll = futures[fut]
                try:
                    r_roll, html = fut.result()
                    chunk_results[r_roll] = html
                except Exception:
                    chunk_results[roll] = None
                    
            # Process chunk results sequentially to maintain the fail counter
            for roll in chunk:
                html = chunk_results.get(roll)
                if html:
                    consecutive_fails = 0
                    total_found += 1
                    # Save HTML
                    file_path = os.path.join(college_dir, f"{roll}.html")
                    with open(file_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(html)
                else:
                    consecutive_fails += 1
                    
            if consecutive_fails >= CONSECUTIVE_FAIL_LIMIT:
                break
                
    with print_lock:
        print(f"  [College {college_code}] Scan complete. Found {total_found} student result(s).")
        
    return True

# ==========================================
#        MAIN SCRAPER ENGINE
# ==========================================
def main():
    if not os.path.exists(LINKS_FILE):
        print(f"[Error] {LINKS_FILE} not found. Run notices scraper first.")
        return
        
    with open(LINKS_FILE, 'r') as f:
        config_entries = json.load(f)
        
    # Filter only REGULAR / PRIVATE entries
    reg_pvt_entries = []
    for idx, entry in enumerate(config_entries):
        if "REGULAR / PRIVATE" in entry.get("description", ""):
            reg_pvt_entries.append((idx, entry))
            
    print(f"Loaded {len(reg_pvt_entries)} REGULAR / PRIVATE entries to process.")
    
    proxy_manager.fetch_proxies()
    load_progress()
    
    for idx, entry in reg_pvt_entries:
        desc = entry["description"]
        pub_date = entry.get("publication_date", "")
        # Extract publication year
        match = re.search(r'20\d{2}', pub_date)
        pub_year = int(match.group(0)) if match else 2024
        
        idx_str = str(idx)
        if idx_str not in progress_data["link_indexes"]:
            progress_data["link_indexes"][idx_str] = {
                "status": "pending",
                "completed_colleges": []
            }
            
        status_info = progress_data["link_indexes"][idx_str]
        if status_info["status"] == "completed":
            continue
            
        print(f"\n🚀 Processing Course: {desc} (Year {pub_year})")
        
        for col in COLLEGE_CODES:
            if col in status_info["completed_colleges"]:
                continue
                
            success = scan_college(idx, desc, pub_year, entry["link"], col)
            if success:
                status_info["completed_colleges"].append(col)
                status_info["status"] = "in_progress"
                save_progress()
            else:
                # Retry session initialization once
                time.sleep(2)
                
        # If all colleges completed
        if len(status_info["completed_colleges"]) == len(COLLEGE_CODES):
            status_info["status"] = "completed"
            save_progress()
            print(f"🎉 Fully completed: {desc}")

if __name__ == "__main__":
    main()
