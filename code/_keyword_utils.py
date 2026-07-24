"""
Shared keyword cleaning, harmonisation, and co-occurrence network
construction module, imported by every other script in this package.
This is the single source of truth for keyword processing: every table
and figure that depends on the keyword network relies on these exact
functions being used consistently.

Methodology:
  - Combine the 'Keywords' and 'MeSH Terms' fields for each document.
  - Lowercase, strip trailing digit artefacts (e.g. "vaccinology1").
  - Remove generic MeSH checktags (male, female, human/humans) as
    non-informative demographic terms.
  - Retain MeSH subheadings after "/" (e.g. "Cattle/physiology" is kept
    distinct from "Cattle") -- this was verified to reproduce an
    independent R/Bibliometrix keyword count almost exactly.
  - Apply a small harmonisation dictionary merging near-synonymous terms.

Determinism note: build_network() inserts nodes and edges in sorted
order. Without this, Louvain community detection (networkx) can return
a different number of communities across otherwise-identical runs,
because Python's per-process string-hash randomisation affects
networkx's internal iteration order even with a fixed `seed` parameter.
Sorting insertion order removes this sensitivity entirely.
"""
import re
from collections import Counter
from itertools import combinations

STOPTERMS = {"male", "female", "humans", "human"}

HARMONIZE = {
    "artificial intelligence": "ai",
    "precision livestock farming": "plf",
    "smart farming": "digital livestock transformation",
    "digital agriculture": "digital livestock transformation",
    "climate change": "climate resilience",
    "climate adaptation": "climate resilience",
}


def clean_term(t: str) -> str:
    """Lowercase, strip whitespace and trailing digit artefacts."""
    t = t.strip().lower()
    t = re.sub(r"\d+$", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def get_doc_terms(df, keywords_col="Keywords", mesh_col="MeSH Terms"):
    """
    Given a dataframe with Lens-format Keywords/MeSH Terms columns,
    return a list (one entry per document/row) of sets of cleaned,
    harmonised keyword terms.
    """
    import pandas as pd

    doc_terms = []
    for kwval, meshval in zip(df[keywords_col], df[mesh_col]):
        terms = set()
        for src in (kwval, meshval):
            if pd.isna(src):
                continue
            for t in str(src).split(";"):
                c = clean_term(t)
                if not c or len(c) < 2 or c in STOPTERMS:
                    continue
                c = HARMONIZE.get(c, c)
                terms.add(c)
        doc_terms.append(terms)
    return doc_terms


def build_cooccurrence(doc_terms):
    """Return (occurrence Counter, cooccurrence Counter keyed by (a,b) tuples)."""
    occurrence = Counter()
    cooc = Counter()
    for terms in doc_terms:
        for t in terms:
            occurrence[t] += 1
        for a, b in combinations(sorted(terms), 2):
            cooc[(a, b)] += 1
    return occurrence, cooc


def build_network(occurrence, cooc, min_occ):
    """
    Build a networkx Graph of keywords co-occurring at or above min_occ.
    Returns (Graph, total_link_strength). Nodes/edges are inserted in
    sorted order for deterministic Louvain clustering (see module note).
    """
    import networkx as nx

    kept = sorted(t for t, c in occurrence.items() if c >= min_occ)
    G = nx.Graph()
    for t in kept:
        G.add_node(t, occurrence=occurrence[t])
    for (a, b), w in sorted(cooc.items()):
        if a in G.nodes and b in G.nodes:
            G.add_edge(a, b, weight=w)
    tls = sum(d["weight"] for _, _, d in G.edges(data=True))
    return G, tls
