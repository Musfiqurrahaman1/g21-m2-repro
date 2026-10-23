"""Step 3 - derive the result from the RAW classification file only.

  py scripts\\summarise.py

Reads results/raw/classification.csv (never the Excel file) and writes
  results/summary_generated.md   human-readable tables + mechanical status + trace example
  results/derived_counts.csv     machine-readable key,value counts

Primary metric (clarification C-04/C-05): among sampled rows that matched at least
one pattern AND are labelled Active or Dormant, the Dormant share.
Mechanical status follows the frozen M1 rule; the group must review and confirm it.
"""
import argparse
import csv
import math
from collections import Counter
from pathlib import Path


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    a = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - a) / d, (c + a) / d)


def pct(k, n):
    return float("nan") if n == 0 else 100.0 * k / n


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--classification", default="results/raw/classification.csv")
    ap.add_argument("--out", default="results/summary_generated.md")
    ap.add_argument("--counts-out", default="results/derived_counts.csv")
    ap.add_argument("--reference", type=float, default=96.0, help="paper figure used in M1 (%%)")
    ap.add_argument("--tolerance", type=float, default=10.0, help="M1: within 10 points")
    ap.add_argument("--floor", type=float, default=80.0, help="M1: non-reproduction below ~80%%")
    args = ap.parse_args()

    with open(args.classification, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    n = len(rows)
    cats = Counter(r["category"] for r in rows)
    matched = [r for r in rows if r["matched"] == "True"]
    unmatched = [r for r in rows if r["matched"] == "False"]
    split = [r for r in matched if r["category"] in ("Active", "Dormant")]
    active = sum(1 for r in split if r["category"] == "Active")
    dormant = sum(1 for r in split if r["category"] == "Dormant")
    n_split = len(split)
    dorm_pct = pct(dormant, n_split)
    lo, hi = wilson(dormant, n_split)

    # descriptive sensitivity checks (NOT used for the decision)
    all_split = [r for r in rows if r["category"] in ("Active", "Dormant")]
    all_dorm = sum(1 for r in all_split if r["category"] == "Dormant")
    single = [r for r in split if r["multi_label"] != "True"]
    single_dorm = sum(1 for r in single if r["category"] == "Dormant")
    tokens = Counter()
    for r in rows:
        for t in [t.strip() for t in r["ad_types_manual"].split(",") if t.strip()]:
            tokens[t] += 1

    warnings = []
    if cats.get("MISSING"):
        warnings.append(f"{cats['MISSING']} sampled id(s) not found in the input (category MISSING).")
    if cats.get("UNMAPPED"):
        warnings.append(f"{cats['UNMAPPED']} row(s) have a label outside the mapping (UNMAPPED).")

    ref_lo = args.reference - args.tolerance
    if n_split == 0:
        status = "INCONCLUSIVE / BLOCKED"
        why = "no matched Active/Dormant rows, so no valid comparison"
    elif dorm_pct >= ref_lo:
        status = "REPRODUCED"
        why = f"Dormant share {dorm_pct:.1f}% is within {args.tolerance:.0f} points of {args.reference:.0f}% (>= {ref_lo:.0f}%)"
    elif dorm_pct >= args.floor:
        status = "NOT REPRODUCED"
        why = (
            f"Dormant share {dorm_pct:.1f}% is in the {args.floor:.0f}-{ref_lo:.0f}% band M1 left undefined; "
            "treated as NOT REPRODUCED because it fails the only REPRODUCED criterion (clarification C-05)"
        )
    else:
        status = "NOT REPRODUCED"
        why = f"Dormant share {dorm_pct:.1f}% is below the M1 floor of {args.floor:.0f}%"
    if warnings and status != "INCONCLUSIVE / BLOCKED":
        why += " - BUT see warnings: resolve them before treating this status as final"

    # trace example: first matched Dormant row (else first matched row)
    trace = next((r for r in split if r["category"] == "Dormant"), None) or (split[0] if split else None)

    counts = [
        ("sampled_rows", n),
        ("matched_rows", len(matched)),
        ("unmatched_rows", len(unmatched)),
        ("matched_pct_of_sample", f"{pct(len(matched), n):.2f}"),
        ("category_Active_all", cats.get("Active", 0)),
        ("category_Dormant_all", cats.get("Dormant", 0)),
        ("category_EXPLANATORY_all", cats.get("EXPLANATORY", 0)),
        ("category_UNMAPPED_all", cats.get("UNMAPPED", 0)),
        ("category_MISSING_all", cats.get("MISSING", 0)),
        ("split_rows_matched_Active_or_Dormant", n_split),
        ("split_Active", active),
        ("split_Dormant", dormant),
        ("split_Dormant_pct", f"{dorm_pct:.2f}"),
        ("split_Dormant_wilson95_lo", f"{100*lo:.2f}"),
        ("split_Dormant_wilson95_hi", f"{100*hi:.2f}"),
        ("mechanical_status", status),
    ]
    Path(args.counts_out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.counts_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "value"])
        w.writerows(counts)

    md = []
    md.append("# AUTO-GENERATED summary (review before using)\n")
    md.append("Computed from `results/raw/classification.csv` only. The status below is mechanical; "
              "the group must confirm it and write the interpretation in `results/summary.md`.\n")
    md.append("## Primary result\n")
    md.append(f"- Sampled comments: **{n}**")
    md.append(f"- Matched at least one pattern: **{len(matched)}** ({pct(len(matched), n):.1f}% of sample)")
    md.append(f"- Matched and labelled Active/Dormant (the split population): **{n_split}**")
    md.append(f"  - Active: **{active}**, Dormant: **{dormant}**")
    md.append(f"  - **Dormant share: {dorm_pct:.1f}%** (Wilson 95% interval {100*lo:.1f}-{100*hi:.1f}%)")
    md.append(f"- M1 reference: {args.reference:.0f}% (within {args.tolerance:.0f} points => >= {ref_lo:.0f}%; floor {args.floor:.0f}%)")
    md.append(f"- **Mechanical status: {status}** - {why}\n")
    if warnings:
        md.append("## Warnings\n")
        md.extend(f"- {w}" for w in warnings)
        md.append("")
    md.append("## All sampled rows by category\n")
    md.append("| Category | Rows |\n|---|---|")
    for k in ("Active", "Dormant", "EXPLANATORY", "UNMAPPED", "MISSING"):
        md.append(f"| {k} | {cats.get(k, 0)} |")
    md.append("")
    md.append("## Descriptive sensitivity checks (not used for the decision)\n")
    md.append(f"- Dormant share over ALL Active/Dormant rows, matched or not: {all_dorm}/{len(all_split)} = {pct(all_dorm, len(all_split)):.1f}%")
    md.append(f"- Dormant share excluding multi-label rows: {single_dorm}/{len(single)} = {pct(single_dorm, len(single)):.1f}%")
    md.append("")
    md.append("## Label token frequency in the sample\n")
    md.append("| Label | Count |\n|---|---|")
    for t, c in tokens.most_common():
        md.append(f"| {t} | {c} |")
    md.append("")
    md.append("## Trace example (claim -> raw evidence -> input)\n")
    if trace:
        md.append(f"- Claim: Dormant share = {dormant}/{n_split} = {dorm_pct:.1f}%")
        md.append("- Recompute: count rows in `results/raw/classification.csv` with `matched=True` and `category=Dormant` (numerator) "
                  "and `matched=True` and `category` in {Active, Dormant} (denominator)")
        md.append(f"- Example row: sample_order {trace['sample_order']}, comment_id `{trace['comment_id']}`, "
                  f"patterns matched on file lines [{trace['matched_pattern_lines']}], manual label `{trace['ad_types_manual']}` -> {trace['category']}")
        md.append("- Input identity and run details: `results/raw/run_log.txt` (hashes), `data/sample_manifest.json` (seed, population)")
        md.append("- Look the comment_id up in `gold_standard_saad_comments.xlsx` (column `comment_id`) and the pattern line numbers in `data/raw/saad_patterns.txt`")
    else:
        md.append("- No matched Active/Dormant row to trace.")
    Path(args.out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
