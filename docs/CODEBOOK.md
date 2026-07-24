# CODEBOOK

## Analytical Workflow

This document describes each script in `../code/` in the order they should
be run (or via `run_all.py`, which runs them in this order automatically).

---

### `_paths.py`
Shared path configuration. Defines `DATA_DIR`, `OUTPUT_DIR`, `FIG_DIR`, and
creates the output directories if they do not exist. Every numbered script
imports this module so the package runs identically regardless of the
working directory it is launched from.

### `_keyword_utils.py`
Shared keyword-cleaning, harmonisation, and network-construction module.
This is the single source of truth for keyword processing — every table
and figure depending on the keyword network uses these exact functions.
Combines the `Keywords` and `MeSH Terms` fields, lowercases and strips
digit artefacts, removes generic demographic checktags (male/female/human),
and applies a small harmonisation dictionary merging near-synonymous terms
(e.g. "artificial intelligence" → "ai"). Network construction inserts
nodes and edges in sorted order to guarantee deterministic Louvain
clustering (see the Known Discrepancies section of the main README).

### `01_dataset_overview.py`
Loads the raw (7,405-record) and filtered (2,812-record) datasets, verifies
the filtered set is a subset of the raw set, reconstructs the PRISMA
screening table, and computes dataset-overview descriptives (unique
authors, single-authored documents, average citations, average document
age).

### `02_leading_sources.py`
Groups documents by journal (case-insensitive) and computes a
dataset-specific h-index per journal using each journal's own citation
distribution within this dataset.

### `03_citation_structure.py`
Ranks documents by citation count (stable sort: citations descending, then
title alphabetical) and reports the top 12 most-cited documents, explicitly
flagging the genuine tie at rank 9/10 (747 citations each).

### `04_citation_regression.py`
Fits three citation-impact regression models on the same covariate set
(centred publication year, open-access status, digital-technology keyword
presence, social-dimension keyword presence):
1. A preliminary Poisson regression (diagnostic only) — reports the Pearson
   dispersion statistic that motivates the primary model.
2. The primary negative binomial (NB2) regression, fit by maximum
   likelihood with the dispersion parameter estimated jointly with the
   mean-structure coefficients, with bootstrap standard errors.
3. A log1p-transformed OLS regression as a robustness check.

Runtime: ~1-2 minutes (bootstrap resampling for the NB model, 300 resamples).

### `05_keyword_network.py`
Builds the keyword co-occurrence network at the main analysis threshold
(minimum occurrence = 5), with a sensitivity check at thresholds 3 and 10.
Runs Louvain community detection (seeded, with sorted insertion order for
determinism) and reports cluster assignments and node-level total link
strength.

### `06_statistical_tests.py`
Runs the formal inferential tests:
- **Test 1**: OLS regression of annual document count on publication year
  (2000-2025, excluding the partial year 2026).
- **Test 2**: One-sample Wilcoxon signed-rank test of each social-dimension
  keyword's within-cluster percentile rank (using the Louvain partition
  from `05_keyword_network.py`) against the null of a 50th-percentile rank.
  This design avoids the circularity of comparing investigator-selected
  keyword groups directly, since cluster membership is assigned by an
  unsupervised algorithm blind to any social/core labelling.
- **Test 3**: Separate linear probability models for digital-technology and
  social-dimension keyword prevalence over time, with a bootstrap 95%
  confidence interval (2,000 resamples) for the difference in slopes, plus
  a five-year-bin prevalence breakdown.
- **Benjamini-Hochberg correction** across the primary hypothesis tests
  (Tests 1-4) to control the false discovery rate.

### `07_make_figures.py`
Generates Figure 1 (keyword co-occurrence network, Louvain clusters
coloured) and Figure 2 (annual publication output) at 300 DPI.

### `run_all.py`
Runs all seven numbered scripts in sequence and prints a summary of total
runtime. Each script can also be run individually to regenerate a single
table or figure.

---

## R and VOSviewer Components

### `../r/bibliometrix_reproduction.R`
Independently rebuilds the same keyword-cleaned dataset in R and cross-
validates the descriptive bibliometrics against the Python output. Also
produces Callon's strategic (thematic) map (Figure 3) and the Sankey
thematic-evolution diagram (Figure 4) using bibliometrix's `thematicMap()`
and `thematicEvolution()` functions — analyses that require R/Bibliometrix
specifically and are not available in the Python pipeline.

### `../vosviewer/`
Contains a pre-cleaned, harmonised RIS file (`lens_for_vosviewer.ris`) for
direct VOSviewer import, a pre-computed network file
(`vosviewer_network_thr5.txt`) as a guaranteed-working fallback, and a
synonym/harmonisation thesaurus file. VOSviewer provides a third,
fully independent cross-validation of the keyword co-occurrence network
(different software, different clustering algorithm, no shared
preprocessing code with the Python or R pipelines), producing the four
Appendix figures.

## A Note on the Adoption-Economics Evidence Table

The manuscript's table summarising eight peer-reviewed studies on
precision livestock/agriculture adoption economics is a manually
compiled narrative literature synthesis, not a computational output of
this repository — no script generates it. Its search-and-selection
protocol is documented in the manuscript's Methods section (adoption-
economics literature synthesis).
