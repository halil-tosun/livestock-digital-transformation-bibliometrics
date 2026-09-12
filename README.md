# Social Dimensions in Livestock Digital Transformation: A Bibliometric and Adoption-Economics Analysis

**Authors:** Halil Tosun (ADA University) and Victor E. Cabrera (University of Wisconsin-Madison)

## Replication Package

This repository contains the complete replication package accompanying the
manuscript examining whether social-dimension research in livestock digital
transformation is structurally marginalised within the scientific literature
or simply rare in prevalence, combined with a synthesis of recent
adoption-economics evidence on precision livestock technologies.

---

## Repository Overview

This repository follows open science and computational reproducibility
principles and includes:

- Complete Python source code (bibliometric analysis, statistical tests, figures)
- R/Bibliometrix script (independent cross-validation, strategic map, thematic evolution)
- VOSviewer project files (independent cross-validation)
- Raw and filtered bibliometric datasets (Lens Scholarly Database export)
- Comprehensive documentation
- Software environment specifications

---

## Repository Structure

```text
Livestock_Digital_Transformation_Replication/
├── code/
│   ├── _paths.py                      # shared path configuration
│   ├── _keyword_utils.py              # shared keyword cleaning/network module
│   ├── 01_dataset_overview.py
│   ├── 02_leading_sources.py
│   ├── 03_citation_structure.py
│   ├── 04_citation_regression.py
│   ├── 05_keyword_network.py
│   ├── 06_statistical_tests.py
│   ├── 07_make_figures.py
│   └── run_all.py
├── r/
│   └── bibliometrix_reproduction.R
├── vosviewer/
│   ├── lens_for_vosviewer.ris
│   ├── vosviewer_network_thr5.txt
│   └── vosviewer_thesaurus.txt
├── data/
│   └── raw/
│       ├── lens-data-raw-7405.csv.gz
│       └── lens-data-filtered-2812.csv.gz
├── output/                            # generated tables (.csv)
├── figures/                           # generated figures (.png, 300 DPI)
├── docs/
│   ├── CODEBOOK.md
│   ├── DATA_DESCRIPTION.md
│   ├── REPRODUCIBILITY_CHECKLIST.md
│   └── Replication_Guide.md
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── .zenodo.json
├── LICENSE
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Documentation

- **docs/CODEBOOK.md** — analytical workflow and script-by-script description
- **docs/DATA_DESCRIPTION.md** — data sources and dataset structure
- **docs/REPRODUCIBILITY_CHECKLIST.md** — reproducibility checklist
- **docs/Replication_Guide.md** — complete replication guide

## Installation

```bash
conda env create -f environment.yml
conda activate livestock-digital-repro
```

or

```bash
pip install -r requirements.txt
```

## Run

```bash
cd code
python run_all.py
```

This reproduces the complete Python analytical workflow: dataset overview
and PRISMA screening verification, leading-source and citation-structure
descriptives, the citation-impact regression models (preliminary Poisson,
primary negative binomial — the only regression table retained in the
manuscript body — and log1p-OLS robustness check), the keyword
co-occurrence network and Louvain clustering, all formal statistical
significance tests, and Figures 1-2.

Expected runtime: 2-3 minutes on a standard laptop. The slowest step is
bootstrap resampling in the negative binomial regression.

Two further analyses are produced in separate software environments and
are not part of the Python pipeline. As of manuscript v2 (see CHANGELOG),
neither is embedded as a numbered figure in the manuscript body — both
are condensed into a single "Independent verification (VOSviewer and
R/Bibliometrix)" paragraph in the Results, with full outputs retained
here for transparency and reproducibility:

- **R/Bibliometrix** (`r/bibliometrix_reproduction.R`): independent
  cross-validation of the descriptive bibliometrics, Callon's strategic
  map, and the Sankey thematic-evolution diagram (`figures/`, not
  individually numbered in the manuscript).
- **VOSviewer** (`vosviewer/`): an independent, third cross-validation of
  the keyword co-occurrence network, producing the four Electronic
  Supplementary Material figures referenced in the manuscript as
  Fig. S1-S4 (`figures/supplementary_vosviewer/`).

## Script-to-Output Correspondence

**Manuscript table/figure numbers below refer to the current (v2) manuscript.**
Several tables present in manuscript v1 (the preliminary Poisson
regression, the log1p-OLS robustness regression, and the annual
document-count table) were condensed into one-sentence in-text summaries
during peer-review revision to keep the manuscript focused; the
underlying scripts and CSV outputs are unchanged and still reproduce
those results in full — see CHANGELOG.md for the full list of
manuscript-side condensations.

| Script | Produces |
|---|---|
| `01_dataset_overview.py` | Table 1 (PRISMA screening); dataset overview summary |
| `02_leading_sources.py` | Leading-sources table (with dataset-specific h-index) |
| `03_citation_structure.py` | Top-cited documents table (including the rank-9/10 citation tie) |
| `04_citation_regression.py` | Preliminary Poisson and log1p-OLS robustness regressions (both summarised in-text only in the manuscript, full tables in `output/`); primary negative binomial regression (manuscript Table 2) |
| `05_keyword_network.py` | Keyword co-occurrence network, threshold-sensitivity table, Louvain cluster assignments |
| `06_statistical_tests.py` | Annual growth test, within-cluster percentile test (manuscript Table 4), five-year-bin prevalence test (manuscript Table 5), Benjamini-Hochberg correction — all summarised in manuscript Table 3 |
| `07_make_figures.py` | Fig. 1 (keyword network), Fig. 2 (annual growth) |
| `r/bibliometrix_reproduction.R` | Independent cross-check of sections above; Callon's strategic map and the Sankey thematic-evolution diagram (full images in `figures/`, condensed to one paragraph in the manuscript body) |
| `vosviewer/` | Independent cross-check of the keyword network; manuscript Fig. S1-S4 (Electronic Supplementary Material) |

**Note on the adoption-economics evidence table (manuscript Table 6):**
the table summarising eight peer-reviewed studies on precision
livestock/agriculture adoption economics is a manually compiled
narrative literature synthesis, not a computational output — there is no
script that generates it. Its search-and-selection protocol is
documented in the manuscript's Methods section, and the table itself,
with full source citations, appears in the manuscript's Results section
on the adoption-economics synthesis.

## Known, Documented Discrepancies

This package was built with a "verify everything, disclose everything"
principle. Minor discrepancies between tools are documented rather than
silently resolved:

1. **Unique-source count.** A case-sensitive Python count gives 370 unique
   journal sources; R/Bibliometrix, after normalising journal-name case
   variants (e.g., "Journal of Animal Science" vs "JOURNAL OF ANIMAL
   SCIENCE"), gives 355. A simple case-insensitive grouping in Python
   (`02_leading_sources.py`) gives 356 — a one-source residual discrepancy
   likely caused by a near-duplicate journal-name variant not merged by
   simple lowercasing (e.g. trailing punctuation).
2. **Rank-9/10 citation tie.** Two documents are tied at exactly 747
   citations. `03_citation_structure.py` reports both explicitly rather
   than resolving the tie by an arbitrary sort order.
3. **Rank-~10 source-count tie.** Two journals are tied at exactly 36
   documents; both are disclosed in `02_leading_sources.py`'s output.
4. **Louvain cluster-count determinism.** Node/edge insertion order must
   be sorted (`_keyword_utils.build_network`) for Louvain clustering to
   return a deterministic result; without this, Python's per-process
   string-hash randomisation causes the cluster count to vary
   non-deterministically across runs.
5. **Preliminary Poisson model z-statistics.** This package's
   `output/regression_poisson_preliminary.csv` reports z-statistics that
   differ by a small margin (≤0.1) from an earlier full Poisson
   regression table that appeared in manuscript v1. As of manuscript v2,
   the preliminary Poisson model is summarised in-text only (reporting
   solely the Pearson dispersion statistic, 140.9, that motivates the
   primary negative binomial model), so this z-statistic discrepancy no
   longer affects any manuscript-reported number; it is retained here
   for full transparency about the underlying computational output. The
   coefficients, incidence rate ratios, and bootstrap confidence
   intervals for the primary (negative binomial) model are unaffected
   and match exactly.

## Citation

Please cite both the published article and this archived repository.
Citation metadata are provided in `CITATION.cff` and `.zenodo.json`.

## License

MIT License (code). The underlying bibliometric data were retrieved from
the Lens Scholarly Database (https://www.lens.org) under its terms of use
for research purposes; see `docs/DATA_DESCRIPTION.md`.

## Contact

**Halil Tosun** (corresponding author)
ADA University, Department of Animal Science, Baku, Azerbaijan
ORCID: https://orcid.org/0000-0001-5117-0390
Email: halilibrahimtosun@gmail.com

**Victor E. Cabrera**
University of Wisconsin-Madison, Department of Animal and Dairy Sciences, USA
ORCID: https://orcid.org/0000-0003-1739-7457
Email: vcabrera@wisc.edu

**Version:** 2.0.0
**Zenodo DOI:** To be assigned after public release.
