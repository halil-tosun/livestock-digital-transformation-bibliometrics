# Beyond Technology: Understanding Sustainable Livestock Digital Transformation through Adoption Economics and Evidence Synthesis

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
primary negative binomial, log1p-OLS robustness check), the keyword
co-occurrence network and Louvain clustering, all formal statistical
significance tests, and Figures 1-2.

Expected runtime: 2-3 minutes on a standard laptop. The slowest step is
bootstrap resampling in the negative binomial regression.

Two further analyses are produced in separate software environments and
are not part of the Python pipeline:

- **R/Bibliometrix** (`r/bibliometrix_reproduction.R`): independent
  cross-validation of the descriptive bibliometrics, Callon's strategic
  map (Figure 3), and the Sankey thematic-evolution diagram (Figure 4).
- **VOSviewer** (`vosviewer/`): an independent, third cross-validation of
  the keyword co-occurrence network, producing the four Appendix figures
  (`figures/appendix_vosviewer/`).

## Script-to-Output Correspondence

| Script | Produces |
|---|---|
| `01_dataset_overview.py` | Table 1 (PRISMA screening); dataset overview summary |
| `02_leading_sources.py` | Leading-sources table (with dataset-specific h-index) |
| `03_citation_structure.py` | Top-cited documents table (including the rank-9/10 citation tie) |
| `04_citation_regression.py` | Preliminary Poisson, primary negative binomial, and log1p-OLS robustness regression tables |
| `05_keyword_network.py` | Keyword co-occurrence network, threshold-sensitivity table, Louvain cluster assignments |
| `06_statistical_tests.py` | Annual growth test, within-cluster percentile test, five-year-bin prevalence test, Benjamini-Hochberg correction |
| `07_make_figures.py` | Figure 1 (keyword network), Figure 2 (annual growth) |
| `r/bibliometrix_reproduction.R` | Independent cross-check of Sections above; Figure 3 (Callon map); Figure 4 (Sankey thematic evolution) |
| `vosviewer/` | Independent cross-check of the keyword network; Appendix Figures A1-A4 |

**Note on the adoption-economics evidence table:** the table summarising
eight peer-reviewed studies on precision livestock/agriculture adoption
economics is a manually compiled narrative literature synthesis, not a
computational output — there is no script that generates it. Its
search-and-selection protocol is documented in the manuscript's Methods
section, and the table itself, with full source citations, appears in
the manuscript's Results section on the adoption-economics synthesis.

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
5. **Preliminary Poisson model z-statistics.** The manuscript's Table 4
   (preliminary Poisson regression, explicitly superseded by the primary
   negative binomial model in Table 2) reports z-statistics that differ
   by a small margin (≤0.1) from this package's output, though the
   coefficients, incidence rate ratios, and bootstrap confidence
   intervals match exactly. This table is diagnostic-only — its sole
   purpose is to document the overdispersion statistic that motivates
   the primary model — and no manuscript conclusion depends on its
   z-statistics or p-values.

## Citation

Please cite both the published article and this archived repository.
Citation metadata are provided in `CITATION.cff` and `.zenodo.json`.

## License

MIT License (code). The underlying bibliometric data were retrieved from
the Lens Scholarly Database (https://www.lens.org) under its terms of use
for research purposes; see `docs/DATA_DESCRIPTION.md`.

## Contact

**Halil Tosun, Ph.D.**

ORCID: https://orcid.org/0000-0001-5117-0390

Email: halilibrahimtosun@gmail.com

**Zenodo DOI:** https://doi.org/10.5281/zenodo.21541503

**Version:** 1.0.0
