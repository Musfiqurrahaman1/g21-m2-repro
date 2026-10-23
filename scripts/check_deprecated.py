import pandas as pd, sys
path = r"data\raw\gold_standard_saad_comments.xlsx"
df = pd.read_excel(path)
c = df["cleaned_comment"].astype(str)
lines = []
lines.append("file: " + path)
lines.append("rows: " + str(len(df)))
for term in ["@deprecated", "deprecated"]:
    n = int(c.str.contains(term, case=False, regex=False).sum())
    lines.append("rows containing " + repr(term) + ": " + str(n))
sample = pd.read_csv(r"data\sample_ids.csv")
id_col = "comment_id" if "comment_id" in df.columns else df.columns[0]
sub = df[df[id_col].isin(sample["comment_id"])]
cs = sub["cleaned_comment"].astype(str)
lines.append("sampled rows: " + str(len(sub)))
lines.append("sampled rows containing '@deprecated': " + str(int(cs.str.contains("@deprecated", case=False, regex=False).sum())))
text = "\n".join(lines)
print(text)
open(r"results\checks\deprecated_check.txt", "w").write(text + "\n")
