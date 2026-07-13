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

## 3. General Usage Notes
1. **College Code Rotation**: Probing should rotate through the major colleges (e.g. `303`, `335`, `337`) to find student records.
2. **Active Years**: Check publication dates in `batch_config.json` to select either the 8-digit format (for 2024/2025/2026 result releases) or the 11/12-digit format (for older historical results).
