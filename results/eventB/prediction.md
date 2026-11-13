# Event B prediction - G21 / P16 (written before any change)

Written 2026-11-13, before we changed any code. The Week 9 state is the tag `PRE_EVENT_B`.
AI note: Claude helped draft this text. We checked it against the code at `PRE_EVENT_B`.

## The event
Assume a nearby library API is deprecated or removed. Our project is Python, so the nearby library is
pandas. We assume the call we use to read the gold Excel file, `pd.read_excel(..., dtype=str)`, is
deprecated (or its default Excel engine changes). This is our assumption, as the event says "assume".

## Week 9 decision (not rewritten)
We pulled the multi-label rule out of `categorize()` into named rules (`MULTI_LABEL_RULES`, Strategy idea)
so the rule behind the Dormant share can be swapped and tested. See `results/week9/README.md`.

## Prediction: what the pressure will hit
- **It will hit data loading, not the Week 9 rule.** At `PRE_EVENT_B`, `pd.read_excel` is called in
  **four separate scripts**: `sample.py`, `classify.py`, `make_heldout.py` and `check_deprecated.py`.
  (Our first draft said two. We read only two scripts when we wrote it, then counted with `git grep`
  at the tag before changing any code, and corrected this line. Nothing had been committed or changed.)
  `classify.py` also relies on pandas row access (`df.loc`, `pd.isna`) after loading.
- **The four calls are not identical.** `sample.py`, `classify.py` and `make_heldout.py` read with
  `dtype=str`; `check_deprecated.py` reads without it. That difference already exists, which is the
  divergence risk below.
- **It will not hit `common.py`.** The Strategy rule code is plain Python and does not use pandas.
- **It will not hit `summarise.py`.** It reads the CSV with Python's `csv` module only.
- So we expect the Week 9 decision to be only **partly supported**: it made one rule easy to change,
  but it did nothing about the library boundary, which is duplicated in two scripts.
- Risk we expect: if the copies are fixed differently, the scripts could read the file differently (for
  example different column types), and our sample and results would silently differ.

## Responses we will compare
1. **No structural change.** Patch each `read_excel` call if and when it breaks. Smallest edit now, but two
   places to keep in step (four today).
2. **One small loader function.** Add `load_gold_table(path)` in `common.py`, the only place that calls pandas
   to read the Excel file. All four scripts call it. Trade-off: one extra function, and `common.py` gains a pandas
   import (we will import it inside the function so the pure-Python tests do not need it).
3. **A reader interface with several back-ends** (Excel, CSV, other libraries). Rejected in advance as more
   architecture than this problem needs.

We expect to choose response 2 only if the evidence shows the duplicated call is a real risk. If it does not,
the honest result is response 1.

## How we will compare before and after
- Number of places that call `read_excel` (before: 4, measured with `git grep` at `PRE_EVENT_B`).
- Files changed and lines changed.
- `tests/test_pipeline.py` and `tests/test_multilabel_rule.py` still PASS.
- Default run gives a `classification.csv` identical (same sha256) to the Week 9 one, so results do not change.
- A test that simulates the loader failing, to show how many places must change.
- Whether `check_deprecated.py` (no `dtype=str`) and the others now read the file the same way.

## How new debt will be recorded
Any dependency we knowingly leave in place is recorded in `docs/eventB-debt.md` and as a one-line
`AGING-DEBT` comment at the code that depends on the library, with the date and the library name.
