# REPRODUCIBILITY_CHECKLIST

## Study
**Beyond Technology: Understanding Sustainable Livestock Digital Transformation through Adoption Economics and Evidence Synthesis**

---

## Reproducibility Status

| Item | Status |
|------|:------:|
| Source code included (Python) | ✓ |
| Source code included (R) | ✓ |
| VOSviewer project files included | ✓ |
| Raw data included | ✓ |
| Filtered/analytical dataset reproducible from raw data | ✓ |
| README provided | ✓ |
| CODEBOOK provided | ✓ |
| Data documentation provided | ✓ |
| Software dependencies documented | ✓ |
| Conda environment provided | ✓ |
| License provided | ✓ |
| Citation metadata (CITATION.cff, .zenodo.json) | ✓ |
| One-command workflow (`run_all.py`) | ✓ |
| Figures reproducible (300 DPI) | ✓ |
| Tables reproducible | ✓ |
| Deterministic clustering (sorted node/edge insertion order) | ✓ |
| Open repository planned | ✓ |
| Zenodo DOI | ✓ |

**Zenodo DOI:** https://doi.org/10.5281/zenodo.21541502

---

## Computational Environment

- Python environment documented in `environment.yml`
- Package list documented in `requirements.txt`
- Python version tested: 3.12
- R version tested: 4.6.1, with the current CRAN release of `bibliometrix`
- VOSviewer version tested: 1.6.21
- Expected Python runtime: 2-3 minutes on a standard laptop

---

## Expected Workflow

1. Create the Python environment (`conda env create -f environment.yml` or
   `pip install -r requirements.txt`).
2. Run `python code/run_all.py`.
3. Verify that all tables appear in `output/` and Figures 1-2 appear in
   `figures/` at 300 DPI.
4. Cross-check reported values against the manuscript's tables and figures
   (see `docs/CODEBOOK.md` for the full script-to-output correspondence).
5. For Figures 3-4, open `r/bibliometrix_reproduction.R` in R/RStudio (or
   Posit Cloud) and run interactively; `thematicEvolution()`'s Sankey
   output renders in the Viewer pane, not the Plots pane.
6. For the Appendix figures, import `vosviewer/lens_for_vosviewer.ris`
   into VOSviewer (Lens tab), set the minimum-occurrence threshold to 5,
   and locate the four social-dimension keywords individually.

---

## Internal Consistency Checks

The following results are computed by more than one script, or in more
than one independent software environment, and should match (or be
explicitly reconciled where they do not — see the Known Discrepancies
section of the main README):

| Quantity | Computed in | Cross-checked in |
|---|---|---|
| Unique authors (14,330) | `01_dataset_overview.py` | `r/bibliometrix_reproduction.R` |
| Unique sources (355/370/356) | `01_dataset_overview.py`, `02_leading_sources.py` | `r/bibliometrix_reproduction.R` |
| Keyword network at threshold 5 (560 items, 12,790 links) | `05_keyword_network.py` | `r/bibliometrix_reproduction.R` |
| Keyword network (independent software/preprocessing) | `05_keyword_network.py` | `vosviewer/` |
| Top-cited documents and rank-9/10 tie | `03_citation_structure.py` | `r/bibliometrix_reproduction.R` |
| Louvain cluster count (6) | `05_keyword_network.py` | -- (see determinism note in README) |

---

## Transparency Statement

This repository has been prepared to maximise computational reproducibility and long-term accessibility. Minor cross-tool discrepancies (source-count normalisation, a genuine citation tie, and Louvain clustering determinism) are documented explicitly in the main README rather than being silently resolved.

This release has been permanently archived on Zenodo and assigned the following DOI:

**Zenodo DOI:** https://doi.org/10.5281/zenodo.21541502

The archived Zenodo record serves as the citable, immutable version of the reproducibility package accompanying the manuscript.
