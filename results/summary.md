# G21 - M2 reproduction summary (RQ1)

Group 21, project P16 (Self-Admitted Aging Debt). 23 Oct 2026.
AI note: Claude helped us write the scripts and draft this summary. We ran the scripts ourselves and are responsible for the results.

## What we froze in M1
- **Question:** Do we get a similar Dormant/Active split as the paper when we apply its aging-debt patterns to a sample of the released comments?
- **Sample:** 500 random comments from the released dataset (Zenodo 10.5281/zenodo.15211796), fixed seed.
- **Expected:** Dormant is the big majority (about 96% in the paper, Table 9).
- **Rule:** Reproduced if our Dormant share is within 10 points of the paper's. Not reproduced if it is below about 80%.
- Our extra decisions (made before the run, M1 numbers not changed) are in `deviations.md`.

## What we did
1. Took 500 random comments (seed 42) from the 3,437 in `gold_standard_saad_comments.xlsx`.
2. Matched each one against the paper's 399 patterns.
3. Put each comment in Active or Dormant using the authors' labels and the paper's categories.
4. Ran one comment first as a test, then all 500. Nothing was
@'
# G21 - M2 reproduction summary (RQ1)

Group 21, project P16 (Self-Admitted Aging Debt). 23 Oct 2026.
AI note: Claude helped us write the scripts and draft this summary. We ran the scripts ourselves and are responsible for the results.

## What we froze in M1
- **Question:** Do we get a similar Dormant/Active split as the paper when we apply its aging-debt patterns to a sample of the released comments?
- **Sample:** 500 random comments from the released dataset (Zenodo 10.5281/zenodo.15211796), fixed seed.
- **Expected:** Dormant is the big majority (about 96% in the paper, Table 9).
- **Rule:** Reproduced if our Dormant share is within 10 points of the paper's. Not reproduced if it is below about 80%.
- Our extra decisions (made before the run, M1 numbers not changed) are in `deviations.md`.

## What we did
1. Took 500 random comments (seed 42) from the 3,437 in `gold_standard_saad_comments.xlsx`.
2. Matched each one against the paper's 399 patterns.
3. Put each comment in Active or Dormant using the authors' labels and the paper's categories.
4. Ran one comment first as a test, then all 500. Nothing was removed.

Commands are in `README.md`. File hashes and versions are in `data/raw/CHECKSUMS.txt` and `results/raw/run_log.txt`.

## Results
| | Count |
|---|---|
| Sampled comments | 500 |
| Matched a pattern | 493 (98.6%) |
| Did not match | 7 |
| Marked "explanatory" (not aging debt), left out of the split | 121 |
| Used for the split (matched, Active or Dormant) | 375 |
| - Active | 237 |
| - Dormant | 138 |
| **Dormant share** | **36.8%** (95% range 32.1% to 41.8%) |

Raw output: `results/raw/classification.csv`. Numbers: `results/derived_counts.csv`.

## Status: NOT REPRODUCED
The run is valid (no missing comments, no unknown labels, all patterns worked). Our Dormant share is 36.8%. To be within 10 points of 96% we needed 86% or more, and we are also below the 80% line. The whole 95% range is below both.

## Why the numbers may not match
The paper's 96% is a count of label types over its whole dataset, and about 94% of that is `@deprecated` tags. Those tags are not in the file we sampled. So our number and theirs measure different things. We think this explains most of the gap, but this run did not test it. Without the `@deprecated` tags the paper's own gold figure is about 42% Dormant, which is close to ours. TODO( ) check this 42% against Table 9. We only noticed this after seeing the data, so it was not part of our rule.

## How to trace one result
Dormant share = 138 / 375 in `results/raw/classification.csv`. Example: comment `07c8485f57e9fd594472f1f8cb0dd1d6` (row 3 of `data/sample_ids.csv`) matched line 380 of `saad_patterns.txt`, label `future_obsolescence`, so Dormant. We checked this chain by hand: Musfiqur, 23 Oct 2026.

## Limits
- One sample, one seed.
- The file was built from these same patterns, so the 98.6% match rate is expected and proves little.
- Active/Dormant comes from the authors' labels, not from the patterns.
- Some choices were ours: ignore upper/lower case, clean quote marks in the pattern file, count a comment with several labels as Dormant if any label is Dormant.
- We saw the label counts before the run, so we kept the M1 rule unchanged.
- Only RQ1 was done. RQ2 has not started.
- No Event or held-out material was used.

## Next steps
1. Freeze the RQ2 repository and selection rule before looking at results.
2. TODO( ) pilot row checked by eye against the Excel file (name, date).
3. Get Jusmir and Shiam to confirm the sign-off in `deviations.md`.
