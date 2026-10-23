# AUTO-GENERATED summary (review before using)

Computed from `results/raw/classification.csv` only. The status below is mechanical; the group must confirm it and write the interpretation in `results/summary.md`.

## Primary result

- Sampled comments: **500**
- Matched at least one pattern: **493** (98.6% of sample)
- Matched and labelled Active/Dormant (the split population): **375**
  - Active: **237**, Dormant: **138**
  - **Dormant share: 36.8%** (Wilson 95% interval 32.1-41.8%)
- M1 reference: 96% (within 10 points => >= 86%; floor 80%)
- **Mechanical status: NOT REPRODUCED** - Dormant share 36.8% is below the M1 floor of 80%

## All sampled rows by category

| Category | Rows |
|---|---|
| Active | 241 |
| Dormant | 138 |
| EXPLANATORY | 121 |
| UNMAPPED | 0 |
| MISSING | 0 |

## Descriptive sensitivity checks (not used for the decision)

- Dormant share over ALL Active/Dormant rows, matched or not: 138/379 = 36.4%
- Dormant share excluding multi-label rows: 94/329 = 28.6%

## Label token frequency in the sample

| Label | Count |
|---|---|
| legacy_backwards_compatibility | 225 |
| not_aging_debt_but_explanatory | 121 |
| current_deprecation | 83 |
| future_obsolescence | 40 |
| non_maintenance | 26 |
| current_obsolescence | 17 |
| updates_upgrades | 16 |
| aging_maintenance | 15 |
| future_deprecation | 4 |

## Trace example (claim -> raw evidence -> input)

- Claim: Dormant share = 138/375 = 36.8%
- Recompute: count rows in `results/raw/classification.csv` with `matched=True` and `category=Dormant` (numerator) and `matched=True` and `category` in {Active, Dormant} (denominator)
- Example row: sample_order 3, comment_id `07c8485f57e9fd594472f1f8cb0dd1d6`, patterns matched on file lines [380], manual label `future_obsolescence` -> Dormant
- Input identity and run details: `results/raw/run_log.txt` (hashes), `data/sample_manifest.json` (seed, population)
- Look the comment_id up in `gold_standard_saad_comments.xlsx` (column `comment_id`) and the pattern line numbers in `data/raw/saad_patterns.txt`
