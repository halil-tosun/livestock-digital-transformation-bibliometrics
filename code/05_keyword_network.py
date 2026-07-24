"""
05_keyword_network.py
======================
Keyword co-occurrence network construction at threshold 5 (main
analysis), with a sensitivity check at thresholds 3 and 10, and Louvain
community detection.

Produces:
  output/top_keywords_threshold5.csv
  output/keyword_network_threshold5_edges.csv
  output/keyword_clusters_threshold5.csv
  output/threshold_sensitivity.csv
"""
import pandas as pd
import networkx as nx
from _keyword_utils import get_doc_terms, build_cooccurrence, build_network
from _paths import FILTERED_CSV, OUTPUT_DIR, SEED


def main():
    df = pd.read_csv(FILTERED_CSV)
    doc_terms = get_doc_terms(df)
    occurrence, cooc = build_cooccurrence(doc_terms)
    print(f"Total unique keyword terms (cleaned, harmonised): {len(occurrence)}")

    sensitivity_rows = []
    for thr in (3, 5, 10):
        G, tls = build_network(occurrence, cooc, thr)
        sensitivity_rows.append({"threshold": thr, "items": G.number_of_nodes(),
                                  "links": G.number_of_edges(), "total_link_strength": tls})
    sens_df = pd.DataFrame(sensitivity_rows)
    sens_df.to_csv(OUTPUT_DIR / "threshold_sensitivity.csv", index=False)
    print("\nSensitivity analysis across thresholds:")
    print(sens_df.to_string(index=False))

    G5, tls5 = build_network(occurrence, cooc, 5)
    communities = nx.algorithms.community.louvain_communities(G5, weight="weight", seed=SEED)
    print(f"\nLouvain clusters at threshold 5: {len(communities)}")
    print("(Deterministic: node/edge insertion order is sorted in _keyword_utils.build_network.")
    print(" Without this, cluster count varies non-deterministically across runs -- see README.)")

    node_strength = {n: sum(G5[n][nb]["weight"] for nb in G5[n]) for n in G5.nodes()}
    top15 = sorted(G5.nodes(data=True), key=lambda x: -x[1]["occurrence"])[:15]
    print("\nTop 15 keywords by occurrence at threshold 5:")
    rows = []
    for n, d in top15:
        rows.append((n, d["occurrence"], node_strength[n]))
        print(f"  {n}: occurrence={d['occurrence']}, total_link_strength={node_strength[n]}")
    pd.DataFrame(rows, columns=["keyword", "occurrence", "total_link_strength"]).to_csv(
        OUTPUT_DIR / "top_keywords_threshold5.csv", index=False
    )

    with open(OUTPUT_DIR / "keyword_network_threshold5_edges.csv", "w") as f:
        f.write("keyword_a,keyword_b,weight\n")
        for (a, b), w in cooc.items():
            if a in G5.nodes and b in G5.nodes:
                f.write(f'"{a}","{b}",{w}\n')

    cluster_map = {}
    for i, comm in enumerate(communities, start=1):
        for node in comm:
            cluster_map[node] = i
    with open(OUTPUT_DIR / "keyword_clusters_threshold5.csv", "w") as f:
        f.write("keyword,occurrence,total_link_strength,cluster\n")
        for n, d in G5.nodes(data=True):
            f.write(f'"{n}",{d["occurrence"]},{node_strength[n]},{cluster_map[n]}\n')


if __name__ == "__main__":
    main()
