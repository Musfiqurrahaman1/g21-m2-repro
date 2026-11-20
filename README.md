# CS4928 G21 / P16 - Bounded reproduction of Self-Admitted Aging Debt

Group 21: Musfiqur Rahaman, Jusmir AslamUddin, Shiam MD Hossain.

We reproduce one result from Sridharan, Mantyla and Rantala (EMSE 2025, arXiv 2504.17428) on a bounded sample: the split between Dormant and Active self-admitted aging debt (RQ1). The data and patterns come from the paper's replication package (Zenodo 10.5281/zenodo.15211796, v2).

**Result:** NOT REPRODUCED. The Dormant share in our 500-comment sample is 36.8% (138 of 375), against about 96% expected. See `results/summary.md` for the reasons and limits.

**Event B:** one loader function for the gold Excel file. Outputs are identical before and after. The Week 9 decision is only partly supported. See `results/eventB/README.md`.

**Final tag:** `FINAL`.

## What is in this repo
- `scripts/` - `sample.py` (draws the sample), `classify.py` (matches patterns and assigns Active/Dormant), `summarise.py` (counts and status), `common.py` (shared helpers, including the single loader `load_gold_table()`), `check_deprecated.py` (checks the gold file for `@deprecated` rows), `make_heldout.py`
- `data/` - `sample_ids.csv` and `sample_manifest.json` (the frozen sample); `raw/` holds the two input files and their hashes in `CHECKSUMS.txt`
- `results/raw/` - raw output of the full run; `results/pilot/` - the one-comment test run
- `results/derived_counts.csv`, `results/summary_generated.md` - numbers produced by `summarise.py`
- `results/summary.md` - our write-up
- `results/checks/deprecated_check.txt` - output of the `@deprecated` check
- `results/eventB/` - Event B prediction, README (options, before/after, conclusion), verification log and re-run outputs
- `docs/comparability-note.md` - why our number and the paper's are not like-for-like
- `docs/eventB-debt.md` - debt table for Event B
- `deviations.md` - decisions we made before running, and the group sign-off
- `tests/test_pipeline.py` - self-test on made-up data
- `tests/test_single_loader.py` - checks the single-loader design on made-up data

## How to run it (Windows PowerShell)
```
python -m pip install -r requirements.txt
python tests\test_pipeline.py
python tests\test_single_loader.py
```
Both tests should print PASS. They use made-up data and are not study results.

Unzip the Zenodo `replication_package.zip` and copy `gold_standard_saad_comments.xlsx` and `saad_patterns.txt` into `data\raw\`. Then run, in this order:
```
python scripts\sample.py --input data\raw\gold_standard_saad_comments.xlsx --seed 42
python scripts\classify.py --input data\raw\gold_standard_saad_comments.xlsx --patterns data\raw\saad_patterns.txt --limit 1 --out results\pilot
python scripts\classify.py --input data\raw\gold_standard_saad_comments.xlsx --patterns data\raw\saad_patterns.txt
python scripts\summarise.py
```
On Mac or Linux use `python3`. The second command is the one-comment pilot, and the third is the full run.

## What the scripts do
- `sample.py` sorts all comment ids and draws 500 with `random.Random(seed)`, so the same seed gives the same sample.
- `classify.py` cleans the 399 patterns and searches each sampled comment (case-insensitive regex). It takes Active or Dormant from the authors' manual label using the paper's taxonomy. It writes one row per sampled comment, with nothing dropped, plus a run log with file hashes and versions.
- `summarise.py` reads only the raw CSV and computes the counts, the Dormant share, a Wilson 95% interval, a status under our M1 rule, and a trace example.
- Every script that reads the gold Excel file does so through `load_gold_table()` in `scripts/common.py`.

## Later work (Week 9 and Event B)
- Week 9 design decision: the multi-label rule is swappable (`MULTI_LABEL_RULES` in `scripts/common.py`, `--multi-label-rule` in `classify.py`). Tag `PRE_EVENT_B`. Sensitivity run with `active_first`: Dormant 125 of 375 = 33.3%.
- Event B (assumed deprecation of pandas `read_excel`): prediction recorded first (tag `EVENT_B_PREDICTION`), then one loader function `load_gold_table()` (tag `EVENT_B_RESPONSE`). Outputs are identical before and after (sha256 hashes in `results/eventB/verification_log.txt`).
- Conclusion: the Week 9 decision is only partly supported. It covered the rule but not data loading. The trade-off is that `common.py` now has a second job. Remaining debt (AD-02, pandas row access in `classify.py`) is in `docs/eventB-debt.md`.
- Why the M2 result differs from the paper: `docs/comparability-note.md` and `results/checks/deprecated_check.txt` (the released gold file has 0 `@deprecated` rows).

## Rules we followed
- The sample, method, metric and thresholds were frozen in M1. Anything we decided afterwards is dated in `deviations.md`.
- Raw outputs were kept as produced and not edited.
- A crash or missing file would count as INCONCLUSIVE/BLOCKED, not NOT REPRODUCED.
- No held-out or Event material was used in M2.
- We used AI to help us write the scripts and draft the write-up. We ran everything ourselves and checked the numbers, and we can explain each script. One example: our first Event B prediction counted two places that read the data, our own check found four, and we corrected it before changing any code.

## Tags
`M2_REPRO` (the commit submitted for the M2 checkpoint), `PRE_EVENT_A`, `PRE_EVENT_B`, `EVENT_B_PREDICTION`, `EVENT_B_RESPONSE`, `FINAL`. Tags are not moved after they are pushed.
