"""
06_statistical_tests.py
=========================
Formal statistical tests: annual publication growth (OLS), within-
cluster centrality of social-dimension keywords (Wilcoxon signed-rank
on a data-driven Louvain partition), and prevalence-divergence testing
between digital-technology and social-dimension keyword shares
(bootstrap CI for the difference in trend slopes), plus five-year-bin
prevalence and Benjamini-Hochberg correction across the primary tests.

Produces:
  output/test1_annual_growth.csv
  output/test2_within_cluster_percentiles.csv
  output/test3_five_year_bin_prevalence.csv
  output/benjamini_hochberg_correction.csv
"""
import numpy as np
import pandas as pd
from scipy import stats
import networkx as nx
from _keyword_utils import get_doc_terms, build_cooccurrence, build_network
from _paths import FILTERED_CSV, OUTPUT_DIR, SEED

SOCIAL_TERMS = ["farmers", "technology", "policy", "socioeconomic factors", "farmers/psychology"]
DIGITAL_TERMS = {"machine learning", "ai", "plf"}
SOCIAL_TERMS_SET = {"farmers", "technology", "policy", "socioeconomic factors"}


def test1_growth_trend(df):
    yearly = df.groupby("Publication Year").size()
    yearly_full = yearly[yearly.index < 2026]
    slope, intercept, r, p, se = stats.linregress(yearly_full.index, yearly_full.values)
    out = pd.DataFrame([{"slope_docs_per_year": slope, "R_squared": r ** 2, "p_value": p}])
    out.to_csv(OUTPUT_DIR / "test1_annual_growth.csv", index=False)
    print("Test 1 (OLS annual growth):")
    print(out.to_string(index=False))
    yearly_full.reset_index().rename(columns={0: "documents", "Publication Year": "year"}).to_csv(
        OUTPUT_DIR / "annual_document_counts.csv", index=False
    )


def test2_within_cluster(occurrence, cooc):
    G5, _ = build_network(occurrence, cooc, 5)
    node_strength = {n: sum(G5[n][nb]["weight"] for nb in G5[n]) for n in G5.nodes()}
    communities = nx.algorithms.community.louvain_communities(G5, weight="weight", seed=SEED)

    percentiles = []
    for comm in communities:
        comm_list = sorted(comm)
        tls_list = [node_strength[n] for n in comm_list]
        for term in comm_list:
            if term in SOCIAL_TERMS_SET or term == "farmers/psychology":
                pct = stats.percentileofscore(tls_list, node_strength[term], kind="mean")
                percentiles.append({"keyword": term, "cluster_size": len(comm_list),
                                     "total_link_strength": node_strength[term], "percentile_rank": pct})

    pdf = pd.DataFrame(percentiles)
    pdf.to_csv(OUTPUT_DIR / "test2_within_cluster_percentiles.csv", index=False)
    print("\nTest 2 (within-cluster percentile ranks):")
    print(pdf.to_string(index=False))

    pcts = pdf["percentile_rank"].tolist()
    res = stats.wilcoxon([p - 50 for p in pcts], alternative="less")
    n = len(pcts)
    diffs = [p - 50 for p in pcts]
    ranks = stats.rankdata(np.abs(diffs))
    signed_ranks = ranks * np.sign(diffs)
    w_plus = signed_ranks[signed_ranks > 0].sum()
    mean_w = n * (n + 1) / 4
    sd_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    z = (w_plus - mean_w) / sd_w
    effect_r = z / np.sqrt(n)
    print(f"\nMean percentile: {np.mean(pcts):.1f}%  |  Wilcoxon p={res.pvalue:.4f}  |  effect size r={effect_r:.3f}")
    return res.pvalue


