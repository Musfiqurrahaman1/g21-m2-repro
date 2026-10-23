@'
# CS4928 G21 / P16 - Bounded reproduction of Self-Admitted Aging Debt (M2)

Group 21: Musfiqur Rahaman, Jusmir AslamUddin, Shiam MD Hossain.

We reproduce one result from Sridharan, Mantyla and Rantala (EMSE 2025, arXiv 2504.17428) on a bounded sample: the split between Dormant and Active self-admitted aging debt (RQ1). The data and patterns come from the paper's replication package (Zenodo 10.5281/zenodo.15211796, v2).

**Result:** NOT REPRODUCED. The Dormant share in our 500-comment sample is 36.8% (138 of 375), against about 96% expected. See `results/summary.md` for the reasons and limits.

## What is in this repo
- `scripts/` - `sample.py` (draws the sample), `classify.py` (matches patterns and assigns Active/Dormant), `summarise.py` (counts and status)
- `data/` - `sample_ids.csv` and `sample_manifest.json` (the frozen sample); `raw/` holds the two input files and their hashes in `CHECKSUMS.txt`
- `results/raw/` - raw output of the full run; `results/pilot/` - the one-comment test run
- `results/derived_counts.csv`, `results/summary_generated.md` - numbers produced by `summarise.py`
- `results/summary.md` - our write-up
- `deviations.md` - decisions we made before running, and the group sign-off
- `tests/test_pipeline.py` - self-test on made-up data

## How to run it (Windows PowerShell)
```
python -m pip install -r requirements.txt
python tests\test_pipeline.py
```
The test should print PASS. It uses made-up data and is not a study result.

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

## Rules we followed
- The sample, method, metric and thresholds were frozen in M1. Anything we decided afterwards is dated in `deviations.md`.
- Raw outputs were kept as produced and not edited.
- A crash or missing file would count as INCONCLUSIVE/BLOCKED, not NOT REPRODUCED.
- No held-out or Event material was used.
- Claude (an AI assistant) helped us write the scripts and draft the write-up. We ran everything ourselves and checked the numbers, and we can explain each script.

The tag `M2_REPRO` marks the commit we submitted for the M2 checkpoint.
'@ | Set-Content -Path README.md -Encoding UTF8
