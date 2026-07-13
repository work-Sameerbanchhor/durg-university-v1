import os
import json
import urllib.parse
import requests
import random
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty
import sys

# BASE URL and config
BASE_URL = "https://www.durguniversity.ac.in/notices"
HOST_URL = "https://www.durguniversity.ac.in"
MAX_PAGES = 159
PROXY_TEST_URL = "https://www.durguniversity.ac.in/notices"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_proxy_list():
    """Fetch HTTP proxies from ProxyScrape"""
    print("Fetching proxy list from ProxyScrape...")
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all"
    try:
        r = requests.get(url, timeout=10)
        proxies = [line.strip() for line in r.text.split("\n") if line.strip()]
        print(f"Fetched {len(proxies)} proxies from ProxyScrape.")
        return proxies
    except Exception as e:
        print(f"Error fetching proxy list: {e}")
        return []

def test_single_proxy(proxy):
    """Test a single proxy to see if it bypasses the WAF and returns 200 OK"""
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        r = requests.get(PROXY_TEST_URL, headers=HEADERS, proxies=proxies, timeout=5)
        if r.status_code == 200 and "notices-table" in r.text:
            return proxy, True
    except Exception:
        pass
    return proxy, False

def build_proxy_pool(master_list, target_size=15, max_to_test=300):
    """Test proxies from the master list until we get target_size working proxies"""
    print(f"Testing proxies to build a pool of {target_size} working proxies...")
    working_pool = []
    
    # Shuffle so we don't always test the same ones
    proxies_to_test = list(master_list)
    random.shuffle(proxies_to_test)
    proxies_to_test = proxies_to_test[:max_to_test]
    
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(test_single_proxy, p) for p in proxies_to_test]
        for fut in as_completed(futures):
            proxy, success = fut.result()
            if success:
                working_pool.append(proxy)
                print(f"  [Proxy Pool] Added working proxy: {proxy} (Pool size: {len(working_pool)})")
                if len(working_pool) >= target_size:
                    break
                    
    print(f"Finished building proxy pool. Found {len(working_pool)} working proxies.")
    return working_pool

def parse_page_html(html_content):
    """Parse notices from a page's HTML content"""
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="notices-table")
    if not table:
        return []
    
    tbody = table.find("tbody")
    if not tbody:
        tbody = table
        
    rows = tbody.find_all("tr")
    notices = []
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        
        # 1. Date
        date_cell = cells[0]
        date_span = date_cell.find("span", class_="notice-date")
        date_text = date_span.get_text(strip=True) if date_span else date_cell.get_text(strip=True)
            
        # 2. Title & Notice No
        title_cell = cells[1]
        title_div = title_cell.find("div", class_="notice-title")
        title_text = " ".join(title_div.get_text().split()) if title_div else " ".join(title_cell.get_text().split())
            
        notice_no = None
        notice_no_div = title_cell.find("div", class_="notice-date")
        if notice_no_div:
            notice_no_text = " ".join(notice_no_div.get_text().split())
            if "Notice no." in notice_no_text:
                notice_no = notice_no_text.replace("Notice no.", "").strip()
        
        # 3. Attachments
        attachments_cell = cells[2]
        attachments = []
        links = attachments_cell.find_all("a")
        for link in links:
            href = link.get("href")
            if href:
                full_url = urllib.parse.urljoin(HOST_URL, href)
                attachments.append(full_url)
                
        notices.append({
            "date": date_text,
            "title": title_text,
            "notice_no": notice_no,
            "attachments": attachments
        })
        
    return notices

