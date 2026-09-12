# CHANGELOG

All notable changes to this replication package will be documented in this file.

The format is inspired by *Keep a Changelog* and follows semantic versioning where appropriate.

---

## Version 2.0.0 (Co-author added; manuscript focus revision)

### Added
- Victor E. Cabrera (University of Wisconsin-Madison) added as second
  author across CITATION.cff, .zenodo.json, and README.md, following his
  addition as co-author on the manuscript.

### Changed — manuscript structure (repository outputs unaffected)
Following co-author review, the manuscript was substantially condensed
to keep it focused on its core hypotheses. **No underlying analysis,
script, or output in this repository changed as a result** — only which
tables/figures are embedded in the manuscript body changed. Specifically:

- The preliminary Poisson regression table, the log1p-OLS robustness
  regression table, and the annual-document-count table (manuscript v1
  Tables 3, 4, and 6) were condensed into one-sentence in-text summaries.
  Full tables remain available in `output/`.
- Callon's strategic thematic map and the Sankey thematic-evolution
  diagram (manuscript v1 Figures 3 and 4) were condensed into a single
  paragraph ("Independent verification (VOSviewer and R/Bibliometrix)")
  together with the VOSviewer cross-validation discussion. Full images
  remain available in `figures/`.
- The four VOSviewer zoomed-keyword figures (manuscript v1 Appendix
  Figures A1-A4) are now referenced as Electronic Supplementary Material
  Fig. S1-S4 rather than as main-text appendix figures.
- Manuscript tables were renumbered accordingly: v1 Table 5 (statistical
  summary) → v2 Table 3; v1 Table 7 (within-cluster percentiles) → v2
  Table 4; v1 Table 8 (five-year prevalence) → v2 Table 5; v1 Table 9
  (adoption-economics synthesis) → v2 Table 6. v1 Tables 1 and 2 are
  unchanged (v2 Table 1 and Table 2).
- All manuscript figure captions were reformatted from "Figure N." to
  the journal-required "Fig. N" style (no trailing punctuation).

See `docs/CODEBOOK.md`, `docs/Replication_Guide.md`, and
`docs/REPRODUCIBILITY_CHECKLIST.md` for updated table/figure
cross-references reflecting the v2 manuscript numbering.

---

## Version 1.1.0 (Peer-review revision)

Added during a peer-review revision pass (see manuscript "Corpus relevance
robustness check" section and Discussion) in response to a reviewer query
about corpus relevance and citation-comparison claims.

### Added
- `code_extra_robustness_check/build_relevance_filter.py` — reproducible,
  rule-based check flagging records lacking any livestock/species-specific
  term; used to verify that the study's conclusions are robust to excluding
  298 (10.6%) potentially off-topic records. The primary 2,812-document
  corpus was retained for all reported analyses.
- `code_extra_robustness_check/test_irr_coefficient_difference.py` — formal
  bootstrap test of the difference between the `has_digital` and
  `has_social` negative-binomial regression coefficients (Δlog-IRR = 0.18,
  95% CI −0.26 to 0.52, bootstrap *p* = 0.376), confirming that the two are
  not statistically distinguishable. This corrected an earlier draft claim
  that social-dimension framing achieved "significantly greater" citation
  visibility than digital-technology framing.

### Changed
- `code/07_make_figures.py` — Figure 1 (keyword co-occurrence network)
  regenerated to show only the top 30 keywords by occurrence, excluding the
  generic MeSH checktag "animals" (present in 32% of documents and
  providing no discriminating signal), for readability. The underlying
  keyword-network analysis (threshold-5, in `code/05_keyword_network.py`)
  is unchanged.

### Notes
Manuscript-side corrections made during this revision (single-reviewer
screening disclosure, author-block and title-page completion, figure/
reference formatting to journal style, removal of double-anonymization
placeholders after confirming the target journal uses single-blind review)
are documented in the manuscript's own tracked changes and are not
duplicated here, as they do not affect the code or data in this package.

---

## Version 1.0.0 (Initial Public Release)

### Added
- Complete Python source code for all bibliometric analyses, statistical
  tests, tables, and figures.
- R/Bibliometrix script for independent cross-validation and for
  producing the strategic (thematic) map and Sankey thematic-evolution
  diagram.
- VOSviewer project files (RIS export, pre-computed network file, and
  thesaurus) for a third, independent cross-validation of the keyword
  co-occurrence network.
- Raw (7,405-record) and PRISMA-filtered (2,812-record) bibliometric
  datasets retrieved from the Lens Scholarly Database.
- README.md with repository overview and usage instructions.
- CODEBOOK.md describing the analytical workflow and script-to-output
  correspondence.
- DATA_DESCRIPTION.md documenting data sources and structure.
- REPRODUCIBILITY_CHECKLIST.md.
- Replication_Guide.md with step-by-step instructions for all three
  software environments (Python, R, VOSviewer).
- CITATION.cff and .zenodo.json for software citation and Zenodo metadata.
- LICENSE, requirements.txt, environment.yml, .gitignore.

### Reproducibility
- One-command Python workflow via `run_all.py` (7 scripts, ~2-3 minutes).
- All figures rendered at 300 DPI.
- Shared, deterministic keyword-processing and network-construction
  module (`_keyword_utils.py`) ensures every table and figure depending
  on the keyword network is computed on an identical basis.
- A previously-encountered non-determinism in Louvain cluster counts
  (caused by Python's per-process string-hash randomisation affecting
  networkx's internal iteration order) is fixed by sorting node/edge
  insertion order; this is documented in the main README rather than
  silently corrected.
- Computational environment documented for all three software
  environments used (Python, R, VOSviewer).
- Repository prepared for GitHub release and Zenodo archiving.

### Notes
The Zenodo DOI will be added after the first public repository release.
