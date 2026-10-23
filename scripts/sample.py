"""Step 1 - draw the frozen sample (M1: 500 comments, fixed random seed).

Usage (Windows):
  py scripts\\sample.py --input data\\raw\\gold_standard_saad_comments.xlsx --seed 42

The seed has NO default on purpose: the group must state it (and record it in
deviations.md) before running. Do not change seed/population after seeing results.
"""
import argparse
import csv
import json
import platform
import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from common import EXPLANATORY, sha256


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="gold_standard_saad_comments.xlsx")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument(
        "--population",
        choices=["all", "saad_only"],
        default="all",
        help="all = every row of the file (recommended, clarification C-01); "
        "saad_only = drop rows labelled not_aging_debt_but_explanatory",
    )
    ap.add_argument("--out", default="data/sample_ids.csv")
    args = ap.parse_args()

    df = pd.read_excel(args.input, dtype=str)
    if df["comment_id"].duplicated().any():
        raise SystemExit("duplicate comment_id values in input - stop and investigate")
    total_rows = len(df)
    if args.population == "saad_only":
        df = df[df["ad_types_manual"].fillna("").str.strip() != EXPLANATORY]

    ids = sorted(df["comment_id"].astype(str))  # sorted first => deterministic
    if args.n > len(ids):
        raise SystemExit(f"requested n={args.n} but population has only {len(ids)} rows")
    chosen = random.Random(args.seed).sample(ids, args.n)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_order", "comment_id"])
        for i, cid in enumerate(chosen, start=1):
            w.writerow([i, cid])

    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input_file": str(args.input),
        "input_sha256": sha256(args.input),
        "input_rows": total_rows,
        "population": args.population,
        "population_rows": len(ids),
        "seed": args.seed,
        "n": args.n,
        "sample_csv": str(out),
        "sample_sha256": sha256(out),
        "python": platform.python_version(),
        "pandas": pd.__version__,
    }
    man_path = out.with_name("sample_manifest.json")
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {out} ({args.n} ids) and {man_path}")


if __name__ == "__main__":
    main()
