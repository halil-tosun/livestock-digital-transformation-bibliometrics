"""
build_relevance_filter.py
==========================
Post-hoc, reproducible corpus-relevance safeguard added during peer
review. Flags records in the primary 2,812-document corpus that contain
no livestock- or species-specific term anywhere in Title, Abstract,
Keywords, MeSH Terms, or Fields of Study, and writes the reduced corpus
used for the sensitivity re-analysis reported in the manuscript
("Corpus relevance robustness check").

This filter is NOT used to redefine the primary dataset -- it is a
transparency/robustness check only. The original 2,812-document corpus
remains the dataset used throughout the primary analyses.
"""
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data" / "raw"

LIVESTOCK_PATTERN = re.compile(
    r"livestock|dairy|cattle|poultry|farm|pig|swine|sheep|goat|animal|"
    r"veterinar|herd|equine|aquacultur|bovine|ovine|porcine|avian|"
    r"ruminant|broiler|layer hen|buffalo|calv|milk|meat|hen\b|cow\b|"
    r"horse|beef|lamb|goose|duck|rabbit|hog",
    re.IGNORECASE,
)

FIELDS = ["Title", "Abstract", "Keywords", "MeSH Terms", "Fields of Study"]


def has_livestock_signal(row) -> bool:
    text = " ".join(str(row.get(f, "")) for f in FIELDS)
    return bool(LIVESTOCK_PATTERN.search(text))


def main():
    src = DATA_DIR / "lens-data-filtered-2812.csv.gz"
    df = pd.read_csv(src)
    df["relevant"] = df.apply(has_livestock_signal, axis=1)

    n_excluded = int((~df["relevant"]).sum())
    print(f"Total records: {len(df)}")
    print(f"Excluded (no livestock/species signal): {n_excluded} "
          f"({100 * n_excluded / len(df):.1f}%)")

    kept = df[df["relevant"]].drop(columns=["relevant"])
    out = DATA_DIR / "lens-data-filtered-2514.csv.gz"
    kept.to_csv(out, index=False, compression="gzip")
    print(f"Wrote {len(kept)} records to {out}")


if __name__ == "__main__":
    main()
