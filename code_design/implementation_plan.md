# Implementation Plan: Batch Config Scraper

This plan outlines the architecture, data structures, and implementation steps for building the robust, resumable, and parallel student result scraper (`batch_config_scraper.py`).

---

## 1. Core Requirements

1. **Parallel Workers**: A default pool size of **30 workers** configured globally at the top of the file.
2. **Resumable Progress**: Save state to a `scraping_progress.json` file. If interrupted, the scraper can reload this file and skip fully processed courses and colleges.
3. **Robustness**: Rotate proxies dynamically using a thread-safe proxy manager to bypass AWS WAF/ALB blocks.
4. **Roll Number Generation**: Auto-detect course type, year, and course indicators to construct correct 8-digit or 11/12-digit roll numbers.

---

## 2. Directory & Storage Structure

Results will be stored in a clean directory hierarchy:
```
Htmls/Results/
  ├── UG/
  │    ├── BCA/
  │    │    └── Year_2024/
  │    │         └── College_335/
  │    │              ├── 43350001.html
  │    │              └── 43350002.html
  │    └── BCom/
  │         ...
  └── PG/
       ├── MCom/
       └── MA_English/
```

---

## 3. Scraping & Probing Algorithm

To scrape all students without querying an infinite number of blank rolls:
1. **Colleges Loop**: Loop through all active college codes.
2. **Roll Sequence**:
   - Begin at serial `0001` (e.g. `43350001` or `33350130001`).
   - If a student is found (HTML length > 200), save it locally, reset the `consecutive_fails` counter, and increment the serial.
   - If a student is not found, increment `consecutive_fails`.
3. **Early Stopping**: If `consecutive_fails` exceeds **200**, assume all students in that college have been parsed, and advance to the next college.

---

## 4. Key Components of `batch_config_scraper.py`

### A. Global Configurations
```python
MAX_WORKERS = 30
CONSECUTIVE_FAIL_LIMIT = 200
PROGRESS_FILE = 'scraping_progress.json'
RESULTS_DIR = 'Htmls/Results'
```

### B. Progress Manager
Maintains a JSON file (`scraping_progress.json`) mapping the index of `batch_config.json` entries to college statuses:
```json
{
  "link_indexes": {
    "0": {
      "status": "in_progress",
      "current_college_index": 2,
      "completed_colleges": ["303", "304"]
    },
    "1": {
      "status": "completed"
    }
  }
}
```

### C. Proxy Rotation Manager
- Fetches proxies from ProxyScrape.
- Maintains a thread-safe queue of verified, working proxies.
- If a request returns `403 Forbidden` or `429 Too Many Requests`, the proxy is discarded, and a new one is selected.

### D. ThreadPoolExecutor Architecture
- A thread pool handles the HTTP POST requests for result lookups.
- A lock is used to update the progress tracker file safely.
