# Durg University notice Scraper & PDF Roll Number Extractor

A robust pipeline to scrape exam revaluation/retotaling result notifications from Durg University, bypass WAF blocks, download attachment PDFs, and extract structured lists of roll numbers in parallel using multiple Google Gemini API keys.

## Features
1. **Full-Page notice Scraper (`scrape_all.py`)**: Rotates public proxies to bypass the university website's AWS WAF/ALB `403 Forbidden` cloud IP blocks. Scrapes all notices and saves metadata.
2. **Search & Filter**: Locates revaluation and retotaling notices while excluding New Education Policy (NEP) updates.
3. **Parallel Attachment Downloader**: Concurrently downloads PDF notifications from CloudFront.
4. **Structured Gemini Roll Number Extractor (`extract_all_parallel.py`)**:
   - Uses the modern `google-genai` SDK and `gemini-3.1-flash-lite`.
   - Employs **Key Rotation** across multiple API keys to increase rate limit throughput.
   - Enforces **structured schemas** via Pydantic to get clean JSON outputs mapping courses to roll numbers.
   - Includes automatic retry handling for large PDFs that fail due to JSON parsing/truncation.

---

## Installation & Setup

1. Install dependencies:
   ```bash
   pip install google-genai pydantic python-dotenv beautifulsoup4 requests
   ```
2. Configure `.env` file with one or multiple Gemini API keys:
   ```env
   GEMINI_API_KEYS=AIzaSyA...,AIzaSyB...,AIzaSyC...
   ```

---

## Usage

### 1. Scrape all notices:
```bash
python3 scrape_all.py
```
This produces `notices.json` and a filtered list `filtered_notices.json` matching revaluation/retotaling criteria.

### 2. Run Parallel Roll Number Extraction:
```bash
python3 extract_all_parallel.py
```
This reads the downloaded PDFs, uploads them to the Gemini Files API, performs structured extraction, and saves the aggregated database in:
* `all_extracted_results.json`

---

## Datasets Produced
* **[notices.json](notices.json)**: Metadata of 3,180 university notices.
* **[filtered_notices.json](filtered_notices.json)**: 282 revaluation/retotaling notices.
* **[all_extracted_results.json](all_extracted_results.json)**: Extracted course names and roll numbers from 279 processed notice PDFs.