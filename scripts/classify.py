"""Step 2 - apply the paper's SAAD patterns and assign Active/Dormant.

Pilot (one comment, written to a separate folder so it never overwrites the real run):
  py scripts\\classify.py --input data\\raw\\gold_standard_saad_comments.xlsx ^
     --patterns data\\raw\\saad_patterns.txt --limit 1 --out results\\pilot

Full run:
  py scripts\\classify.py --input data\\raw\\gold_standard_saad_comments.xlsx ^
     --patterns data\\raw\\saad_patterns.txt

Every sampled row is written to the output, matched or not, mapped or not.
Nothing is dropped. Rows whose id cannot be found are written with category MISSING.
"""
import argparse
import csv
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
import pandas as pd

from common import categorize, load_patterns, sha256

FIELDS = [
    "sample_order",
    "comment_id",
    "project_id",
    "matched",
    "n_patterns_matched",
    "matched_pattern_lines",
    "ad_types_manual",
    "category",
    "multi_label",
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--patterns", required=True)
    ap.add_argument("--sample", default="data/sample_ids.csv")
    ap.add_argument("--out", default="results/raw")
    ap.add_argument("--limit", type=int, default=None, help="pilot: only first N sampled ids")
    args = ap.parse_args()

    df = pd.read_excel(args.input, dtype=str).set_index("comment_id")
    patterns = load_patterns(args.patterns)

    with open(args.sample, newline="", encoding="utf-8") as f:
        sample = list(csv.DictReader(f))
    if args.limit:
        sample = sample[: args.limit]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    n_missing = 0
    for s in sample:
        cid = s["comment_id"]
        if cid not in df.index:
            n_missing += 1
            rows.append(
                {
                    "sample_order": s["sample_order"],
                    "comment_id": cid,
                    "project_id": "",
                    "matched": "",
                    "n_patterns_matched": "",
                    "matched_pattern_lines": "",
                    "ad_types_manual": "",
                    "category": "MISSING",
                    "multi_label": "",
                }
            )
            continue
        rec = df.loc[cid]
        text = "" if pd.isna(rec["cleaned_comment"]) else str(rec["cleaned_comment"])
        hits = [p.line_no for p in patterns if p.rx is not None and p.rx.search(text)]
        label = rec["ad_types_manual"]
        category, tokens, multi = categorize(None if pd.isna(label) else label)
        rows.append(
            {
                "sample_order": s["sample_order"],
                "comment_id": cid,
                "project_id": "" if pd.isna(rec["project_id"]) else rec["project_id"],
                "matched": bool(hits),
                "n_patterns_matched": len(hits),
                "matched_pattern_lines": "|".join(str(h) for h in hits),
                "ad_types_manual": "" if pd.isna(label) else label,
                "category": category,
                "multi_label": multi,
            }
        )

    with open(out_dir / "classification.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    with open(out_dir / "pattern_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file_line", "raw", "cleaned", "compiled", "error"])
        for p in patterns:
            w.writerow([p.line_no, p.raw, p.cleaned, p.rx is not None, p.error])

    n_bad = sum(1 for p in patterns if p.rx is None)
    log = [
        f"run_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"command: {' '.join(sys.argv)}",
        f"python: {platform.python_version()}  pandas: {pd.__version__}  openpyxl: {openpyxl.__version__}",
        f"input: {args.input}  sha256: {sha256(args.input)}",
        f"patterns: {args.patterns}  sha256: {sha256(args.patterns)}",
        f"sample: {args.sample}  sha256: {sha256(args.sample)}",
        f"patterns loaded: {len(patterns)}  failed to compile: {n_bad}",
        f"sampled rows processed: {len(rows)}  ids not found in input: {n_missing}",
    ]
    (out_dir / "run_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))

    if args.limit and args.limit <= 10:
        print("\n--- pilot rows ---")
        for r in rows:
            print(r)
    if n_bad:
        print(f"WARNING: {n_bad} pattern(s) failed to compile - see pattern_report.csv", file=sys.stderr)


if __name__ == "__main__":
    main()
