# Corpus relevance robustness check & IRR coefficient-difference test

Added during peer-review revision in response to reviewer queries about
(a) whether all 2,812 records in the primary corpus are genuinely
livestock-relevant, and (b) whether social-dimension framing's citation
advantage over digital-technology framing was formally tested. As of
manuscript v2, both checks are summarised as short in-text passages
(Materials and Methods, and Results, respectively) rather than under
dedicated headings.

## Files
- `build_relevance_filter.py` — flags records lacking any livestock/species
  term in Title, Abstract, Keywords, MeSH Terms, or Fields of Study, and
  writes `../data/raw/lens-data-filtered-2514.csv.gz` (the 298 flagged
  records excluded).
- `test_irr_coefficient_difference.py` — bootstrap test of the difference
  between the `has_digital` and `has_social` negative-binomial
  coefficients (output: `../output/irr_coefficient_difference_test.txt`).
- To reproduce the corpus-relevance sensitivity re-analysis: copy
  `code/01,04,05,06_*.py` and `_paths.py`/`_keyword_utils.py` into a
  scratch folder, point `FILTERED_CSV` in `_paths.py` at
  `lens-data-filtered-2514.csv.gz`, and re-run. All primary results
  replicate (see manuscript for full comparison).

## Results
**Corpus relevance:** 298 of 2,812 records (10.6%) lacked any
livestock/species-specific term. Re-estimating all primary analyses on
the remaining 2,514 documents (2,295 excluding partial-year 2026)
reproduced every substantive conclusion of the paper: digital-technology
and social-dimension keyword presence remained significant positive
predictors of citation count (NB2 IRR = 1.41, p<0.001 and IRR = 1.70,
p=0.004, respectively), the annual growth trend remained significant,
the Wilcoxon within-cluster peripherality test remained non-significant,
and Louvain clustering again returned six communities. The original
2,812-document corpus was therefore retained as the primary dataset.

**IRR coefficient difference:** although the point estimate for
social-dimension framing (IRR = 1.62) was numerically higher than for
digital-technology framing (IRR = 1.35), a bootstrap test of the
difference between the two log-scale coefficients found no statistically
significant difference (Δlog-IRR = 0.18, 95% CI −0.26 to 0.52, bootstrap
p = 0.376). The manuscript therefore describes social-dimension research
as achieving citation visibility "at least comparable to" — rather than
"significantly exceeding" — technology-oriented research.
