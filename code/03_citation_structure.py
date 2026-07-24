"""
03_citation_structure.py
==========================
Top-cited documents, including the genuine citation tie at rank 9/10.
Tie handling: citations descending, then title alphabetical (stable
sort) -- the tie is reported explicitly rather than resolved silently.

Produces:
  output/top_cited_documents.csv
"""
import pandas as pd
from _paths import FILTERED_CSV, OUTPUT_DIR


def main():
    df = pd.read_csv(FILTERED_CSV)
    df_sorted = df.sort_values(["Citing Works Count", "Title"], ascending=[False, True], kind="mergesort")

    top12 = df_sorted[["Title", "Author/s", "Publication Year", "Citing Works Count"]].head(12)
    top12.to_csv(OUTPUT_DIR / "top_cited_documents.csv", index=False)

    print("Top-cited documents:")
    print(top12.to_string(index=False))

    tied = df[df["Citing Works Count"] == 747]
    print(f"\n{len(tied)} documents share exactly 747 citations (rank 9/10 tie):")
    print(tied[["Title", "Publication Year", "Citing Works Count"]].to_string(index=False))


if __name__ == "__main__":
    main()
