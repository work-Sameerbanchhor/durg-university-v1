import os
import sys
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ==========================================
# MASTER CONFIGURATION & VERIFICATION SETTINGS
# ==========================================
AJAX_URL = "https://durg.ucanapply.com/get-result-details"
BATCH_CONFIG_PATHS = [
    os.path.join(os.path.dirname(__file__), "source_code", "batch_config.json"),
    os.path.join(os.path.dirname(__file__), "batch_config.json")
]
VERIFICATION_TXT = os.path.join(os.path.dirname(__file__), "verification", "bsc.txt")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "verification", "output")


def load_verification_cases():
    """
    Parses verification/bsc.txt or returns default test cases.
    """
    cases = []
    if os.path.exists(VERIFICATION_TXT):
        print(f"📖 Reading ground truth verification file: {VERIFICATION_TXT}")
        with open(VERIFICATION_TXT, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
            header = lines[0].split('\t')
            for line in lines[1:]:
                parts = line.split('\t')
                if len(parts) >= 8:
                    cases.append({
                        "course": parts[0],
                        "batch": parts[1],
                        "exam": parts[2],
                        "roll": parts[3],
                        "year_num": int(parts[4]) + 2000 if len(parts[4]) == 2 else int(parts[4]),
                        "college_code": parts[5],
                        "course_code": parts[6],
                        "roll_suffix": parts[7]
                    })
    
    if not cases:
        print("⚠️ bsc.txt not found or empty, using default B.Sc. test roll dataset.")
        cases = [
            {"batch": "B1", "exam": "Annual 2019", "roll": "93340090046", "year_num": 2019},
            {"batch": "B2", "exam": "Annual 2020", "roll": "93340080085", "year_num": 2020},
            {"batch": "B3", "exam": "Annual 2021", "roll": "23340080001", "year_num": 2021},
            {"batch": "B4", "exam": "Annual 2022", "roll": "23340070113", "year_num": 2022},
            {"batch": "B5", "exam": "Annual 2023", "roll": "32050070003", "year_num": 2023},
            {"batch": "B6", "exam": "Annual 2024", "roll": "43330594", "year_num": 2024},
            {"batch": "B7", "exam": "Annual 2025", "roll": "53021299", "year_num": 2025},
        ]
    return cases


def load_batch_config():
    for path in BATCH_CONFIG_PATHS:
        if os.path.exists(path):
            print(f"📦 Loading batch configuration from: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    print("❌ ERROR: batch_config.json could not be found.")
    sys.exit(1)


def find_matching_links(config_data, case):
    """
    Finds all candidate B.Sc. links for the specific exam year in batch_config.json.
    Excludes unrelated courses like B.Sc.-B.Ed. or supplementary/reval unless no regular link is found.
    """
    tgt_year = case["year_num"]
    candidates = []

    for item in config_data:
        desc = item.get('description', '')
        desc_lower = desc.lower()
        
        # Must match B.Sc. keywords but exclude B.Sc.-B.Ed., B.Sc. Home Science etc if pure B.Sc. is available
        if not any(k in desc_lower for k in ['b.sc', 'bsc', 'bachelor of science']):
            continue
            
        if 'b.ed' in desc_lower or 'home science' in desc_lower or 'biotechnology' in desc_lower:
            continue

        if 'reval' in desc_lower or 'retotal' in desc_lower:
            continue

        pub_date = item.get('publication_date', '')
        item_year = None
        if pub_date:
            try:
                dt = datetime.strptime(pub_date, "%d/%m/%Y")
                item_year = dt.year
            except:
                pass
        
        if item_year == tgt_year or str(tgt_year) in desc:
            candidates.append(item)

    # Sort candidates so "REGULAR / PRIVATE" comes first
    candidates.sort(key=lambda x: (0 if "regular" in x.get('description', '').lower() else 1))
    return candidates



def get_session_token_and_payload(url):
    """
    Fetches the result portal page and extracts hidden form inputs and CSRF token.
    """
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    try:
        r = s.get(url, timeout=12)
        if r.status_code != 200:
            return None, None, None
            
        soup = BeautifulSoup(r.text, 'html.parser')
        token_el = soup.find('input', {'name': '_token'})
        if not token_el:
            return None, None, None
            
        token = token_el['value']
        payload = {
            'COURSECD':   soup.find('input', {'name': 'COURSECD'})['value'] if soup.find('input', {'name': 'COURSECD'}) else '',
            'SEMCODE':    soup.find('input', {'name': 'SEMCODE'})['value'] if soup.find('input', {'name': 'SEMCODE'}) else '',
            'RESULTTYPE': soup.find('input', {'name': 'RESULTTYPE'})['value'] if soup.find('input', {'name': 'RESULTTYPE'}) else '',
            'session':    soup.find('input', {'name': 'session'})['value'] if soup.find('input', {'name': 'session'}) else '',
            'tcc':        soup.find('input', {'name': 'tcc'})['value'] if soup.find('input', {'name': 'tcc'}) else '',
            'p1': '', 
            'all': ''
        }
        return s, payload, token
    except Exception as e:
        print(f"   ⚠️ Network error initializing session for {url}: {e}")
        return None, None, None


def query_result(session, url, payload, token, roll_number):
    """
    Posts the roll number to the AJAX endpoint to fetch student result HTML.
    """
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-TOKEN': token,
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    data = payload.copy()
    data['EXAMROLLNUMBER'] = str(roll_number)
    data['_token'] = token

    try:
        r = session.post(AJAX_URL, data=data, headers=headers, timeout=10)
        if r.status_code == 200:
            resp_json = r.json()
            html_content = resp_json.get('html', '')
            if len(html_content.strip()) > 200:
                return True, html_content
            else:
                return False, "Empty or short HTML response (No result found)"
        else:
            return False, f"HTTP Error status code {r.status_code}"
    except Exception as e:
        return False, f"Exception during AJAX query: {e}"


def extract_student_info(html_content):
    """
    Parses student details from returned HTML result card.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    info = {}
    
    # Try finding student name, roll number, result status, college name
    name_match = re.search(r"(?:Name of Candidate|Student Name|Name)\s*[:\-]\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    if name_match:
        info['name'] = name_match.group(1).strip()
        
    result_match = re.search(r"(?:Result|Status)\s*[:\-]\s*(PASS|FAIL|SUPP|SUPPLEMENTARY|PROMOTED|WITHHELD)", text, re.IGNORECASE)
    if result_match:
        info['result'] = result_match.group(1).upper()
        
    college_match = re.search(r"(?:College|Institute|Center)\s*[:\-]\s*([A-Za-z0-9\s.,\-]+)", text, re.IGNORECASE)
    if college_match:
        info['college'] = college_match.group(1).strip()[:50]
        
    return info


def main():
    print("=" * 75)
    print("🧪 DURG UNIVERSITY B.SC. RESULTS VERIFICATION & TEST PIPELINE")
    print("=" * 75)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cases = load_verification_cases()
    config = load_batch_config()

    results = []

    print(f"\n🔍 Processing {len(cases)} B.Sc. batch test cases...\n")

    for case in cases:
        batch_id = case.get('batch', 'Unknown')
        exam_name = case.get('exam', '')
        roll = case['roll']
        year = case['year_num']

        print(f"---------------------------------------------------------------------------")
        print(f"👉 Testing Batch {batch_id} | Exam: {exam_name} ({year}) | Roll No: {roll}")

        candidate_links = find_matching_links(config, case)
        if not candidate_links:
            print(f"   ❌ Could not find matching link entry in batch_config.json for B.Sc. year {year}")
            results.append({
                "batch": batch_id, "year": year, "roll": roll,
                "status": "FAIL (No Link Match)", "details": "N/A", "link_desc": "None"
            })
            continue

        print(f"   🔎 Found {len(candidate_links)} potential B.Sc. exam link(s) for year {year}. Probing links...")

        found_success = False
        for link_item in candidate_links:
            url = link_item.get('link', '')
            desc = link_item.get('description', '')
            
            # Initialize session and fetch CSRF token
            session, payload, token = get_session_token_and_payload(url)
            if not session or not token:
                continue

            # Post Roll Number query
            success, html_or_err = query_result(session, url, payload, token, roll)

            if success:
                student_info = extract_student_info(html_or_err)
                student_name = student_info.get('name', 'Found HTML (Details Parsed)')
                status_text = student_info.get('result', 'VALID RESULT')
                print(f"   ✅ SUCCESS on link: {desc[:60]}...")
                print(f"      👤 Candidate: {student_name}")
                if status_text:
                    print(f"      📊 Result:    {status_text}")

                # Save HTML verification file
                out_filename = os.path.join(OUTPUT_DIR, f"BSc_{batch_id}_{year}_{roll}.html")
                with open(out_filename, 'w', encoding='utf-8') as f:
                    f.write(html_or_err)
                print(f"      💾 Saved result HTML to: {out_filename}")

                results.append({
                    "batch": batch_id, "year": year, "roll": roll,
                    "status": f"SUCCESS ({status_text})",
                    "details": student_name,
                    "link_desc": desc[:45]
                })
                found_success = True
                break

        if not found_success:
            print(f"   ❌ FAILED to retrieve result for Roll {roll} across all {len(candidate_links)} candidate link(s).")
            results.append({
                "batch": batch_id, "year": year, "roll": roll,
                "status": "FAIL (No Result Output)",
                "details": "Invalid roll or wrong exam level link",
                "link_desc": candidate_links[0].get('description', '')[:45]
            })

    # Summary Table Output
    print("\n" + "=" * 80)
    print("📋 SUMMARY REPORT - B.SC. RESULTS VERIFICATION")
    print("=" * 80)
    print(f"{'Batch':<6} | {'Year':<5} | {'Roll Number':<12} | {'Status':<20} | {'Candidate Name / Details':<25}")
    print("-" * 80)
    for res in results:
        print(f"{res['batch']:<6} | {res['year']:<5} | {res['roll']:<12} | {res['status']:<20} | {res['details']:<25}")
    print("=" * 80)
    print(f"Saved all result HTML files in: {OUTPUT_DIR}\n")



if __name__ == "__main__":
    main()
