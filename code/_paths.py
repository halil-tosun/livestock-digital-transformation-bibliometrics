"""
Shared path configuration. Every script imports this so the package runs
identically regardless of the current working directory it is launched from.

Tables are written to ../output/ (as .csv). Figures (.png) are written to
../figures/ at 300 DPI.
"""
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CODE_DIR.parent
DATA_DIR = ROOT_DIR / "data" / "raw"
OUTPUT_DIR = ROOT_DIR / "output"
FIG_DIR = ROOT_DIR / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

RAW_CSV = DATA_DIR / "lens-data-raw-7405.csv.gz"
FILTERED_CSV = DATA_DIR / "lens-data-filtered-2812.csv.gz"

FIGURE_DPI = 300
SEED = 42