def scrape_page(page_num, proxy_pool, master_list):
    """Scrape a single page, rotating proxies on failure"""
    url = f"{BASE_URL}?page={page_num}" if page_num > 1 else BASE_URL
    attempts = 0
    max_attempts = 15
    
    while attempts < max_attempts:
        attempts += 1
        
        # If proxy pool is empty, rebuild it
        if not proxy_pool:
            print("[Warning] Proxy pool is empty! Rebuilding...")
            new_pool = build_proxy_pool(master_list, target_size=10)
            proxy_pool.extend(new_pool)
            if not proxy_pool:
                print("[Error] Could not find any working proxies. Waiting 10s before retry...")
                time.sleep(10)
                continue
                
        # Pick a random proxy from the pool
        proxy = random.choice(proxy_pool)
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        
        try:
            r = requests.get(url, headers=HEADERS, proxies=proxies, timeout=8)
            if r.status_code == 200 and "notices-table" in r.text:
                notices = parse_page_html(r.text)
                if notices:
                    return page_num, notices
                else:
                    # Succeeded but no notices parsed (invalid page/empty table)
                    return page_num, []
            elif r.status_code == 403:
                # WAF block, remove proxy from pool
                print(f"  [Page {page_num}] Proxy {proxy} returned 403 Forbidden. Removing from pool. Attempt {attempts}/{max_attempts}")
                if proxy in proxy_pool:
                    proxy_pool.remove(proxy)
            else:
                print(f"  [Page {page_num}] Proxy {proxy} returned status {r.status_code}. Attempt {attempts}/{max_attempts}")
        except Exception as e:
            # Connection error/timeout
            pass
            
        time.sleep(random.uniform(0.5, 1.5))
        
    print(f"[Error] Failed to scrape page {page_num} after {max_attempts} attempts.")
    return page_num, None

def main():
    print("Starting Durg University Notices Scraper (All Pages)...")
    
    master_proxies = get_proxy_list()
    if not master_proxies:
        print("No proxies fetched. Cannot proceed.")
        sys.exit(1)
        
    proxy_pool = build_proxy_pool(master_proxies, target_size=20)
    if not proxy_pool:
        print("Could not find any working proxies. Cannot proceed.")
        sys.exit(1)
        
    results = {}
    pages_to_scrape = list(range(1, MAX_PAGES + 1))
    
    # Thread pool for scraping the pages
    print(f"Scraping {MAX_PAGES} pages using concurrent threads...")
    
    # We use a thread pool to download pages. We pass proxy_pool as a shared list.
    # Note: list operations like random.choice, remove, append are thread-safe in Python (GIL).
    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_page = {
            executor.submit(scrape_page, page, proxy_pool, master_proxies): page
            for page in pages_to_scrape
        }
        
        completed = 0
        failed_pages = []
        
        for future in as_completed(future_to_page):
            page = future_to_page[future]
            completed += 1
            try:
                page_num, notices = future.result()
                if notices is not None:
                    results[page_num] = notices
                    print(f"[Progress] {completed}/{MAX_PAGES} pages processed. Page {page_num} scraped successfully ({len(notices)} notices).")
                else:
                    failed_pages.append(page_num)
                    print(f"[Progress] {completed}/{MAX_PAGES} pages processed. Page {page_num} FAILED.")
            except Exception as exc:
                failed_pages.append(page)
                print(f"[Progress] {completed}/{MAX_PAGES} pages processed. Page {page} generated an exception: {exc}")
                
    # Retry failed pages if any
    if failed_pages:
        print(f"\nRetrying {len(failed_pages)} failed pages...")
        retry_pool = build_proxy_pool(master_proxies, target_size=15)
        proxy_pool.extend(retry_pool)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_page = {
                executor.submit(scrape_page, page, proxy_pool, master_proxies): page
                for page in failed_pages
            }
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    page_num, notices = future.result()
                    if notices is not None:
                        results[page_num] = notices
                        print(f"[Retry Success] Page {page_num} scraped successfully ({len(notices)} notices).")
                    else:
                        print(f"[Retry Fail] Page {page_num} failed again.")
                except Exception as exc:
                    print(f"[Retry Fail] Page {page} exception: {exc}")
                    
    # Flatten and sort the results
    all_notices = []
    for page in sorted(results.keys()):
        all_notices.extend(results[page])
        
    print(f"\nScraping complete. Successfully scraped {len(results)}/{MAX_PAGES} pages.")
    print(f"Total notices extracted: {len(all_notices)}")
    
    # Save output to JSON
    output_file = "notices.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_notices, f, indent=2, ensure_ascii=False)
    print(f"Saved all notices to {output_file}")

if __name__ == "__main__":
    main()
