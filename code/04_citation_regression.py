"""
04_citation_regression.py
===========================
Citation-impact regression models: a preliminary Poisson specification
(diagnostic only), the primary negative binomial (NB2) model, and a
log1p-transformed OLS robustness check.

Produces:
  output/regression_poisson_preliminary.csv
  output/regression_negative_binomial_primary.csv
  output/regression_log1p_ols_robustness.csv

Runtime: ~1-2 minutes (bootstrap resampling for the NB model).
"""
import numpy as np
import pandas as pd
from scipy import stats, optimize
from scipy.special import gammaln
from sklearn.linear_model import PoissonRegressor
from _keyword_utils import get_doc_terms
from _paths import FILTERED_CSV, OUTPUT_DIR, SEED


def build_covariates(df):
    doc_terms = get_doc_terms(df)
    digital_terms = {"machine learning", "ai", "plf"}
    social_terms = {"farmers", "technology", "policy", "socioeconomic factors"}
    df = df.copy()
    df["has_digital"] = [1 if terms & digital_terms else 0 for terms in doc_terms]
    df["has_social"] = [1 if terms & social_terms else 0 for terms in doc_terms]
    full = df[df["Publication Year"] < 2026].copy()
    full["is_open_access"] = (full["Is Open Access"].astype(str).str.lower() == "true").astype(int)
    full["year_c"] = full["Publication Year"] - full["Publication Year"].mean()
    return full


def poisson_preliminary(full):
    X = full[["year_c", "is_open_access", "has_digital", "has_social"]].values
    y = full["Citing Works Count"].values.astype(float)

    model = PoissonRegressor(alpha=1e-6, max_iter=2000)
    model.fit(X, y)
    mu = model.predict(X)
    pearson_resid = (y - mu) / np.sqrt(mu)
    dispersion = np.sum(pearson_resid ** 2) / (len(y) - X.shape[1] - 1)
    print(f"Preliminary Poisson: Pearson dispersion statistic = {dispersion:.1f} (severe overdispersion; motivates NB model)")

    rng = np.random.default_rng(SEED)
    n_boot = 500
    boot_coefs = []
    idx = np.arange(len(y))
    for _ in range(n_boot):
        s_idx = rng.choice(idx, size=len(idx), replace=True)
        m = PoissonRegressor(alpha=1e-6, max_iter=1000)
        try:
            m.fit(X[s_idx], y[s_idx])
            boot_coefs.append(m.coef_)
        except Exception:
            continue
    boot_coefs = np.array(boot_coefs)

    names = ["year_c", "is_open_access", "has_digital", "has_social"]
    rows = []
    for i, name in enumerate(names):
        se = boot_coefs[:, i].std()
        z = model.coef_[i] / se
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        lo, hi = np.percentile(boot_coefs[:, i], [2.5, 97.5])
        rows.append({"variable": name, "coef_log": model.coef_[i], "IRR": np.exp(model.coef_[i]),
                     "bootstrap_SE": se, "z": z, "p_value": p,
                     "CI_low": np.exp(lo), "CI_high": np.exp(hi)})
    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT_DIR / "regression_poisson_preliminary.csv", index=False)
    print(out.to_string(index=False))


def negative_binomial_primary(full):
    X = full[["year_c", "is_open_access", "has_digital", "has_social"]].values
    X1 = np.column_stack([np.ones(len(X)), X])
    y = full["Citing Works Count"].values.astype(float)
    n, k = X1.shape

    def nb_negloglik(params):
        beta = params[:k]
        alpha = np.exp(params[k])
        mu = np.clip(np.exp(X1 @ beta), 1e-8, 1e8)
        r = 1.0 / alpha
        ll = (gammaln(y + r) - gammaln(r) - gammaln(y + 1)
              + r * np.log(r / (r + mu)) + y * np.log(mu / (r + mu)))
        return -np.sum(ll)

    init_beta = np.zeros(k)
    init_beta[0] = np.log(y.mean())
    res = optimize.minimize(nb_negloglik, np.concatenate([init_beta, [0.0]]),
                             method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-6, "fatol": 1e-6})
    beta_hat = res.x[:k]
    alpha_hat = np.exp(res.x[k])
    print(f"\nPrimary NB2 model converged: {res.success}. Dispersion alpha = {alpha_hat:.2f}")

    rng = np.random.default_rng(SEED)
    n_boot = 300
    boot_coefs = []
    idx = np.arange(n)
    for _ in range(n_boot):
        s_idx = rng.choice(idx, size=n, replace=True)
        Xb, yb = X1[s_idx], y[s_idx]

        def nll_b(params):
            beta = params[:k]
            al = np.exp(params[k])
            mu = np.clip(np.exp(Xb @ beta), 1e-8, 1e8)
            r = 1.0 / al
            ll = (gammaln(yb + r) - gammaln(r) - gammaln(yb + 1)
                  + r * np.log(r / (r + mu)) + yb * np.log(mu / (r + mu)))
            return -np.sum(ll)

        r2 = optimize.minimize(nll_b, res.x, method="Nelder-Mead",
                                options={"maxiter": 8000, "xatol": 1e-5, "fatol": 1e-5})
        if r2.success:
            boot_coefs.append(r2.x[:k])
    boot_coefs = np.array(boot_coefs)

    names = ["intercept", "year_c", "is_open_access", "has_digital", "has_social"]
    rows = []
    for i, name in enumerate(names):
        se = boot_coefs[:, i].std()
        z = beta_hat[i] / se
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        lo, hi = np.percentile(boot_coefs[:, i], [2.5, 97.5])
        rows.append({"variable": name, "coef_log": beta_hat[i], "IRR": np.exp(beta_hat[i]),
                     "bootstrap_SE": se, "z": z, "p_value": p,
                     "CI_low": np.exp(lo), "CI_high": np.exp(hi)})
    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT_DIR / "regression_negative_binomial_primary.csv", index=False)
    print(out.to_string(index=False))


def log1p_ols_robustness(full):
    full = full.copy()
    full["log_cites"] = np.log1p(full["Citing Works Count"])
    X = full[["year_c", "is_open_access", "has_digital", "has_social"]].values
    X1 = np.column_stack([np.ones(len(X)), X])
    y = full["log_cites"].values
    n, k = X1.shape

    coef, _, _, _ = np.linalg.lstsq(X1, y, rcond=None)
    resid = y - X1 @ coef
    sigma2 = np.sum(resid ** 2) / (n - k)
    xtx_inv = np.linalg.inv(X1.T @ X1)
    se = np.sqrt(np.diag(xtx_inv) * sigma2)

    names = ["intercept", "year_c", "is_open_access", "has_digital", "has_social"]
    rows = []
    for i, name in enumerate(names):
        t = coef[i] / se[i]
        p = 2 * (1 - stats.t.cdf(abs(t), df=n - k))
        rows.append({"variable": name, "coef": coef[i], "SE": se[i], "t": t, "p_value": p})
    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT_DIR / "regression_log1p_ols_robustness.csv", index=False)
    print("\nLog1p OLS robustness check:")
    print(out.to_string(index=False))


def main():
    df = pd.read_csv(FILTERED_CSV)
    full = build_covariates(df)
    print(f"n = {len(full)} documents (excludes partial-year 2026)\n")
    poisson_preliminary(full)
    negative_binomial_primary(full)
    log1p_ols_robustness(full)


if __name__ == "__main__":
    main()
