# CHANGELOG

All notable changes to this replication package will be documented in this file.

The format is inspired by *Keep a Changelog* and follows semantic versioning where appropriate.

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

**Zenodo DOI:** https://doi.org/10.5281/zenodo.21541503
