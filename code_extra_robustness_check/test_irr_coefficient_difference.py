import sys
sys.path.insert(0, '/home/claude/work/Replication/Replication/code')
import numpy as np
import pandas as pd
from scipy import stats, optimize
from scipy.special import gammaln
from _keyword_utils import get_doc_terms

df = pd.read_csv('/home/claude/work/Replication/Replication/data/raw/lens-data-filtered-2812.csv.gz')
doc_terms = get_doc_terms(df)
digital_terms = {"machine learning", "ai", "plf"}
social_terms = {"farmers", "technology", "policy", "socioeconomic factors"}
df["has_digital"] = [1 if terms & digital_terms else 0 for terms in doc_terms]
df["has_social"] = [1 if terms & social_terms else 0 for terms in doc_terms]
full = df[df["Publication Year"] < 2026].copy()
full["is_open_access"] = (full["Is Open Access"].astype(str).str.lower() == "true").astype(int)
full["year_c"] = full["Publication Year"] - full["Publication Year"].mean()

X = full[["year_c", "is_open_access", "has_digital", "has_social"]].values
X1 = np.column_stack([np.ones(len(X)), X])
y = full["Citing Works Count"].values.astype(float)
n, k = X1.shape

def nb_negloglik(params, Xb, yb):
    beta = params[:k]
    alpha = np.exp(params[k])
    mu = np.clip(np.exp(Xb @ beta), 1e-8, 1e8)
    r = 1.0 / alpha
    ll = (gammaln(yb + r) - gammaln(r) - gammaln(yb + 1)
          + r * np.log(r / (r + mu)) + yb * np.log(mu / (r + mu)))
    return -np.sum(ll)

init_beta = np.zeros(k)
init_beta[0] = np.log(y.mean())
res = optimize.minimize(nb_negloglik, np.concatenate([init_beta, [0.0]]), args=(X1, y),
                         method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-6, "fatol": 1e-6})
beta_hat = res.x[:k]
point_diff = beta_hat[4] - beta_hat[3]  # has_social - has_digital (log scale)
print("Point estimate coef diff (social - digital, log scale):", point_diff)
print("IRR ratio (social/digital):", np.exp(point_diff))

SEED = 42
rng = np.random.default_rng(SEED)
n_boot = 300
diffs = []
idx = np.arange(n)
for i in range(n_boot):
    s_idx = rng.choice(idx, size=n, replace=True)
    Xb, yb = X1[s_idx], y[s_idx]
    r2 = optimize.minimize(nb_negloglik, res.x, args=(Xb, yb), method="Nelder-Mead",
                            options={"maxiter": 8000, "xatol": 1e-5, "fatol": 1e-5})
    if r2.success:
        diffs.append(r2.x[4] - r2.x[3])

diffs = np.array(diffs)
se = diffs.std()
z = point_diff / se
p = 2 * (1 - stats.norm.cdf(abs(z)))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"\nBootstrap (n={len(diffs)}): SE={se:.4f}, z={z:.3f}, p={p:.4f}")
print(f"95% CI for log-diff: [{lo:.4f}, {hi:.4f}]")
print(f"95% CI for IRR ratio: [{np.exp(lo):.3f}, {np.exp(hi):.3f}]")
