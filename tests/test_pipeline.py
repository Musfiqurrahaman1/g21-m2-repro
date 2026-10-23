"""Self-test of the pipeline on a tiny SYNTHETIC dataset (made-up comments).

This only checks that the scripts do what deviations.md says they do. Its output is
NOT a result for the study and must never be reported as one.

  py tests\\test_pipeline.py
"""
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

# (comment text, manual label, expected category, expected matched)
ROWS = [
    ("Legacy code, kept for backwards compatibility.", "legacy_backwards_compatibility", "Active", True),
    ("This method is deprecated since 2.0", "current_deprecation", "Dormant", True),
    ("Obsolete helper, remove in a future release", "current_obsolescence, future_obsolescence", "Dormant", True),
    ("Needs to be updated after upgrading to Java 17", "updates_upgrades", "Active", True),
    ("Remove jumpsite if unused", "not_aging_debt_but_explanatory", "EXPLANATORY", False),
    ("Unused: kept for compat", "non_maintenance", "Dormant", True),
    ("Deprecated, but legacy callers still need it", "current_deprecation, legacy_backwards_compatibility", "Dormant", True),
    ("Old code that needs a rewrite", "aging_maintenance", "Active", True),
    ("Some totally unrelated comment", "legacy_backwards_compatibility", "Active", False),
    ("legacy support for the mystery module", "mystery_label", "UNMAPPED", True),
    ("The legacy parsing is explained here", "not_aging_debt_but_explanatory", "EXPLANATORY", True),
]

# Mimics the quirks of the released file: stray quotes, a missing leading quote, a blank line.
PATTERNS = """'backwards?\\s*compatibility'
'is deprecated'
'^obsolete'
'needs? to be updated'
'^unused'
^deprecated'
old code that
legacy support
legacy parsing

'this one is (broken'
"""


def run(args):
    r = subprocess.run([PY] + [str(a) for a in args], capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(f"command failed: {args}")
    return r


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        xlsx = tmp / "fixture.xlsx"
        pats = tmp / "patterns.txt"
        pd.DataFrame(
            {
                "comment_id": [f"id{i:02d}" for i in range(len(ROWS))],
                "cleaned_comment": [r[0] for r in ROWS],
                "ad_types_manual": [r[1] for r in ROWS],
                "project_id": [f"p{i}" for i in range(len(ROWS))],
            }
        ).to_excel(xlsx, index=False)
        pats.write_text(PATTERNS, encoding="utf-8")

        sample = tmp / "sample_ids.csv"
        outdir = tmp / "raw"
        run([ROOT / "scripts" / "sample.py", "--input", xlsx, "--seed", 1, "--n", len(ROWS), "--out", sample])
        run([ROOT / "scripts" / "classify.py", "--input", xlsx, "--patterns", pats, "--sample", sample, "--out", outdir])
        counts_csv = tmp / "derived_counts.csv"
        run(
            [
                ROOT / "scripts" / "summarise.py",
                "--classification", outdir / "classification.csv",
                "--out", tmp / "summary_generated.md",
                "--counts-out", counts_csv,
            ]
        )

        # per-row expectations
        with open(outdir / "classification.csv", newline="", encoding="utf-8") as f:
            got = {r["comment_id"]: r for r in csv.DictReader(f)}
        assert len(got) == len(ROWS), "a sampled row was dropped"
        for i, (_, _, exp_cat, exp_match) in enumerate(ROWS):
            r = got[f"id{i:02d}"]
            assert r["category"] == exp_cat, (i, r["category"], exp_cat)
            assert (r["matched"] == "True") == exp_match, (i, r["matched"], exp_match)

        # aggregate expectations, worked out by hand from ROWS:
        # matched & Active/Dormant = rows 0,3,7 (Active=3) and 1,2,5,6 (Dormant=4) -> 4/7
        with open(counts_csv, newline="", encoding="utf-8") as f:
            c = {r["key"]: r["value"] for r in csv.DictReader(f)}
        assert c["split_Active"] == "3", c
        assert c["split_Dormant"] == "4", c
        assert c["split_rows_matched_Active_or_Dormant"] == "7", c
        assert c["split_Dormant_pct"] == "57.14", c
        assert c["matched_rows"] == "9" and c["unmatched_rows"] == "2", c
        assert c["category_UNMAPPED_all"] == "1" and c["category_EXPLANATORY_all"] == "2", c
        assert c["mechanical_status"] == "NOT REPRODUCED", c

        # the deliberately broken pattern must be reported, not silently dropped
        with open(outdir / "pattern_report.csv", newline="", encoding="utf-8") as f:
            rep = list(csv.DictReader(f))
        assert sum(1 for r in rep if r["compiled"] == "False") == 1, rep
        assert len(rep) == 10, len(rep)  # blank line skipped, bad pattern kept

        # determinism: same seed => same sample
        again = tmp / "sample_again.csv"
        run([ROOT / "scripts" / "sample.py", "--input", xlsx, "--seed", 1, "--n", len(ROWS), "--out", again])
        assert sample.read_text() == again.read_text(), "sampling is not deterministic"

    print("PASS: pipeline self-test on synthetic data (not a study result)")


if __name__ == "__main__":
    main()
