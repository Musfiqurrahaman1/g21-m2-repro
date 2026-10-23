# G21 / P16 - M2 bounded reproduction: results summary

> Template. Every `[FILL]` must be written by the group from its OWN run. The numbers come from
> `results/summary_generated.md` after you run the scripts; the interpretation is yours.
> Nothing in this file was produced by running the real data.

## 1. Frozen M1 (copied verbatim, not edited)
- RQ1: _[FILL - paste exact RQ1 from your workbook/tracker]_
- Source anchor in the paper: _[FILL]_
- Sample: 500 comments, fixed seed, released dataset (Zenodo 10.5281/zenodo.15211796)
- Method: apply the paper's published aging-debt patterns, classify matches Active/Dormant
- Expected: Dormant is the large majority (~96% in the paper's gold-standard data)
- Decision rule: REPRODUCED if Dormant share within 10 points of the paper's figure; non-reproduction if below ~80%
- Clarifications/deviations: see `deviations.md` (C-01 .. C-07, D-00)

## 2. Input identity
- File: `gold_standard_data/gold_standard_saad_comments.xlsx`, Zenodo v2, sha256 `[FILL from results/raw/run_log.txt]`
- Patterns: `saad_patterns.txt`, sha256 `[FILL]`
- Sample: seed `[FILL]`, population `[FILL]`, `data/sample_ids.csv` sha256 `[FILL]`

## 3. Environment and execution route
- Python / pandas / openpyxl versions: `[FILL from run_log.txt]`
- Commands run, in order: `[FILL - copy from your terminal history]`
- Pilot (1 comment): `[FILL - what you checked by eye and what you saw]`

## 4. Raw evidence
- `results/raw/classification.csv` (one row per sampled comment, nothing dropped)
- `results/raw/run_log.txt`, `results/raw/pattern_report.csv`
- Failed/awkward cases (unmatched, UNMAPPED, uncompilable patterns): `[FILL - counts and what you did, which should be: nothing, they stay in]`

## 5. Derived result
`[FILL - paste the "Primary result" block from results/summary_generated.md]`

## 6. Trace of one result (be ready to do this live)
Dormant share -> rows in `results/raw/classification.csv` -> command in `run_log.txt` -> comment_id in `data/sample_ids.csv` -> row in the Excel file.
`[FILL - write the actual chain with one real comment_id]`

## 7. Status and justification
- Status: `[REPRODUCED / NOT REPRODUCED / INCONCLUSIVE-BLOCKED / IN PROGRESS]`
- Why, against the M1 rule: `[FILL]`
- Why the comparison with the paper's figure may not be like-for-like (see C-06): `[FILL]`

## 8. Threats and limitations
`[FILL - e.g. one sample of 500 from a file that mixes confirmed and explanatory rows; categories come from manual labels not from the patterns; seed-specific result; source of 96% unverified; multi-label rule; other threats you identify]`

## 9. Held-out boundary
No Event / held-out material used. `[CONFIRM]`

## 10. Next action before the M2 checkpoint
`[FILL - one concrete next step, e.g. freeze RQ2 repository + selection rule]`
