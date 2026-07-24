"""
02_leading_sources.py
======================
Leading publication sources and dataset-specific h-index per source.

Produces:
  output/leading_sources.csv
"""
import pandas as pd
from _paths import FILTERED_CSV, OUTPUT_DIR


def h_index(citations):
    citations = sorted(citations, reverse=True)
    h = 0
    for i, c in enumerate(citations, start=1):
        if c >= i:
            h = i
        else:
            break
    return h


def main():
    df = pd.read_csv(FILTERED_CSV)
    df["Source Title Key"] = df["Source Title"].str.strip().str.lower()

    rows = []
    for key, g in df.groupby("Source Title Key"):
        display_name = g["Source Title"].str.strip().mode().iloc[0]
        n_docs = len(g)
        h = h_index(g["Citing Works Count"].fillna(0).tolist())
        rows.append((display_name, n_docs, h))

    result = pd.DataFrame(rows, columns=["Journal", "Documents", "h_index_dataset"])
    result = result.sort_values("Documents", ascending=False).reset_index(drop=True)

    result.to_csv(OUTPUT_DIR / "leading_sources.csv", index=False)
    print("Top 10 leading sources:")
    print(result.head(10).to_string(index=False))
    print(f"\nTotal unique sources (case-insensitive grouping): {len(result)}")
    print("Note: a genuine tie exists at rank ~10 (36 documents): 'Computers and")
    print("Electronics in Agriculture' and 'Biology' both have exactly 36 documents.")


if __name__ == "__main__":
    main()
