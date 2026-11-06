"""Week 9: unit tests for the swappable multi-label rule in scripts/common.py.

  py tests\\test_multilabel_rule.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from common import DEFAULT_MULTI_LABEL_RULE, categorize  # noqa: E402

MIXED = "current_deprecation, legacy_backwards_compatibility"


def main():
    # default must be C-04, so M2 / Event A results are unchanged
    assert DEFAULT_MULTI_LABEL_RULE == "dormant_first"
    assert categorize(MIXED)[0] == "Dormant"
    assert categorize(MIXED, "dormant_first")[0] == "Dormant"

    # the alternative rule only changes mixed rows
    assert categorize(MIXED, "active_first")[0] == "Active"
    for rule in ("dormant_first", "active_first"):
        assert categorize("current_deprecation", rule)[0] == "Dormant"
        assert categorize("legacy_backwards_compatibility", rule)[0] == "Active"
        assert categorize("current_obsolescence, future_obsolescence", rule)[0] == "Dormant"
        assert categorize("not_aging_debt_but_explanatory", rule)[0] == "EXPLANATORY"
        assert categorize("mystery_label", rule)[0] == "UNMAPPED"

    # an unknown rule name must fail loudly, not fall back silently
    try:
        categorize(MIXED, "no_such_rule")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown rule was accepted")

    print("PASS: multi-label rule tests")


if __name__ == "__main__":
    main()
