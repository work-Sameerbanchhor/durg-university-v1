# @title Unified UG Scraper  BCA, BCom, BA, BSc
# Handles 1st, 2nd, and Final Year Result sets from durg.ucanapply.com with Resume feature

import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
import time
from requests.adapters import HTTPAdapter
import json
from datetime import datetime

# ==========================================
#        MASTER CONFIGURATION
# ==========================================
LINKS_FILE = 'batch_config.json'
AJAX_URL   = "https://durg.ucanapply.com/get-result-details"

MAX_WORKERS           = 90     # Parallel threads per chunk
MAX_SERIAL_PER_COLLEGE = 9999  # Max roll serial to probe
CONSECUTIVE_FAIL_LIMIT = 200   # Gap tolerance after first hit
BASE_FOLDER = "Htmls/UG_Results"

# ==========================================
#        YEAR LEVEL CONFIGURATION
# ==========================================
# Maps folder names to the possible keywords found in the ucanapply link descriptions
YEAR_LEVELS = {
    "First_Year": ["first year", "1st year"],
    "Second_Year": ["second year", "2nd year"],
    "Final_Year": ["final year", "3rd year", "third year"]
}

# ==========================================
#        COLLEGE CODES (HARDCODED)
# ==========================================
COLLEGE_CODES = [
    '303', '304', '305', '307',
    '331', '332', '333', '334', '335',
    '337', '338', '339', '340', '341', '344',
    '352', '366', '381', '386'
]

# ==========================================
#     COURSE DEFINITIONS
# ==========================================
COURSES = {
    "BCA": {
        "folder"  : "BCA",
        "keywords": ["b.c.a", "bca", "bachelor of computer application"],
        "batches" : [
            {"id": "B1_2019", "year": 2019, "roll_algo": lambda c, i: f"9{c}015{i:04d}"},
            {"id": "B2_2020", "year": 2020, "roll_algo": lambda c, i: f"9{c}014{i:04d}"},
            {"id": "B3_2021", "year": 2021, "skip": True},
            {"id": "B4_2022", "year": 2022, "roll_algo": lambda c, i: f"2{c}013{i:04d}"},
            {"id": "B5_2023", "year": 2023, "roll_algo": lambda c, i: f"3{c}013{i:04d}"},
            {"id": "B6_2024", "year": 2024, "roll_algo": lambda c, i: f"4{c}{i:04d}"},
            {"id": "B7_2025", "year": 2025, "roll_algo": lambda c, i: f"5{c}{i:04d}"},
        ]
    },
    "BCom": {
        "folder"  : "BCom",
        "keywords": ["b.com", "bachelor of commerce"],
        "batches" : [
            {"id": "B1_2019", "year": 2019, "roll_algo": lambda c, i: f"9{c}006{i:04d}"},
            {"id": "B2_2020", "year": 2020, "roll_algo": lambda c, i: f"9{c}005{i:04d}"},
            {"id": "B3_2021", "year": 2021, "roll_algo": lambda c, i: f"2{c}005{i:04d}"},
            {"id": "B4_2022", "year": 2022, "roll_algo": lambda c, i: f"2{c}004{i:04d}"},
            {"id": "B5_2023", "year": 2023, "roll_algo": lambda c, i: f"22{c}005{i:04d}"},
            {"id": "B6_2024", "year": 2024, "roll_algo": lambda c, i: f"4{c}{i:04d}"},
            {"id": "B7_2025", "year": 2025, "roll_algo": lambda c, i: f"5{c}{i:04d}"},
        ]
    },
    "BSc": {
        "folder"  : "BSc",
        "keywords": ["b.sc", "bsc", "bachelor of science"],
        "batches" : [
            {"id": "B1_2019", "year": 2019, "roll_algo": lambda c, i: f"9{c}009{i:04d}"},
            {"id": "B2_2020", "year": 2020, "roll_algo": lambda c, i: f"9{c}008{i:04d}"},
            {"id": "B3_2021", "year": 2021, "roll_algo": lambda c, i: f"2{c}008{i:04d}"},
            {"id": "B4_2022", "year": 2022, "roll_algo": lambda c, i: f"2{c}007{i:04d}"},
            {"id": "B5_2023", "year": 2023, "roll_algo": lambda c, i: f"3{c}008{i:04d}"},
            {"id": "B6_2024", "year": 2024, "roll_algo": lambda c, i: f"4{c}{i:04d}"},
            {"id": "B7_2025", "year": 2025, "roll_algo": lambda c, i: f"5{c}{i:04d}"},
        ]
    },
    "BA": {
        "folder"  : "BA",
        "keywords": ["b.a.", "bachelor of arts", " b.a "],
        "batches" : [
            {"id": "B1_2019", "year": 2019, "roll_algo": lambda c, i: f"9{c}003{i:04d}"},
            {"id": "B2_2020", "year": 2020, "roll_algo": lambda c, i: f"9{c}002{i:04d}"},
            {"id": "B3_2021", "year": 2021, "roll_algo": lambda c, i: f"2{c}002{i:04d}"},
            {"id": "B4_2022", "year": 2022, "roll_algo": lambda c, i: f"2{c}001{i:04d}"},
            {"id": "B5_2023", "year": 2023, "roll_algo": lambda c, i: f"3{c}001{i:04d}"},
            {"id": "B6_2024", "year": 2024, "roll_algo": lambda c, i: f"4{c}{i:04d}"},
            {"id": "B7_2025", "year": 2025, "roll_algo": lambda c, i: f"5{c}{i:04d}"},
        ]
    },
}

