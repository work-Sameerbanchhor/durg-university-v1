# Durg University Roll Number Structure Guide

This document defines the standardized roll number patterns for all **REGULAR / PRIVATE** courses listed in `batch_config.json`.

## 1. Global Pattern Schemes

Durg University assigns roll numbers based on two major schemes, determined by the examination year of the result:

### Scheme A: Year 2024 & 2025 (8-Digit Simplified Format)
A streamlined format applied to **all** undergraduate and postgraduate courses:
```
Format:  [Year_Code][College_Code][Serial_Number]
Length:  8 digits
```
- **Year Code (1 digit)**: `4` for Year 2024 results, `5` for Year 2025 results.
- **College Code (3 digits)**: E.g., `335` for Kalyan PG College, `337` for Govt. Digvijay College.
- **Serial Number (4 digits)**: Sequential serial starting from `0001` to `9999` (e.g., `0129`).
- *Example*: `43350129` (BCA Part 1, Kalyan College, Year 2024)

### Scheme B: Year 2023 & Prior (11/12-Digit Indicator Format)
A structured format containing a unique course indicator code:
```
Format 1 (11-digit): [Year_Code][College_Code][Course_Indicator][Serial_Number]
Format 2 (12-digit): [23][College_Code][Course_Indicator][Serial_Number]
Length:              11 or 12 digits
```
- **Year Code (1 or 2 digits)**: `3` (for 11-digit 2023), `23` (for 12-digit 2023), `9` (for 2019/2020).
- **College Code (3 digits)**: Same 3-digit code.
- **Course Indicator (3 digits)**: Unique code for each course/subject (listed in Section 2).
- **Serial Number (4 digits)**: Sequential serial from `0001` to `9999`.
- *Example*: `33340130018` (BCA Part 1, Year 2023, Course Indicator: `013`, Serial: `0018`)

---

## 2. Verified Undergraduate (UG) Roll Number Reference Tables

The following roll number batches (B1 to B8) have been configured against live `durg.ucanapply.com` result APIs:

### A. Bachelor of Science (B.Sc.)
| Batch | Exam Session | Sample Verified Roll No | Verified Student Name | Scheme & Format |
|---|---|---|---|---|
| **B1** | Annual 2019 | `93340090046` | PRANJALI KANUNGO | 11-Digit (`9 + 334 + 009 + 0046`) |
| **B2** | Annual 2020 | `93340080085` | PALLAVI SHARMA | 11-Digit (`9 + 334 + 008 + 0085`) |
| **B3** | Annual 2021 | `23340080001` | Shaivi Dewangan | 11-Digit (`2 + 334 + 008 + 0001`) |
| **B4** | Annual 2022 | `23340070113` | MEGHA R SOAN | 11-Digit (`2 + 334 + 007 + 0113`) |
| **B5** | Annual 2023 | `32050070003` | AMBE | 11-Digit (`3 + 205 + 007 + 0003`) |
| **B6** | Annual 2024 | `43330594` | ANUSHKA YADAV | 8-Digit (`4 + 333 + 0594`) |
| **B7** | Annual 2025 | `53021299` | ANAMIKA SINGH | 8-Digit (`5 + 302 + 1299`) |
| **B8** | Annual 2026 | `63020001` | *Dynamic Probe* | 8-Digit (`6 + [College] + [Serial]`) |

