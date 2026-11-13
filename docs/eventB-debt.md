# Event B debt record - G21 / P16

Written 2026-11-13, after the prediction (`results/eventB/prediction.md`, tag `EVENT_B_PREDICTION`).
AI note: Claude helped draft this record; we checked it against the code.

Assumption from the event: pandas' Excel reading (`pd.read_excel`) is deprecated or removed.
We record debt in two places: a one-line `AGING-DEBT` comment at the code that depends on the library,
and the table below. The categories are the paper's taxonomy.

| ID | Where | What we depend on | Category | How to exit |
|---|---|---|---|---|
| AD-01 | `scripts/common.py`, `load_gold_table()` | `pandas.read_excel` and the Excel engine behind it (openpyxl) | `future_deprecation` (Dormant) while only assumed; becomes `updates_upgrades` (Active) the day we must migrate | Change that one function. Run `tests/test_single_loader.py`, then compare the `classification.csv` hash with `results/raw/` |
| AD-02 | `scripts/classify.py` | pandas after loading: `set_index`, `df.loc`, `pd.isna` | `updates_upgrades` (Active) | Not addressed on purpose (smallest justified response). If pandas indexing changes, this is the next place to look |
| AD-03 | `scripts/check_deprecated.py` | It read the file without `dtype=str`, unlike the other scripts | Resolved by this change: it now uses the shared loader | None needed |
