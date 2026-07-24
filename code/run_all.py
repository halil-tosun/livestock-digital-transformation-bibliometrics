"""
run_all.py
==========
Runs the full replication pipeline in order and writes every table
(.csv) reported in the paper to ../output/, and every figure (.png,
300 DPI) to ../figures/.

Expected runtime: 2-3 minutes total on a standard laptop. The slowest
step is the bootstrap resampling in the negative binomial citation
regression (300-1,000 resamples).

Run individual numbered scripts directly to regenerate only one
table or figure, e.g.: python 03_citation_structure.py
"""
import importlib.util
import os
import time

HERE = os.path.dirname(__file__)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if hasattr(mod, "main"):
        mod.main()
    return mod


if __name__ == "__main__":
    t0 = time.time()

    print("=== 01: Dataset overview and PRISMA screening (Table 1) ===")
    _load("01_dataset_overview")

    print("\n=== 02: Leading sources ===")
    _load("02_leading_sources")

    print("\n=== 03: Citation structure (top-cited documents) ===")
    _load("03_citation_structure")

    print("\n=== 04: Citation regression models (Tables 2-4) ===")
    _load("04_citation_regression")

    print("\n=== 05: Keyword co-occurrence network ===")
    _load("05_keyword_network")

    print("\n=== 06: Statistical significance tests ===")
    _load("06_statistical_tests")

    print("\n=== 07: Figures 1-2 (300 DPI) ===")
    _load("07_make_figures")

    print(f"\nAll done in {time.time() - t0:.0f} seconds.")
    print("See ../output/ for all tables and ../figures/ for Figures 1-2.")
    print("Figures 3-4 (R/Bibliometrix) and Appendix Figures A1-A4 (VOSviewer)")
    print("are produced separately -- see ../r/ and ../vosviewer/.")
