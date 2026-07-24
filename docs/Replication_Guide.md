# Replication Guide

This guide walks through reproducing every table and figure in the
manuscript from scratch.

## Step 1 — Set up the computational environment

```bash
git clone <repository-url>
cd Livestock_Digital_Transformation_Replication
conda env create -f environment.yml
conda activate livestock-digital-repro
```

If you prefer pip:

```bash
pip install -r requirements.txt
```

## Step 2 — Run the Python pipeline

```bash
cd code
python run_all.py
```

This single command reproduces:
- Table 1 (PRISMA screening) and the dataset-overview summary
- The leading-sources table (with dataset-specific h-index)
- The top-cited-documents table (including the rank-9/10 citation tie)
- All three citation-regression models (preliminary Poisson, primary
  negative binomial, log1p-OLS robustness)
- The keyword co-occurrence network, threshold-sensitivity analysis, and
  Louvain cluster assignments
- All formal statistical significance tests (annual growth, within-cluster
  centrality, prevalence divergence) with Benjamini-Hochberg correction
- Figures 1 and 2 (300 DPI)

Every script prints its output to the console for immediate comparison
against the manuscript, in addition to saving `.csv` files to `../output/`
and `.png` files to `../figures/`.

To regenerate a single table or figure, run its script directly, e.g.:

```bash
python 04_citation_regression.py
```

## Step 3 — Reproduce the R/Bibliometrix cross-check (Figures 3-4)

1. Install R (tested on 4.6.1) and the required packages:
   ```r
   install.packages(c("bibliometrix", "dplyr", "stringr"))
   ```
   Posit Cloud (https://posit.cloud) requires no local installation and was
   used to develop and test this script.
2. Open `r/bibliometrix_reproduction.R` and run it from the `r/` directory
   (so the relative path to `../data/raw/lens-data-filtered-2812.csv.gz`
   resolves correctly), or adjust the path at the top of the script.
3. Sections 4-5 of the script reproduce the descriptive bibliometrics and
   keyword network for cross-validation against the Python output.
4. Section 6 produces Callon's strategic map (Figure 3); save it with
   `ggsave()` or the RStudio Plots-pane export button.
5. Section 7 produces the Sankey thematic-evolution diagram (Figure 4).
   This renders as an interactive HTML widget in the RStudio/Posit
   **Viewer** pane (not the Plots pane) — use the Viewer pane's own
   "Export > Save as Image" button, or take a screenshot directly.

## Step 4 — Reproduce the VOSviewer cross-check (Appendix Figures A1-A4)

1. Download and install VOSviewer (free, https://www.vosviewer.com).
2. Open VOSviewer and choose "Create a map based on bibliographic data."
3. Select the **Lens** tab (not Web of Science) and import
   `vosviewer/lens_for_vosviewer.ris`.
4. Set the co-occurrence analysis type to "All keywords," counting
   method "Full counting," and minimum number of occurrences of a
   keyword to **5**.
5. Optionally load `vosviewer/vosviewer_thesaurus.txt` as a thesaurus file
   to apply the same harmonisation rules used in the Python/R pipelines.
6. Once the network renders, zoom to each of the four social-dimension
   keywords individually (farmers, technology, policy, socioeconomic
   factors) and take a screenshot of each zoomed view — these correspond
   to Appendix Figures A1-A4.
7. Alternatively, `vosviewer/vosviewer_network_thr5.txt` is a pre-computed
   network file that can be opened directly in VOSviewer as a
   guaranteed-working fallback if the RIS import behaves differently in
   a newer VOSviewer version.

## Step 5 — Cross-check results

Compare the console output and generated files against the manuscript's
tables and figures using the correspondence table in `docs/CODEBOOK.md`.
Any discrepancy beyond those explicitly documented in the main README's
"Known, Documented Discrepancies" section should be reported as an issue
in the repository.

## Troubleshooting

- **R column names differ from those referenced in the script**: R's
  `read.csv()` can convert column names differently depending on R/readr
  version (e.g., "MeSH Terms" → "MeSH.Terms"). Run `colnames(raw)` and
  adjust the script's column references accordingly.
- **Louvain cluster count differs from 6**: confirm you are using the
  `_keyword_utils.py` module as provided, which sorts node/edge insertion
  order before clustering. Without this, the result becomes sensitive to
  Python's per-process string-hash randomisation (see the main README).
- **VOSviewer version differences**: if the RIS import behaves
  unexpectedly in a newer VOSviewer release, use the pre-computed
  `vosviewer_network_thr5.txt` file instead.
