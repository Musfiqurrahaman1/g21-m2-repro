# Event B response - G21 / P16

Written 2026-11-13. Prediction: `results/eventB/prediction.md` (tag `EVENT_B_PREDICTION`, before any change).
Pre-Event-B state: tag `PRE_EVENT_B`. Raw run output: `results/eventB/verification_log.txt`.
AI note: Claude helped draft this write-up and the code change. We ran every command and checked the output ourselves.

## Pressure (assumed, as the event says)
pandas' Excel reading (`pd.read_excel`) is deprecated or removed.

## Responses compared
| Option | Trade-off |
|---|---|
| 1. No structural change: patch each call if it breaks | Smallest edit now, but four places to keep in step. One of them already read the file differently |
| 2. One loader function, `load_gold_table()` in `common.py` (chosen) | One extra function, and `common.py` gains a second job. pandas is imported inside the function, so the pure-Python rule tests still need no pandas |
| 3. A reader interface with several back-ends | Rejected: more architecture than this problem needs |

## What we changed (smallest response)
- Added `load_gold_table()` in `scripts/common.py`, with an `AGING-DEBT` comment. The Week 9 rule code (`MULTI_LABEL_RULES`, `categorize`) was not touched.
- Switched `sample.py`, `classify.py`, `make_heldout.py` and `check_deprecated.py` to call it.
- Added `tests/test_single_loader.py` and `docs/eventB-debt.md`.

## Before and after
| Evidence | Before (`PRE_EVENT_B`) | After |
|---|---|---|
| Places that call `read_excel` | 4 scripts | 1 (`common.py`) |
| Reads the file as text (`dtype=str`) | 3 of 4 scripts | all 4, through one function |
| Tests | `test_pipeline`, `test_multilabel_rule` PASS | those two plus `test_single_loader` PASS |
| M2 sample (seed 42) vs frozen `data/sample_ids.csv` | - | identical (True) |
| M2 `classification.csv` vs `results/raw/` | - | identical (True) |
| Event A `classification.csv` vs `results/eventA/` | - | identical (True) |
| `check_deprecated.py` output | 0 / 695 / 0 | unchanged (no diff in `results/checks/`) |

The comparison runs are in `results/eventB/after/` and `results/eventB/after_eventA/`, with the log in `results/eventB/verification_log.txt`. The frozen M2 and Event A outputs were not overwritten.

## Did our prediction hold?
Yes. We predicted the pressure would hit data loading and not the Week 9 rule, and it did. Two corrections, both made before any code change: we first counted two call sites and found four with `git grep`, and we found that `check_deprecated.py` read the file differently from the others, which was the divergence risk we predicted.

## Conclusion on the Week 9 decision: only partly supported
- Supported: the Strategy rule isolated the multi-label rule, and this event did not touch it. Our results stayed identical.
- Not supported: it did nothing for the library boundary, which is where the pressure fell. That needed a separate small change.
- We keep the Week 9 design and add the loader. We do not revise it.

## Trade-off and risk
- Introduced: `common.py` now has a second job (loading as well as rules and patterns). It is a small, named function, but the module could become a dumping ground if we keep adding to it.
- Avoided: an adapter layer with several readers (option 3), which would have added architecture we do not need.
- Remaining: `classify.py` still depends on pandas after loading (`set_index`, `df.loc`, `pd.isna`). It is recorded as AD-02 in `docs/eventB-debt.md` and was left alone on purpose.

## Limits
Python and pandas versions are in the log. We did not test a real deprecation. We assumed one, as the event says, and simulated the loader failing in `tests/test_single_loader.py`.
