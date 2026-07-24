"""
01_dataset_overview.py
=======================
Dataset overview and PRISMA screening verification.

Produces:
  output/Table1_prisma_screening.csv
  output/dataset_overview_summary.csv
"""
import pandas as pd
from _paths import RAW_CSV, FILTERED_CSV, OUTPUT_DIR

CURRENT_YEAR = 2026


def main():
    raw = pd.read_csv(RAW_CSV)
    filt = pd.read_csv(FILTERED_CSV)

    raw_ids = set(raw["Lens ID"])
    filt_ids = set(filt["Lens ID"])
    assert filt_ids.issubset(raw_ids), "Filtered set is not a subset of the raw set"

    prisma = pd.DataFrame([
        {"Stage": "Identification", "Records": len(raw), "Excluded": None, "Reason": None},
        {"Stage": "Duplicate removal", "Records": len(raw), "Excluded": 0, "Reason": "No duplicates"},
        {"Stage": "Title/abstract screening", "Records": 2867, "Excluded": 4538, "Reason": "Irrelevant thematic scope"},
        {"Stage": "Eligibility assessment", "Records": len(filt), "Excluded": 55, "Reason": "Incomplete metadata"},
        {"Stage": "Final filtering (document type)", "Records": len(filt), "Excluded": 0, "Reason": "All confirmed journal articles"},
    ])
    prisma.to_csv(OUTPUT_DIR / "Table1_prisma_screening.csv", index=False)
    print("Table 1. PRISMA-guided literature screening")
    print(prisma.to_string(index=False))

    def split_authors(s):
        if pd.isna(s):
            return []
        return [a.strip() for a in str(s).split(";") if a.strip()]

    all_authors = filt["Author/s"].apply(split_authors)
    author_counts = {}
    for lst in all_authors:
        for a in lst:
            author_counts[a] = author_counts.get(a, 0) + 1

    raw_source_count = filt["Source Title"].nunique()
    avg_age = (CURRENT_YEAR - filt["Publication Year"]).mean()

    summary = pd.DataFrame([{
        "total_documents": len(filt),
        "unique_sources_case_sensitive": raw_source_count,
        "unique_authors": len(author_counts),
        "single_authored_documents": int((all_authors.apply(len) == 1).sum()),
        "avg_citations_per_document": round(filt["Citing Works Count"].mean(), 2),
        "avg_document_age_years": round(avg_age, 2),
    }])
    summary.to_csv(OUTPUT_DIR / "dataset_overview_summary.csv", index=False)
    print("\nDataset overview summary")
    print(summary.to_string(index=False))
    print("\nNote: unique-source count above is case-sensitive (370). The manuscript's")
    print("reported figure of 355 sources reflects case-normalisation performed in the")
    print("R/Bibliometrix cross-check (see ../r/bibliometrix_reproduction.R).")


if __name__ == "__main__":
    main()