def test3_prevalence_divergence(df, doc_terms):
    df = df.copy()
    df["has_digital"] = [1 if terms & DIGITAL_TERMS else 0 for terms in doc_terms]
    df["has_social"] = [1 if terms & SOCIAL_TERMS_SET else 0 for terms in doc_terms]

    full_years = df[df["Publication Year"] < 2026]
    slope_d, _, _, p_d, _ = stats.linregress(full_years["Publication Year"], full_years["has_digital"])
    slope_s, _, _, p_s, _ = stats.linregress(full_years["Publication Year"], full_years["has_social"])
    print(f"\nDigital-technology prevalence trend: slope={slope_d:.5f}/yr, p={p_d:.2e}")
    print(f"Social-dimension prevalence trend:   slope={slope_s:.5f}/yr, p={p_s:.3f}")

    rng = np.random.default_rng(SEED)

    def slope_boot(x, y, n=2000):
        slopes = []
        idx = np.arange(len(x))
        for _ in range(n):
            s_idx = rng.choice(idx, size=len(idx), replace=True)
            sl, _, _, _, _ = stats.linregress(np.array(x)[s_idx], np.array(y)[s_idx])
            slopes.append(sl)
        return np.array(slopes)

    boot_d = slope_boot(full_years["Publication Year"].values, full_years["has_digital"].values)
    boot_s = slope_boot(full_years["Publication Year"].values, full_years["has_social"].values)
    diff = boot_d - boot_s
    ci_low, ci_high = np.percentile(diff, [2.5, 97.5])
    print(f"Bootstrap 95% CI for slope difference: [{ci_low:.4f}, {ci_high:.4f}]")

    bins = [(2000, 2005), (2006, 2010), (2011, 2015), (2016, 2020), (2021, 2025)]
    rows = []
    for start, end in bins:
        sub = full_years[(full_years["Publication Year"] >= start) & (full_years["Publication Year"] <= end)]
        rows.append({"period_start": start, "period_end": end, "n_docs": len(sub),
                     "digital_prevalence_pct": sub["has_digital"].mean() * 100,
                     "social_prevalence_pct": sub["has_social"].mean() * 100})
    bin_df = pd.DataFrame(rows)
    bin_df.to_csv(OUTPUT_DIR / "test3_five_year_bin_prevalence.csv", index=False)
    print("\nFive-year-bin prevalence:")
    print(bin_df.to_string(index=False))

    return p_d, p_s


def benjamini_hochberg(pvals_dict):
    names = list(pvals_dict.keys())
    pvals = np.array(list(pvals_dict.values()))
    order = np.argsort(pvals)
    ranked_p = pvals[order]
    m = len(pvals)
    bh = ranked_p * m / (np.arange(m) + 1)
    bh_adj = np.minimum.accumulate(bh[::-1])[::-1]
    bh_adj = np.clip(bh_adj, 0, 1)
    result = []
    for idx, i in enumerate(order):
        result.append({"test": names[i], "raw_p": pvals[i], "bh_adjusted_p": bh_adj[idx]})
    out = pd.DataFrame(result)
    out.to_csv(OUTPUT_DIR / "benjamini_hochberg_correction.csv", index=False)
    print("\nBenjamini-Hochberg correction across primary tests:")
    print(out.to_string(index=False))


def main():
    df = pd.read_csv(FILTERED_CSV)
    doc_terms = get_doc_terms(df)
    occurrence, cooc = build_cooccurrence(doc_terms)

    test1_growth_trend(df)
    p_wilcoxon = test2_within_cluster(occurrence, cooc)
    p_digital, p_social = test3_prevalence_divergence(df, doc_terms)

    benjamini_hochberg({
        "Test 1 (growth trend)": 2.07e-07,
        "Test 2 (within-cluster percentile)": p_wilcoxon,
        "Test 3a (digital prevalence trend)": p_digital,
        "Test 3b (social prevalence trend)": p_social,
        "Test 4 NB: open access": 0.179,
        "Test 4 NB: has_digital": 0.0005,
        "Test 4 NB: has_social": 0.0064,
    })
    print("\n(Test 4 p-values are taken from 04_citation_regression.py output)")


if __name__ == "__main__":
    main()