### B. Bachelor of Arts (B.A.)
| Batch | Exam Session | Sample Verified Roll No | Verified Student Name | Scheme & Format |
|---|---|---|---|---|
| **B1** | Annual 2019 | `91010030001` | SUBHASH KUMAR SAHU | 11-Digit (`9 + 101 + 003 + 0001`) |
| **B2** | Annual 2020 | `91010020001` | girdhar lal | 11-Digit (`9 + 101 + 002 + 0001`) |
| **B3** | Annual 2021 | `21010020001` | ARCHANA | 11-Digit (`2 + 101 + 002 + 0001`) |
| **B4** | Annual 2022 | `21010010001` | AARTI | 11-Digit (`2 + 101 + 001 + 0001`) |
| **B5** | Annual 2023 | `31010010001` | AAMNI | 11-Digit (`3 + 101 + 001 + 0001`) |
| **B6** | Annual 2024 | `41010001` | AAKANKSHA | 8-Digit (`4 + 101 + 0001`) |
| **B7** | Annual 2025 | `51010001` | ABHISHEK | 8-Digit (`5 + 101 + 0001`) |
| **B8** | Annual 2026 | `61010001` | *Dynamic Probe* | 8-Digit (`6 + [College] + [Serial]`) |

### C. Bachelor of Commerce (B.Com)
| Batch | Exam Session | Sample Verified Roll No | Verified Student Name | Scheme & Format |
|---|---|---|---|---|
| **B1** | Annual 2019 | `93020060234` | Swati Jain | 11-Digit (`9 + 302 + 006 + 0234`) |
| **B2** | Annual 2020 | `93330050037` | ANJALI KASHYAP | 11-Digit (`9 + 333 + 005 + 0037`) |
| **B3** | Annual 2021 | `23330050001` | SMRITI ANAND | 11-Digit (`2 + 333 + 005 + 0001`) |
| **B4** | Annual 2022 | `23440040011` | RENUKA VAISHNAV | 11-Digit (`2 + 344 + 004 + 0011`) |
| **B5** | Annual 2023 | `221090050002` | LOKESH KUMAR | 12-Digit (`22 + 109 + 005 + 0002`) |
| **B6** | Annual 2024 | `41091297` | BHASKAR SONBARSA | 8-Digit (`4 + 109 + 1297`) |
| **B7** | Annual 2025 | `53341056` | GARIMA NIRMALKAR | 8-Digit (`5 + 334 + 1056`) |
| **B8** | Annual 2026 | `63340001` | *Dynamic Probe* | 8-Digit (`6 + [College] + [Serial]`) |

### D. Bachelor of Computer Application (BCA)
| Batch | Exam Session | Sample Verified Roll No | Verified Student Name | Scheme & Format |
|---|---|---|---|---|
| **B1** | Annual 2019 | `93370150012` | Md Talib Qureshi | 11-Digit (`9 + 337 + 015 + 0012`) |
| **B2** | Annual 2020 | `93390140002` | Megha Jain | 11-Digit (`9 + 339 + 014 + 0002`) |
| **B3** | Annual 2021 | `23370130001` | ABHISHEK MOURYA | 11-Digit (`2 + 337 + 013 + 0001`) |
| **B4** | Annual 2022 | `23340130017` | PRIYA | 11-Digit (`2 + 334 + 013 + 0017`) |
| **B5** | Annual 2023 | `33340130020` | Omika Jena | 11-Digit (`3 + 334 + 013 + 0020`) |
| **B6** | Annual 2024 | `43311282` | *College 331* | 8-Digit (`4 + 331 + 1282`) |
| **B7** | Annual 2025 | `53341407` | SAKSHI CHOURASIA | 8-Digit (`5 + 334 + 1407`) |
| **B8** | Annual 2026 | `63340001` | *Dynamic Probe* | 8-Digit (`6 + [College] + [Serial]`) |

---

## 3. General Usage & Verification Instructions
1. **Verification Pipeline**: Run `python verify_results.py verification/<course>.txt` to test any dataset against the live API.
2. **College Code Probe**: Rotate through standard college codes (`302`, `304`, `305`, `307`, `331`, `333`, `334`, `337`, `339`, `344`, etc.) when extracting new batches.
3. **Year Prefixes**:
   - **Year 2024**: Starts with `4` (e.g., `41091297`)
   - **Year 2025**: Starts with `5` (e.g., `53341056`)
   - **Year 2026**: Starts with `6` (e.g., `63340001`)
   - **Year 2023**: Starts with `3` or `22` (e.g., `32050070003` / `221090050002`)
