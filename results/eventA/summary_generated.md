# AUTO-GENERATED summary (review before using)

Computed from `results/raw/classification.csv` only. The status below is mechanical; the group must confirm it and write the interpretation in `results/summary.md`.

## Primary result

- Sampled comments: **2937**
- Matched at least one pattern: **2911** (99.1% of sample)
- Matched and labelled Active/Dormant (the split population): **2169**
  - Active: **1356**, Dormant: **813**
  - **Dormant share: 37.5%** (Wilson 95% interval 35.5-39.5%)
- M1 reference: 96% (within 10 points => >= 86%; floor 80%)
- **Mechanical status: NOT REPRODUCED** - Dormant share 37.5% is below the M1 floor of 80%

## All sampled rows by category

| Category | Rows |
|---|---|
| Active | 1359 |
| Dormant | 824 |
| EXPLANATORY | 754 |
| UNMAPPED | 0 |
| MISSING | 0 |

## Descriptive sensitivity checks (not used for the decision)

- Dormant share over ALL Active/Dormant rows, matched or not: 824/2183 = 37.7%
- Dormant share excluding multi-label rows: 520/1862 = 27.9%

## Label token frequency in the sample

| Label | Count |
|---|---|
| legacy_backwards_compatibility | 1234 |
| not_aging_debt_but_explanatory | 754 |
| current_deprecation | 457 |
| future_obsolescence | 322 |
| non_maintenance | 156 |
| current_obsolescence | 111 |
| aging_maintenance | 107 |
| updates_upgrades | 105 |
| future_deprecation | 21 |

## Trace example (claim -> raw evidence -> input)

- Claim: Dormant share = 813/2169 = 37.5%
- Recompute: count rows in `results/raw/classification.csv` with `matched=True` and `category=Dormant` (numerator) and `matched=True` and `category` in {Active, Dormant} (denominator)
- Example row: sample_order 7, comment_id `0062ac376f1790892231cb664cdeafad`, patterns matched on file lines [120|292], manual label `current_deprecation` -> Dormant
- Input identity and run details: `results/raw/run_log.txt` (hashes), `data/sample_manifest.json` (seed, population)
- Look the comment_id up in `gold_standard_saad_comments.xlsx` (column `comment_id`) and the pattern line numbers in `data/raw/saad_patterns.txt`
