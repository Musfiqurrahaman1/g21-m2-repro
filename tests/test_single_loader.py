'''Event B design check: pandas' Excel reader is called from ONE place, common.load_gold_table.

Run from the project folder:  python tests/test_single_loader.py
Synthetic data only. This is a design check, not a study result.
'''
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from common import load_gold_table  # noqa: E402

def check_single_call_site():
    offenders = []
    for p in sorted((ROOT / "scripts").glob("*.py")):
        if p.name == "common.py":
            continue
        if "read_excel" in p.read_text(encoding="utf-8"):
            offenders.append(p.name)
    assert not offenders, "read_excel found outside common.py: " + str(offenders)

def check_loader_reads_text():
    import openpyxl
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "tiny.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["comment_id", "cleaned_comment", "ad_types_manual"])
        ws.append(["00123", "old code, deprecated", "current_deprecation"])
        wb.save(path)
        df = load_gold_table(path)
    assert list(df.columns) == ["comment_id", "cleaned_comment", "ad_types_manual"]
    assert df.loc[0, "comment_id"] == "00123"

def check_loader_failure_is_one_place():
    import pandas as pd
    original = pd.read_excel
    def removed(*args, **kwargs):
        raise AttributeError("simulated: read_excel removed")
    pd.read_excel = removed
    try:
        try:
            load_gold_table("anything.xlsx")
        except AttributeError as exc:
            assert "simulated" in str(exc)
        else:
            raise AssertionError("loader did not call pandas.read_excel")
    finally:
        pd.read_excel = original

if __name__ == "__main__":
    check_single_call_site()
    check_loader_reads_text()
    check_loader_failure_is_one_place()
    print("PASS: single loader design check (synthetic data, not a study result)")
