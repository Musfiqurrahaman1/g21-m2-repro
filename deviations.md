# G21 / P16 - Clarifications and deviations log (M2, Lab 4)

Group 21 - Self-Admitted Aging Debt (Sridharan, Mäntylä, Rantala; EMSE 2025).
Members: Musfiqur Rahaman, Jusmir AslamUddin, Shiam MD Hossain.

**How to use this file.** The M1 entry (in the Student Workbook and the tracker) is NOT edited.
Everything below is either a *clarification* (M1 was silent or ambiguous; we make a bounded
decision) or a *deviation* (M1 genuinely changes). Each entry must be confirmed and dated by the
group **before** the full run (`classify.py` without `--limit`). Do not change an entry after
seeing the output; add a new dated entry instead.

Status values: PROPOSED (drafted with AI assistance, not yet agreed) -> CONFIRMED (group agreed, date + initials).

---

## D-00 - Provenance note: label distribution was seen before the run
- Date: 2026-10-23
- While inspecting the released file's structure, the AI assistant (Claude) printed the value counts
  of the `ad_types_manual` column. The most frequent label, `legacy_backwards_compatibility`
  (about 1,363 of the 2,562 aging-debt rows), is an **Active** category in the paper's taxonomy,
  so the group knows the Dormant share is unlikely to be near 96% in this file.
- Consequence: the M1 expected value, tolerance and floor are **left exactly as frozen**. Changing
  them now would be answer-chasing. If the run is NOT REPRODUCED, that is reported and explained
  (see C-06), not fixed.
- Status: CONFIRMED / PROPOSED  (group to tick) - Date/initials: ____

## C-01 - Sampling population and seed
- Source: Zenodo 10.5281/zenodo.15211796 (version v2), `replication_package.zip` ->
  `gold_standard_data/gold_standard_saad_comments.xlsx`.
- The file has 3,437 rows: 2,562 confirmed aging-debt comments plus 875 rows labelled
  `not_aging_debt_but_explanatory`.
- Decision: sample **500 comments uniformly at random from all 3,437 rows** (M1 says "the released
  dataset"). Comment ids are sorted, then `random.Random(seed).sample` is used. Seed: **42**.
  Ids saved to `data/sample_ids.csv`; seed, population and file hashes in `data/sample_manifest.json`.
- Status: PROPOSED - Seed confirmed as ____ - Date/initials: ____

## C-02 - Cleaning of `saad_patterns.txt`
- The file has 399 patterns plus one blank line. Most lines are wrapped in stray single quotes
  (e.g. `'upgrade to the latest'`), a few have only a trailing quote, some have none.
- Decision: strip whitespace and ONE leading and ONE trailing single quote; skip the blank line.
  No pattern is edited otherwise. Patterns that fail to compile are kept and listed in
  `results/raw/pattern_report.csv`, never silently dropped.
- Status: PROPOSED - Date/initials: ____

## C-03 - Matching rule
- Patterns are applied to the `cleaned_comment` column as regular expressions with Python `re.search`,
  case-insensitive. (The paper does not state case handling for pattern matching.)
- A sampled row that matches no pattern is kept and reported as unmatched.
- Status: PROPOSED - Date/initials: ____

## C-04 - Active/Dormant assignment, multi-label and explanatory rows
- There is no pattern -> category file. The category comes from the row's manual label
  `ad_types_manual`, mapped with the paper's taxonomy (Sec. 6.3):
  - Active: `updates_upgrades`, `aging_maintenance`, `legacy_backwards_compatibility`
  - Dormant: `current_deprecation`, `future_deprecation`, `current_obsolescence`,
    `future_obsolescence`, `non_maintenance`
- About 30 rows carry several labels. Rule: Dormant if ANY label is Dormant, otherwise Active.
- Rows labelled only `not_aging_debt_but_explanatory` are not aging debt: they are excluded from the
  Active/Dormant split but counted and reported.
- Primary metric: Dormant share among sampled rows that matched at least one pattern AND are
  Active or Dormant. Sensitivity variants (all rows; single-label rows only) are descriptive only.
- Status: PROPOSED - Date/initials: ____

## C-05 - Reading of the M1 decision rule
- M1 text: REPRODUCED if the Dormant share is within 10 percentage points of the paper's figure;
  non-reproduction if below about 80%. With a reference of 96%, "within 10 points" means >= 86%.
- M1 does not say what happens between 80% and 86%.
- Decision: the brief defines NOT REPRODUCED as a valid run that fails the pre-declared reproduction
  criterion. The only reproduction criterion is "within 10 points", so **anything below 86% is NOT
  REPRODUCED**, and the 80% mark only separates "narrowly missed" from "clearly missed".
  INCONCLUSIVE/BLOCKED is used only if no valid comparison could be produced (e.g. data or
  environment failure). Numbers (96, 10, 80) are unchanged from M1.
- Status: PROPOSED - Date/initials: ____

## C-06 - Source of the "~96%" figure (open item - validity threat)
- We could not locate "96%" in the paper. What we found: the paper's prevalence analysis (RQ3)
  is computed per project (Wilcoxon signed-rank on 1,957 gold-standard and 3,053 silver-standard
  projects) and reports that the Javadoc/annotation `@deprecated` ("Existing_Aging_Feature") contributes
  94.01% (gold) and 55.85% (silver) of SAAD comments.
- The released gold file is a different population and a different measure (comment level, mined by the
  399 patterns, `@deprecated` was deliberately excluded from the exploration phase).
- Action before the checkpoint: find the exact table/sentence behind 96% (or state that none exists)
  and write it here. In the final write-up, treat the mismatch of populations/measures as a threat to
  the validity of the comparison, regardless of the status.
- Source anchor found: ____ (page/table) - Date/initials: ____

## C-07 - Scope of this run
- Only RQ1 is executed in M2 / Lab 4. RQ2 (new Java repository) has no frozen repository or
  selection rule yet: it is NOT started and no outcome-dependent choice about it is made here.
- No held-out / Event material is used.
- Status: PROPOSED - Date/initials: ____

---

## Deviations (material changes to M1) - add entries ABOVE the next run, never after
_None recorded yet._ Template:

```
## DEV-01 - <short title>
- Date/time: 
- What changed (sample / method / parameter / metric / rule):
- Why it was necessary (what was observed, evidence):
- Effect on interpretation:
- Rerun after this entry? (yes/no, commit):
```

## C-06b - Source of the 96% figure FOUND (update to C-06)
- Date: 2026-10-23
- Source anchor: Table 9 (Section 7.3), gold standard, Dormant SAAD category = 96.53%.
- It is a share of type-level instances over the full PENTACET corpus. About 94% of those instances are Javadoc/annotation @deprecated hits (Existing_Aging_Feature), which are not in the released gold file we sample from. Our comment-level, pattern-based measure is therefore not like-for-like with the 96%.
- The frozen M1 reference (96%) and rule are unchanged.
- Optional descriptive context for the write-up only: the paper's gold split without @deprecated is about 42% Dormant (calculated from Table 9, still to be verified by us). This was noted after the data had been seen and is NOT part of the decision rule.
- Verified against the paper by: ____   Date/initials: ____

## Sign-off (2026-10-23)
- Entries D-00, C-01 to C-07 and C-06b reviewed and accepted as written (seed 42, population = all 3,437 rows).
- Decided by: Musfiqur Rahaman, 2026-10-23.
- Group confirmation (Jusmir AslamUddin, Shiam MD Hossain): ____ date/initials
