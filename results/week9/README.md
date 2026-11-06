# Week 9 design decision (G21 / P16)

**Design problem.** In `scripts/common.py`, the rule for comments with several labels ("Dormant if ANY label is Dormant", clarification C-04) was hard-coded inside `categorize()`. That rule decides our main result (the Dormant share), but it could not be swapped or tested on its own.

**Alternatives considered.**
1. No change. Simplest, but the rule stays hidden and untestable.
2. Add an if/else flag inside `categorize()`. Quick, but every new rule makes the function longer.
3. Pull the rule out into small named functions in `MULTI_LABEL_RULES` and pass the rule name in (Strategy idea). **Chosen.**

**Change.** `categorize(label, rule="dormant_first")` and `classify.py --multi-label-rule {dormant_first, active_first}`. The default is C-04, so earlier results do not change. The rule used is written to `run_log.txt`.

**Verification.**
- `tests/test_multilabel_rule.py`: PASS. `tests/test_pipeline.py`: PASS.
- Default rule on the real M2 sample gives a `classification.csv` identical to `results/raw/classification.csv`: Dormant 138/375 = 36.8%.
- Default rule on the Event A held-out rows is identical to `results/eventA/classification.csv`.
- Sensitivity, `active_first` (`results/week9/active_first/`): Dormant 125/375 = 33.3% (95% CI 28.8-38.3%). Only 13 mixed rows change, so our NOT REPRODUCED result does not depend on the C-04 rule.
