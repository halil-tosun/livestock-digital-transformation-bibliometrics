# DATA_DESCRIPTION

## Data Source

Bibliometric records were retrieved from the **Lens Scholarly Database**
(https://www.lens.org), which indexes multidisciplinary scholarly literature
and provides citation metadata suitable for science-mapping analyses. Data
were retrieved under the Lens.org terms of use for research purposes.

## Search Strategy

A structured Boolean search combined:
- Livestock-related terms (e.g., livestock, dairy, cattle, poultry)
- Digital-technology terms (e.g., artificial intelligence, machine
  learning, Internet of Things, sensors, precision livestock farming,
  precision agriculture, smart farming)
- Sustainability-related terms (e.g., sustainability, climate)

Social-dimension keywords (e.g., farmer autonomy, digital equity, data
governance) were intentionally **excluded** from the search strategy,
since their inclusion would have predetermined the presence of the themes
whose prevalence this study measures. The search covered publications
from January 2000 to June 2026 and was restricted to peer-reviewed
journal articles.

## Files

Both raw-data CSV files below are distributed gzip-compressed
(`.csv.gz`) to keep individual files under GitHub's 25 MB web-upload
limit. `pandas.read_csv()` decompresses `.gz` files automatically based
on the file extension, so no manual decompression is needed to run the
Python pipeline. R's `read.csv()` also auto-detects gzip compression in
most versions; see the note in `r/bibliometrix_reproduction.R` if this
does not work in your R installation.

### `data/raw/lens-data-raw-7405.csv.gz`
The unfiltered search result: 7,405 records at the Identification stage of
PRISMA screening. This file is trimmed to eight columns (Lens ID, Title,
Publication Year, Author/s, Source Title, Citing Works Count, DOI,
Publication Type) rather than the full Lens.org export. The two largest
columns in the original export — Abstract and References — are dropped:
neither is used anywhere in this repository's pipeline, and together they
accounted for roughly 26 of the original ~30 MB file, which exceeded
GitHub's 25 MB web-upload limit. The raw file's sole purpose in this
package is to verify, via the `Lens ID` column, that the filtered
analytical dataset below is a strict subset of the original search
result (`code/01_dataset_overview.py`); no other column from this file
is read by any script.

### `data/raw/lens-data-filtered-2812.csv.gz`
The final, PRISMA-screened analytical dataset: 2,812 peer-reviewed journal
articles. This is a strict subset of the raw file (verified programmatically
in `code/01_dataset_overview.py`) after:
1. Title/abstract screening for thematic relevance (4,538 records excluded).
2. Eligibility assessment for complete bibliographic metadata — author
   information, publication year, source details, keywords, and citation
   metadata (55 records excluded).

No duplicate records were identified within the raw export.

## Key Columns

| Column | Description |
|---|---|
| `Lens ID` | Unique document identifier assigned by Lens.org |
| `Title` | Document title |
| `Author/s` | Semicolon-separated author list |
| `Source Title` | Journal name (case varies; see Known Discrepancies in the main README) |
| `Publication Year` | Year of publication (2000-2026) |
| `Citing Works Count` | Number of citing works recorded by Lens.org at the time of retrieval |
| `Keywords` | Semicolon-separated author/database keywords |
| `MeSH Terms` | Semicolon-separated Medical Subject Headings, where assigned |
| `Is Open Access` | Boolean open-access status |
| `DOI` | Digital Object Identifier, where available |

## Derived Variables

All derived variables (cleaned/harmonised keyword sets, digital-technology
and social-dimension keyword indicators, co-occurrence network edges) are
computed directly from the raw columns above by `code/_keyword_utils.py`
and are not stored as separate raw-data files; running the pipeline
(`code/run_all.py`) regenerates them from the two CSV files above.

## VOSviewer Input Files

`vosviewer/lens_for_vosviewer.ris` is the same filtered dataset (2,812
records), converted to RIS format and pre-cleaned for direct VOSviewer
import. `vosviewer/vosviewer_thesaurus.txt` documents the synonym-merging
rules applied within VOSviewer (a VOSviewer-native equivalent of the
Python harmonisation dictionary in `_keyword_utils.py`).