# ==========================================
#           CORE FUNCTIONS
# ==========================================

def load_json_data():
    if not os.path.exists(LINKS_FILE):
        print(f"âŒ CRITICAL: {LINKS_FILE} not found.")
        return []
    with open(LINKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_exact_link(json_data, course_keywords, tgt_year, level_keywords):
    """
    Finds the exact link matching the course, regular status, year of publication,
    and specifically the academic year level (1st, 2nd, or Final year).
    """
    for item in json_data:
        title = item['description'].lower()
        
        # 1. Must match course keywords
        if not any(kw.lower() in title for kw in course_keywords):
            continue
            
        # 2. Must be regular/private (avoids supplementary/reval if desired)
        if "regular" not in title:
            continue
            
        # 3. Must match the specific academic year level (First, Second, Final)
        if not any(level_kw in title for level_kw in level_keywords):
            continue

        # 4. Must match the target publication year
        try:
            date_obj = datetime.strptime(item['publication_date'], "%d/%m/%Y")
            if date_obj.year == tgt_year:
                return item
        except:
            pass
            
    return None


def get_high_speed_session(url):
    s = requests.Session()
    adapter = HTTPAdapter(pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS)
    s.mount("https://", adapter)
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
    })
    try:
        r = s.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', {'name': '_token'})['value']
        payload = {
            'COURSECD':   soup.find('input', {'name': 'COURSECD'})['value'],
            'SEMCODE':    soup.find('input', {'name': 'SEMCODE'})['value'],
            'RESULTTYPE': soup.find('input', {'name': 'RESULTTYPE'})['value'],
            'session':    soup.find('input', {'name': 'session'})['value'],
            'tcc':        soup.find('input', {'name': 'tcc'})['value'],
            'p1': '', 'all': ''
        }
        return s, payload, token
    except:
        return None, None, None


def fetch_result(session, roll, url, payload, token):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-TOKEN': token,
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    data = payload.copy()
    data['EXAMROLLNUMBER'] = roll
    data['_token'] = token
    try:
        r = session.post(AJAX_URL, data=data, headers=headers, timeout=6)
        if r.status_code == 200:
            rj = r.json()
            if 'html' in rj and len(rj['html']) > 200:
                return roll, rj['html']
    except:
        pass
    return roll, None


