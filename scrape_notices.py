import os
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup

def parse_html(html_content, base_url="https://www.durguniversity.ac.in"):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="notices-table")
    if not table:
        print("Warning: Could not find notices table in HTML.")
        return []
    
    tbody = table.find("tbody")
    if not tbody:
        tbody = table # Fallback
        
    rows = tbody.find_all("tr")
    notices = []
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        
        # 1. Date cell
        date_cell = cells[0]
        date_text = ""
        date_span = date_cell.find("span", class_="notice-date")
        if date_span:
            date_text = date_span.get_text(strip=True)
        else:
            date_text = date_cell.get_text(strip=True)
            
        # 2. Title and Notice No cell
        title_cell = cells[1]
        title_div = title_cell.find("div", class_="notice-title")
        if title_div:
            title_text = " ".join(title_div.get_text().split())
        else:
            # Fallback
            title_text = " ".join(title_cell.get_text().split())
            
        notice_no = None
        notice_no_div = title_cell.find("div", class_="notice-date")
        if notice_no_div:
            # e.g., "Notice no. 625"
            notice_no_text = " ".join(notice_no_div.get_text().split())
            if "Notice no." in notice_no_text:
                notice_no = notice_no_text.replace("Notice no.", "").strip()
        
        # 3. Attachments cell
        attachments_cell = cells[2]
        attachments = []
        links = attachments_cell.find_all("a")
        for link in links:
            href = link.get("href")
            if href:
                # Resolve relative URLs
                full_url = urllib.parse.urljoin(base_url, href)
                attachments.append(full_url)
                
        notices.append({
            "date": date_text,
            "title": title_text,
            "notice_no": notice_no,
            "attachments": attachments
        })
        
    return notices

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scrape Durg University Notices")
    parser.add_argument("--local-file", help="Path to a local HTML file to parse instead of fetching from the web")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default is 1)")
    parser.add_argument("--output", default="notices.json", help="Path to save the JSON output")
    
    args = parser.parse_args()
    
    all_notices = []
    
    if args.local_file:
        print(f"Reading and parsing local file: {args.local_file}")
        with open(args.local_file, "r", encoding="utf-8") as f:
            html = f.read()
        all_notices = parse_html(html)
    else:
        # Scrape live from the web
        base_url = "https://www.durguniversity.ac.in/notices"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        for page in range(1, args.pages + 1):
            url = f"{base_url}?page={page}" if page > 1 else base_url
            print(f"Fetching page {page}: {url}")
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                notices = parse_html(response.text)
                print(f"Successfully scraped {len(notices)} notices from page {page}")
                all_notices.extend(notices)
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break
                
    # Save to JSON
    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_notices, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(all_notices)} notices to {output_path}")

if __name__ == "__main__":
    main()
