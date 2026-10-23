"""Shared helpers for the CS4928 G21 / P16 (Self-Admitted Aging Debt) M2 reproduction.

Nothing in here makes an empirical choice silently: every rule below is listed in
deviations.md (clarifications C-01 .. C-06) and must be confirmed by the group
BEFORE the full run.
"""
import hashlib
import re
from pathlib import Path

# Category mapping from the paper's taxonomy (Sridharan et al., EMSE 2025, Sec. 6.3):
#   Active  = Updates & Upgrades, Aging Maintenance, Legacy & Backwards Compatibility
#   Dormant = Deprecation (current/future), Obsolescence (current/future), Non-Maintenance
ACTIVE_TYPES = {
    "updates_upgrades",
    "aging_maintenance",
    "legacy_backwards_compatibility",
}
DORMANT_TYPES = {
    "current_deprecation",
    "future_deprecation",
    "current_obsolescence",
    "future_obsolescence",
    "non_maintenance",
}
EXPLANATORY = "not_aging_debt_but_explanatory"


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


class Pattern:
    __slots__ = ("line_no", "raw", "cleaned", "rx", "error")

    def __init__(self, line_no, raw, cleaned, rx, error):
        self.line_no = line_no
        self.raw = raw
        self.cleaned = cleaned
        self.rx = rx
        self.error = error


def load_patterns(path):
    """Load saad_patterns.txt.

    Cleaning rule (clarification C-02): strip whitespace, then ONE leading and ONE
    trailing single quote if present (the released file wraps most lines in stray
    quotes), skip blank lines. Matching is case-insensitive (clarification C-03).
    Patterns that fail to compile are KEPT in the list with rx=None so they show up
    in the pattern report instead of silently disappearing.
    """
    patterns = []
    text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    for i, line in enumerate(text.splitlines(), start=1):
        raw = line.rstrip("\r\n")
        s = raw.strip()
        if not s:
            continue
        cleaned = s
        if cleaned.startswith("'"):
            cleaned = cleaned[1:]
        if cleaned.endswith("'"):
            cleaned = cleaned[:-1]
        try:
            rx = re.compile(cleaned, re.IGNORECASE)
            err = ""
        except re.error as exc:
            rx, err = None, str(exc)
        patterns.append(Pattern(i, raw, cleaned, rx, err))
    return patterns


def categorize(label):
    """Map the manual label string to (category, tokens, multi_label).

    category is one of: Active, Dormant, EXPLANATORY, UNMAPPED.
    Rule (clarification C-04): a row with several labels is Dormant if ANY label is
    Dormant, otherwise Active. A row labelled only as explanatory is EXPLANATORY
    (not aging debt). Anything not in the mapping is UNMAPPED and stays visible.
    """
    if label is None:
        return "UNMAPPED", [], False
    s = str(label).strip()
    if s.lower() == "nan":
        return "UNMAPPED", [], False
    tokens = [t.strip() for t in s.split(",") if t.strip()]
    if not tokens:
        return "UNMAPPED", tokens, False
    multi = len(tokens) > 1
    if tokens == [EXPLANATORY]:
        return "EXPLANATORY", tokens, multi
    known = ACTIVE_TYPES | DORMANT_TYPES
    if any(t not in known for t in tokens):
        return "UNMAPPED", tokens, multi
    if any(t in DORMANT_TYPES for t in tokens):
        return "Dormant", tokens, multi
    return "Active", tokens, multi
