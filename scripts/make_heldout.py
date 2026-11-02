"""Event A: list the gold-file comment ids NOT used in the M2 sample (held-out rows).

  python3 scripts/make_heldout.py --input data/raw/gold_standard_saad_comments.xlsx
"""
import argparse
import csv

import pandas as pd

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--input", required=True)
ap.add_argument("--used", default="data/sample_ids.csv")
ap.add_argument("--out", default="data/eventA_ids.csv")
args = ap.parse_args()

df = pd.read_excel(args.input, dtype=str)
all_ids = sorted(set(df["comment_id"].dropna()))
with open(args.used, newline="", encoding="utf-8") as f:
    used = {r["comment_id"] for r in csv.DictReader(f)}
held = [i for i in all_ids if i not in used]

with open(args.out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["sample_order", "comment_id"])
    for n, cid in enumerate(held, 1):
        w.writerow([n, cid])

print(f"gold file ids: {len(all_ids)}  used in M2: {len(used)}  held-out: {len(held)}")
