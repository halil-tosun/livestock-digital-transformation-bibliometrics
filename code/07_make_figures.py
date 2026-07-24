"""
07_make_figures.py
====================
Generates Figure 1 (keyword co-occurrence network) and Figure 2 (annual
publication growth) at 300 DPI.

Figures 3 (Callon strategic map) and 4 (Sankey thematic evolution) are
produced directly in R/Bibliometrix -- see ../r/bibliometrix_reproduction.R.
The Appendix VOSviewer figures are produced directly in the VOSviewer
application -- see ../vosviewer/.

Produces:
  figures/Figure1_keyword_network.png
  figures/Figure2_annual_growth.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from _keyword_utils import get_doc_terms, build_cooccurrence
from _paths import FILTERED_CSV, FIG_DIR, FIGURE_DPI


def make_figure1(occurrence, cooc):
    """Keyword co-occurrence network at min. occurrence=10 (for figure
    readability only; the main analysis in 05_keyword_network.py uses
    threshold 5)."""
    min_occ = 10
    kept = sorted(t for t, c in occurrence.items() if c >= min_occ)
    G = nx.Graph()
    for t in kept:
        G.add_node(t, occurrence=occurrence[t])
    for (a, b), w in sorted(cooc.items()):
        if a in G.nodes and b in G.nodes and w >= 3:
            G.add_edge(a, b, weight=w)
    G.remove_nodes_from(list(nx.isolates(G)))
    print(f"Figure 1 network: nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")

    communities = nx.algorithms.community.louvain_communities(G, weight="weight", seed=42)
    palette = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1"]
    color_map = {n: palette[i % len(palette)] for i, comm in enumerate(communities) for n in comm}

    pos = nx.spring_layout(G, k=0.6, seed=42, weight="weight")
    fig, ax = plt.subplots(figsize=(14, 11), dpi=FIGURE_DPI)
    node_sizes = [max(occurrence[n] * 3, 30) for n in G.nodes()]
    node_colors = [color_map[n] for n in G.nodes()]
    nx.draw_networkx_edges(G, pos, alpha=0.25, width=0.6, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.85, ax=ax)
    labels = {n: n for n in G.nodes() if occurrence[n] >= 20}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)
    ax.set_title(f"Keyword co-occurrence network (min. occurrence={min_occ}, Louvain clusters coloured)\n"
                 f"nodes={G.number_of_nodes()}, edges={G.number_of_edges()}", fontsize=11)
    ax.axis("off")
    plt.tight_layout()
    out_path = FIG_DIR / "Figure1_keyword_network.png"
    plt.savefig(out_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def make_figure2(df):
    """Annual publication output, 2000-2026."""
    yearly = df.groupby("Publication Year").size()
    fig, ax = plt.subplots(figsize=(10, 5), dpi=FIGURE_DPI)
    colors = ["#4E79A7" if y < 2026 else "#B0B0B0" for y in yearly.index]
    ax.bar(yearly.index, yearly.values, color=colors)
    ax.set_xlabel("Publication year", fontsize=11)
    ax.set_ylabel("Number of documents", fontsize=11)
    ax.set_title("Annual publication output, 2000-2026\n(2026, grey, is a partial year, excluded from the OLS growth regression)", fontsize=11)
    plt.tight_layout()
    out_path = FIG_DIR / "Figure2_annual_growth.png"
    plt.savefig(out_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    df = pd.read_csv(FILTERED_CSV)
    doc_terms = get_doc_terms(df)
    occurrence, cooc = build_cooccurrence(doc_terms)
    make_figure1(occurrence, cooc)
    make_figure2(df)


if __name__ == "__main__":
    main()
