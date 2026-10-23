# CS4928 G21 / P16 - M2 bounded reproduction (Self-Admitted Aging Debt)

Reproduces, on a bounded sample, the Active/Dormant split of self-admitted aging debt using the
paper's released data and patterns (Zenodo 10.5281/zenodo.15211796, v2). RQ1 only.

Contents: `scripts/` (sample, classify, summarise), `deviations.md` (decisions log),
`results/summary.md` (your write-up template), `tests/` (self-test on made-up data).

## Before you run anything
1. Read `deviations.md`. Agree each entry, tick it and put today's date and initials. **Do this before the full run.**
2. Find the source of the "~96%" figure in the paper and write it in C-06.

## Setup (Windows PowerShell; on Mac/Linux use `python3` and `shasum -a 256`)
```
py -m pip install -r requirements.txt
py tests\test_pipeline.py                     # should print PASS (synthetic data, not a result)
```
Unzip the Zenodo `replication_package.zip` and copy these two files into `data\raw\`:
`gold_standard_saad_comments.xlsx` and `saad_patterns.txt`. Then record their hashes:
```
Get-FileHash data\raw\* -Algorithm SHA256 | Format-List | Out-File data\raw\CHECKSUMS.txt
```

## Run (in this order)
```
# 1. frozen sample (seed 42 is the proposed value in C-01; use whatever the group agreed)
py scripts\sample.py --input data\raw\gold_standard_saad_comments.xlsx --seed 42
git add data\sample_ids.csv data\sample_manifest.json
git commit -m "M2: frozen sample (seed 42, n=500)"

# 2. pilot - ONE comment, separate folder, check the row by eye
py scripts\classify.py --input data\raw\gold_standard_saad_comments.xlsx --patterns data\raw\saad_patterns.txt --limit 1 --out results\pilot

# 3. full bounded run
py scripts\classify.py --input data\raw\gold_standard_saad_comments.xlsx --patterns data\raw\saad_patterns.txt

# 4. derive the result from the raw output
py scripts\summarise.py
```
Then fill `results/summary.md` (everything marked `[FILL]`), commit, tag and push:
```
git add -A
git commit -m "M2: bounded reproduction run and evidence"
git tag M2_REPRO
git push origin main --tags
```
Link the tag in the tracker (RQs and Milestones sheet, row G21: "Reproduction result" and "Evidence link").

## Rules to keep (from the Lab 4 brief)
- Do not change the sample, patterns handling, metric or thresholds after seeing the output.
  If something material must change, write a dated deviation in `deviations.md` BEFORE rerunning.
- Keep every raw output you use. Do not overwrite `results/raw/classification.csv` with an edited version.
- A crash, missing file or environment problem is INCONCLUSIVE/BLOCKED, not NOT REPRODUCED.
- No held-out / Event material.
- GenAI helped write these scripts. Each of you must be able to explain what they do; you are
  responsible for checking the output. A number from an AI is not evidence; a number from your run is.

## What the scripts do (so you can explain them)
- `sample.py` sorts all comment ids, then draws 500 with `random.Random(seed)`. Same seed -> same sample.
- `classify.py` loads the cleaned patterns, searches each sampled comment (case-insensitive regex),
  maps the row's manual label to Active/Dormant/Explanatory with the paper's taxonomy, and writes one
  row per sampled comment (nothing dropped) plus a run log with file hashes and versions.
- `summarise.py` reads only the raw CSV and computes counts, the Dormant share, a Wilson 95% interval,
  descriptive sensitivity checks, a mechanical status per the M1 rule, and a trace example.
