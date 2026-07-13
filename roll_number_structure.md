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

## 2. Course-Specific Patterns & Indicators

Below is the list of all unique **REGULAR / PRIVATE** courses found in `batch_config.json` with their corresponding 11/12-digit course indicators (when applicable):

| Course Name | Level | 11/12-Digit Course Indicator | 8-Digit Pattern (2024/2025) | 11/12-Digit Pattern (2023 & Prior) |
|---|---|---|---|---|
| B.A.-B.Ed. (B.A.-B.Ed.) | UG | `097` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 097 + [0001-9999]` |
| B.A.Additional (B.A. Add) | UG | `002` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 002 + [0001-9999]` |
| B.Sc.-B.Ed. (B.Sc.-B.Ed.) | UG | `097` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 097 + [0001-9999]` |
| Bachelor of Arts (B.A) | UG | `001` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 001 + [0001-9999]` |
| Bachelor of Business Administration (BBA) | UG | `001` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 001 + [0001-9999]` |
| Bachelor of Commerce (B.Com) | UG | `004` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 004 + [0001-9999]` |
| Bachelor of Computer Application (BCA) | UG | `013` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 013 + [0001-9999]` |
| Bachelor of Education (B.Ed - sem) | UG | `001` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 001 + [0001-9999]` |
| Bachelor of Laws (L.L.B) | UG | `001` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 001 + [0001-9999]` |
| Bachelor of Library and Information Science (B.Lib I.Sc) | UG | `001` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 001 + [0001-9999]` |
| Bachelor of Physical Education (B.P.Ed.) | UG | `001` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 001 + [0001-9999]` |
| Bachelor of Science (B.Sc) | UG | `007` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 007 + [0001-9999]` |
| Bachelor of Science (Home Science) (B.H.Sc.) | UG | `007` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 007 + [0001-9999]` |
| Diploma in Computer Application (D.C.A. - sem) | Diploma | `081` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 081 + [0001-9999]` |
| M.Sc. Home Science - Food Science and Nutrition (M.Sc.HS-FSN) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| M.Sc. Home Science - Human Development (M.Sc.HS-HD) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| M.Sc. Home Science - Textile and Clothing (M.Sc.HS-TC) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| MASTER OF PHILOSOPHY IN CLINICAL PSYCHOLOGY (M.PHIL CLINICAL PSYCHOLOGY) (MPHIL) First Year (1st Year) REGULAR / PRIVATE | UG | `XXX (UG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (UG Course Code) + [0001-9999]` |
| MASTER OF PHILOSOPHY IN CLINICAL PSYCHOLOGY (M.PHIL CLINICAL PSYCHOLOGY) (MPHIL) Second Year (2nd Year) REGULAR / PRIVATE | UG | `XXX (UG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (UG Course Code) + [0001-9999]` |
| MASTER OF PHILOSOPHY IN PSYCHIATRIC SOCIAL WORK (M.PHIL PSYCHIATRIC SOCIAL WORK) (MPHIL) First Year (1st Year) REGULAR / PRIVATE | UG | `XXX (UG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (UG Course Code) + [0001-9999]` |
| MASTER OF PHILOSOPHY IN PSYCHIATRIC SOCIAL WORK (M.PHIL PSYCHIATRIC SOCIAL WORK) (MPHIL) Second Year (2nd Year) REGULAR / PRIVATE | UG | `XXX (UG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (UG Course Code) + [0001-9999]` |
| Master of Arts in Chhattisgarhi (M.A. Chhattisgarhi) | PG | `054` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 054 + [0001-9999]` |
| Master of Arts in Economics (M.A Economics) | PG | `049` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 049 + [0001-9999]` |
| Master of Arts in English (M.A English) | PG | `041` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 041 + [0001-9999]` |
| Master of Arts in Geography (M.A Geography) | PG | `053` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 053 + [0001-9999]` |
| Master of Arts in Hindi (M.A.H) | PG | `037` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 037 + [0001-9999]` |
| Master of Arts in History (M.A History) | PG | `046` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 046 + [0001-9999]` |
| Master of Arts in Home Science (M.A.H.Sc.) | PG | `054` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 054 + [0001-9999]` |
| Master of Arts in Political Science (M.A Political Sc) | PG | `057` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 057 + [0001-9999]` |
| Master of Arts in Psychology (M.A Psychology) | PG | `071` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 071 + [0001-9999]` |
| Master of Arts in Sociology (M.A Sociology) | PG | `051` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 051 + [0001-9999]` |
| Master of Commerce (M.Com) | PG | `036` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 036 + [0001-9999]` |
| Master of Education (M.Ed) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Laws (LLM) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Library &amp; Information Science (MS Lib I Sc) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science Chemistry (M.Sc.Ch) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science Computer Science (M.Sc.C.S.) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Bio Technology (M Sc Bio Tech) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Botany (M Sc Botany) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Information Technology (M Sc IT) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Mathematics (M Sc Mathematics) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Microbiology (M.Sc.Microbio) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Physics (M Sc Physics) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Science in Zoology (M Sc Zoology) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| Master of Social Work (M.S.W) | PG | `XXX (PG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (PG Course Code) + [0001-9999]` |
| P.G.D.C.A (PGDCA - sem) | Diploma | `083` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 083 + [0001-9999]` |
| PG diploma in Psychological Guidance and Counselling (PGDPGC) | UG | `179` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + 179 + [0001-9999]` |
| PG diploma in Tourism and Hotel Management (PGDTHM) | UG | `XXX (UG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (UG Course Code) + [0001-9999]` |
| PG diploma in Yoga Education and philosophy (PGDYEP) | UG | `XXX (UG Course Code)` | `[4/5] + [College] + [0001-9999]` | `[Year] + [College] + XXX (UG Course Code) + [0001-9999]` |

## 3. Verified Undergraduate (UG) Roll Number Reference Tables

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

## 4. General Usage & Verification Instructions
1. **Verification Pipeline**: Run `python verify_results.py verification/<course>.txt` to test any dataset against the live API.
2. **College Code Probe**: Rotate through standard college codes (`302`, `304`, `305`, `307`, `331`, `333`, `334`, `337`, `339`, `344`, etc.) when extracting new batches.
3. **Year Prefixes**:
   - **Year 2024**: Starts with `4` (e.g., `41091297`)
   - **Year 2025**: Starts with `5` (e.g., `53341056`)
   - **Year 2026**: Starts with `6` (e.g., `63340001`)
   - **Year 2023**: Starts with `3` or `22` (e.g., `32050070003` / `221090050002`)