def process_batch(log_prefix, batch_cfg, colleges, link_item, out_folder):
    print(f"\nðŸš€ [{log_prefix}] BATCH: {batch_cfg['id']} â€” {link_item['description'][:80]}")
    print(f"   ðŸ“… Published: {link_item['publication_date']}  |  ðŸ”— {link_item['link'][:70]}")

    url = link_item['link']
    session, payload, token = get_high_speed_session(url)
    if not token:
        print("   âŒ Failed to initialise session token â€” skipping batch.")
        return

    batch_folder = os.path.join(out_folder, batch_cfg['id'])
    os.makedirs(batch_folder, exist_ok=True)

    for coll in colleges:
        found_any = False
        consecutive_fails = 0
        total_saved = 0

        for chunk_start in range(1, MAX_SERIAL_PER_COLLEGE + 1, MAX_WORKERS):
            tasks = []
            local_results = []  # To hold records that already exist locally

            # Evaluate each item within the current chunk sequence
            for i in range(chunk_start, min(chunk_start + MAX_WORKERS, MAX_SERIAL_PER_COLLEGE + 1)):
                roll = batch_cfg['roll_algo'](coll, i)
                filepath = os.path.join(batch_folder, f"{roll}.html")
                
                # RESUME FEATURE: Check file status before issuing thread pool assignments
                if os.path.exists(filepath):
                    local_results.append((roll, "EXISTS"))
                else:
                    tasks.append(roll)

            # Fire concurrent requests only for non-existent files
            network_results = []
            if tasks:
                with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_map = {
                        executor.submit(fetch_result, session, r, url, payload, token): r
                        for r in tasks
                    }
                    for future in concurrent.futures.as_completed(future_map):
                        network_results.append(future.result())

            # Consolidate and sort both types of hits to maintain sequence processing
            combined_results = local_results + network_results
            combined_results.sort(key=lambda x: x[0])

            college_done = False
            for roll, html in combined_results:
                if html == "EXISTS":
                    found_any = True
                    consecutive_fails = 0
                    total_saved += 1
                elif html:
                    found_any = True
                    consecutive_fails = 0
                    total_saved += 1
                    with open(os.path.join(batch_folder, f"{roll}.html"), "w", encoding="utf-8") as f:
                        f.write(html)
                else:
                    if found_any:
                        consecutive_fails += 1

                if found_any and consecutive_fails >= CONSECUTIVE_FAIL_LIMIT:
                    college_done = True
                    break

            print(
                f"\r   ðŸ¢ College {coll} | Scanned to {chunk_start + len(combined_results) - 1} | Found/Verified: {total_saved}",
                end="", flush=True
            )
            if college_done:
                break

        if total_saved > 0:
            print(f"\n   âœ… College {coll} done. Total Records: {total_saved}")
        else:
            print(f"\r   ðŸ¢ College {coll} | âŒ No students found.")


# ==========================================
#           MAIN EXECUTION
# ==========================================
def main():
    links_data = load_json_data()
    if not links_data:
        print("âŒ Dataset not found â€” aborting.")
        return

    print("=" * 80)
    print("  ðŸŽ“ UNIFIED UG SCRAPER â€” BCA | BCom | BSc | BA (ALL YEARS)")
    print("=" * 80)

    # Loop through all courses
    for course_name, course_cfg in COURSES.items():
        
        # Nested loop: Now we check First_Year, Second_Year, and Final_Year for each course
        for level_name, level_keywords in YEAR_LEVELS.items():
            
            # Directory structure: UG_Results / BSc / First_Year / B1_2019 / roll.html
            out_folder = os.path.join(BASE_FOLDER, course_cfg["folder"], level_name)
            os.makedirs(out_folder, exist_ok=True)

            print(f"\n{'â”€' * 80}")
            print(f"  ðŸ“š COURSE: {course_name}  |  LEVEL: {level_name.replace('_', ' ')}")
            print(f"{'â”€' * 80}")

            for batch_cfg in course_cfg["batches"]:
                if batch_cfg.get("skip"):
                    print(f"  âš ï¸  [{course_name} - {level_name}] {batch_cfg['id']} â€” no data (skipped)")
                    continue

                # Pass the level_keywords to dynamically find 1st, 2nd, or 3rd year links
                link_item = find_exact_link(links_data, course_cfg["keywords"], batch_cfg["year"], level_keywords)
                
                if not link_item:
                    print(f"  âŒ [{course_name} - {level_name}] {batch_cfg['id']} â€” no link found for year {batch_cfg['year']}")
                    continue

                log_prefix = f"{course_name} - {level_name}"
                process_batch(log_prefix, batch_cfg, COLLEGE_CODES, link_item, out_folder)
                time.sleep(2)

    print(f"\n{'=' * 80}")
    print("  ðŸŽ‰  ALL UG COURSES (1ST, 2ND, & FINAL YEARS) COMPLETE!")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()