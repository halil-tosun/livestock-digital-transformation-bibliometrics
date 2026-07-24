## ============================================================================
## bibliometrix_reproduction.R
##
## Independently rebuilds the bibliometrix-compatible data frame directly
## from the raw Lens CSV export, using the same keyword cleaning and
## harmonisation rules used in the Python pipeline (../code/_keyword_utils.py),
## so that:
##   (a) descriptive bibliometrics can be cross-checked against the Python
##       output,
##   (b) the keyword co-occurrence network can be reproduced in
##       bibliometrix terms, and
##   (c) Callon's strategic (thematic) map and the Sankey thematic-evolution
##       diagram can be produced directly.
##
## bibliometrix's built-in Lens importer (convert2df(..., dbsource="lens"))
## maps only a subset of Lens export columns and does not combine
## "Keywords" with "MeSH Terms". The data frame is therefore built manually
## below, which guarantees the R analysis uses an identical keyword set to
## the Python analysis.
##
## Requirements: install.packages(c("bibliometrix", "dplyr", "stringr"))
## Tested on R 4.6.1 with the current CRAN release of bibliometrix.
## ============================================================================

library(bibliometrix)
library(dplyr)
library(stringr)

## ---- 1. Load raw data --------------------------------------------------------
## The data file is gzip-compressed to keep the repository under GitHub's web
## upload size limit. Base R's read.csv() auto-detects gzip compression from
## the ".gz" extension. If your R version does not, decompress manually first
## (R.utils::gunzip("../data/raw/lens-data-filtered-2812.csv.gz", remove=FALSE)
## or `gunzip -k` from a terminal) and point this line at the .csv file instead.
raw <- read.csv("../data/raw/lens-data-filtered-2812.csv.gz", stringsAsFactors = FALSE, encoding = "UTF-8")
stopifnot(nrow(raw) == 2812)

## R's read.csv typically converts "MeSH Terms" to "MeSH.Terms" and
## "Author/s" to "Author.s" (dots replacing spaces/slashes). Run
## colnames(raw) and adjust the column references below if this differs
## in your R/readr version.
print(colnames(raw))

## ---- 2. Keyword cleaning / harmonisation (mirrors ../code/_keyword_utils.py) -
STOPTERMS <- c("male", "female", "humans", "human")

HARMONIZE <- c(
  "artificial intelligence"       = "ai",
  "precision livestock farming"   = "plf",
  "smart farming"                 = "digital livestock transformation",
  "digital agriculture"           = "digital livestock transformation",
  "climate change"                = "climate resilience",
  "climate adaptation"            = "climate resilience"
)

clean_term <- function(t) {
  t <- tolower(trimws(t))
  t <- str_remove(t, "\\d+$")
  trimws(t)
}

build_keyword_string <- function(kw, mesh) {
  terms <- c()
  for (src in c(kw, mesh)) {
    if (is.na(src) || src == "") next
    parts <- strsplit(src, ";")[[1]]
    for (p in parts) {
      c1 <- clean_term(p)
      if (nchar(c1) < 2 || c1 %in% STOPTERMS) next
      if (c1 %in% names(HARMONIZE)) c1 <- HARMONIZE[[c1]]
      terms <- c(terms, c1)
    }
  }
  terms <- unique(terms)
  if (length(terms) == 0) return(NA)
  paste(terms, collapse = ";")
}

raw$DE_combined <- mapply(build_keyword_string, raw$Keywords, raw$MeSH.Terms)
cat("Documents with at least one combined keyword term:",
    sum(!is.na(raw$DE_combined)), "/", nrow(raw), "\n")

## ---- 3. Build a minimal bibliometrix-compatible data frame -------------------
M <- data.frame(
  AU = raw$Author.s,
  TI = toupper(raw$Title),
  SO = toupper(raw$Source.Title),
  DE = toupper(raw$DE_combined),
  ID = toupper(raw$DE_combined),
  PY = raw$Publication.Year,
  TC = raw$Citing.Works.Count,
  DT = "ARTICLE",
  DI = raw$DOI,
  stringsAsFactors = FALSE
)

