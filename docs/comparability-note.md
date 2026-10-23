# Why our RQ1 result does not match the paper's 96% (Group 21, P16)

Written 23 Oct 2026 at the request of our lab coordinator. The run itself was not blocked. It finished and gave a valid result. This note explains why that result cannot be compared directly with the paper's figure.

## What happened
- Our frozen M1 plan expected Dormant to be the large majority, about 96% as in the paper.
- Our run gave a Dormant share of 36.8% (138 of 375 matched Active/Dormant comments, 95% range 32.1% to 41.8%).
- Under our M1 rule this is NOT REPRODUCED. The status stays as it is.

## Why the two numbers are not like-for-like
1. **The paper's 96.53% is from Table 9** of the paper ("SAAD Prevalence Across Types & Categories"). It is a share of aging-debt type instances over the whole dataset. Table 9 gives the gold standard as 96.53% Dormant and 3.47% Active, and the silver standard as 81.26% Dormant and 18.74% Active.
2. **About 94% of that is one thing:** the row "Current Deprecation (from Existing_Aging_Feature)", the `@deprecated` Javadoc and annotation hits. Table 9 gives it as 94.01% in the gold standard and 55.85% in the silver standard.
3. **That row is not in the file we sampled.** The released gold file (`gold_standard_saad_comments.xlsx`, 3,437 comments) is a comment-level file built from the paper's 399 patterns. The paper left `@deprecated` out of its pattern exploration.
4. So we measured the Dormant share of comments in a pattern-based file. The paper's 96% measures label-type instances including a very large block of `@deprecated` tags. These are different things.

## A rough check (our own calculation, not tested by the run)
If all `@deprecated` instances are Dormant, then without them the paper's gold figure is (96.53 - 94.01) / (100 - 94.01) = 2.52 / 5.99, about 42.1% Dormant. That is close to our 36.8%. This suggests the gap comes from the different measure and not from an error in our run. We have not shown this. The calculation assumes every `@deprecated` instance is Dormant, and it uses percentages read from Table 9.

## What we did not do, and why
- We did not change the M1 numbers (96, 10, 80) after seeing the result. That would be answer-chasing. We did see the label counts before the run (entry D-00 in `deviations.md`), and we say so.
- We did not add the `@deprecated` data to our sample. It is not in the released file, and adding it would be a new method, not our frozen one.
- We noticed the comparability problem after seeing the data, so it was not part of our decision rule.

## What this means for our status
The status is NOT REPRODUCED, with this caveat: the frozen comparison with the paper's 96% was not like-for-like. We think a different way of counting explains most of the gap, but this run does not prove it.

## What would settle it
A fair test needs the paper's full dataset with the `@deprecated` instances, or the same type-level counting method applied to our sample. Neither is part of this bounded run. If the coordinator wants this tested, we would write it as a new dated entry in `deviations.md` before running it, with a new tag, and leave `M2_REPRO` as it is.

## AI use
Claude helped us draft this note. We checked the figures against Table 9 of the paper and against our own output files.