## biblioAnalysis() requires an M$DB column identifying the source database.
M$DB <- "LENS"

## biblioNetwork() requires an M$SR (short reference) column. Any
## unique-per-row string is sufficient; it does not need to follow a
## specific citation-style format for this analysis.
M$SR <- paste0(toupper(substr(M$AU, 1, 20)), ", ", M$PY, ", DOC", seq_len(nrow(M)))
stopifnot(length(M$SR) == 2812)

class(M) <- c("bibliometrixDB", "data.frame")

## ---- 4. Descriptive bibliometrics (cross-check against Python output) --------
results <- biblioAnalysis(M, sep = ";")
summary(results, k = 10, pause = FALSE)
## Expect: n documents = 2812, average citations/doc = 33.9, top-10 journals
## and top-10 cited documents matching ../output/leading_sources.csv and
## ../output/top_cited_documents.csv.

## ---- 5. Keyword co-occurrence network (cross-check against Section 3.4) ------
NetMatrix <- biblioNetwork(M, analysis = "co-occurrences", network = "keywords", sep = ";", n = NULL)

## The diagonal of NetMatrix holds each keyword's own occurrence count;
## colSums() would give an inflated total co-occurrence weight, not
## occurrence -- use Matrix::diag().
occ <- Matrix::diag(NetMatrix)
kept5 <- names(occ[occ >= 5])
cat("Items at threshold 5 (R):", length(kept5), "\n")
## Expect: 560 (matches ../output/threshold_sensitivity.csv, threshold=5 row)

## ---- 6. Callon's strategic (thematic) map (Figure 3) --------------------------
Map <- thematicMap(M, field = "ID", n = 250, minfreq = 5,
                    stemming = FALSE, size = 0.5, n.labels = 3, repel = TRUE)
plot(Map$map)
print(Map$clusters)

## Locate the four social-dimension keywords in the map.
## Map$words uses capitalised column names (Words, Cluster_Label, Cluster,
## btw_centrality); run colnames(Map$words) if this differs in your version.
words_df <- Map$words
print(words_df[words_df$Words %in% c("farmers", "technology", "policy",
                                       "socioeconomic factors", "farmers/psychology"),
                c("Words", "Cluster_Label", "Cluster", "btw_centrality")])

## ---- 7. Thematic evolution / Sankey diagram (Figure 4) ------------------------
## thematicEvolution() creates n+1 periods from n interior cut-points. Passing
## a cut-point equal to the dataset's own max year causes a
## "'breaks' are not unique" error in cut.default() -- use interior cut-points
## only (here, two cut-points create three periods).
years <- c(2010, 2020)
nexus <- thematicEvolution(M, field = "ID", years = years, n = 150, minFreq = 2)
plotThematicEvolution(nexus$Nodes, nexus$Edges)
## Renders in the RStudio/Posit "Viewer" pane (an interactive htmlwidget, not
## a static plot). Export via the Viewer pane's own "Export > Save as Image"
## button, or take a screenshot directly.

## ---- 8. Save outputs -----------------------------------------------------------
write.csv(Map$words, "R_strategic_map_words.csv", row.names = FALSE)
write.csv(Map$clusters, "R_strategic_map_clusters.csv", row.names = FALSE)
write.csv(nexus$Nodes, "R_thematic_evolution_nodes.csv", row.names = FALSE)
write.csv(nexus$Edges, "R_thematic_evolution_edges.csv", row.names = FALSE)

## ============================================================================
## EXPECTED RESULTS SUMMARY
##   Documents with keywords:      2415 / 2812
##   Items at threshold 5:          560            (exact match to Python)
##   Callon map clusters:             5            (n=250, minfreq=5)
##   farmers:    Cluster "animals",        btw_centrality ~97.8
##   technology: Cluster "animal welfare", btw_centrality ~212.5
##   policy, socioeconomic factors: do not appear among the top 250 terms
##   Thematic evolution: no farmers/technology/policy/socioeconomic-factors
##     node appears in any of the 3 periods at this frequency threshold
## ============================================================================
