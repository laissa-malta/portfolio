# run_analysis.py
# -*- coding: utf-8 -*-
"""
Gender & Income Inequality in Brazil (Open Data Case)
----------------------------------------------------
A reproducible statistical analysis using Python.
It covers:
 - Data loading (from Base dos Dados or local CSV)
 - Data cleaning and feature engineering
 - Descriptive statistics
 - Hypothesis testing (t-test, Mann–Whitney)
 - Linear regression (OLS with robust SE)
 - Visualization and report generation
Author: Laíssa Lima
"""

# ======================================================
# Imports
# ======================================================
import os
import json
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

# ======================================================
# Config
# ======================================================
sns.set(style="whitegrid", palette="Set2", font_scale=1.1)
plt.rcParams["figure.figsize"] = (7, 5)

# ======================================================
# Directory setup
# ======================================================
def ensure_dirs():
    for d in ["data/raw", "data/processed", "figures", "report"]:
        Path(d).mkdir(parents=True, exist_ok=True)

# ======================================================
# Data loading
# ======================================================
def load_data(year, limit, billing_project, local_csv):
    """Try to load from Base dos Dados, else from local CSV."""
    try:
        from basedosdados import read_sql
        if billing_project:
            query = f"""
            SELECT ano, uf, sexo, cor_raca, idade, anos_estudo, renda_trabalho_principal
            FROM `basedosdados.br_ibge_pnadc.microdados`
            WHERE ano = {year} AND renda_trabalho_principal IS NOT NULL
            LIMIT {limit}
            """
            print("Loading data from Base dos Dados...")
            df = read_sql(query, billing_project_id=billing_project)
            return df, "basedosdados"
    except Exception:
        pass

    # Fallback to local CSV
    if Path(local_csv).exists():
        print("Loading data from local CSV...")
        return pd.read_csv(local_csv), "local_csv"

    raise FileNotFoundError(
        "No data source available. Provide --billing_project or a local CSV file."
    )

# ======================================================
# Cleaning
# ======================================================
def clean_data(df):
    """Basic cleaning, variable labeling, and feature creation."""
    df = df.dropna(subset=["sexo", "cor_raca", "idade", "anos_estudo", "renda_trabalho_principal"]).copy()
    df = df[df["renda_trabalho_principal"] > 0].copy()

    # Winsorize income (1–99%)
    low, high = df["renda_trabalho_principal"].quantile([0.01, 0.99])
    df["income_winsorized"] = df["renda_trabalho_principal"].clip(lower=low, upper=high)

    # Gender and race labels
    df["gender"] = df["sexo"].map({1: "Male", 2: "Female"}).fillna("Other")
    df["race"] = df["cor_raca"].map({
        1: "White", 2: "Black", 3: "Yellow", 4: "Brown", 5: "Indigenous"
    }).fillna("Other")

    # Numeric conversions
    df["age"] = pd.to_numeric(df["idade"], errors="coerce")
    df["school_years"] = pd.to_numeric(df["anos_estudo"], errors="coerce")
    df["log_income"] = np.log(df["income_winsorized"])

    # Dummies
    df["is_female"] = (df["gender"] == "Female").astype(int)
    for r in ["Black", "Brown", "Yellow", "Indigenous"]:
        df[f"race_{r.lower()}"] = (df["race"] == r).astype(int)

    df["age2"] = df["age"] ** 2
    return df

# ======================================================
# Descriptive stats
# ======================================================
def descriptive_stats(df):
    desc_gender = df.groupby("gender")["income_winsorized"].agg(["count", "mean", "median", "std"]).reset_index()
    desc_race = df.groupby("race")["income_winsorized"].agg(["count", "mean", "median", "std"]).reset_index()
    overall = df["income_winsorized"].describe(percentiles=[0.25, 0.5, 0.75]).to_frame().T
    return {"overall": overall, "by_gender": desc_gender, "by_race": desc_race}

# ======================================================
# Hypothesis tests
# ======================================================
def hypothesis_tests(df):
    males = df.loc[df["gender"] == "Male", "income_winsorized"]
    females = df.loc[df["gender"] == "Female", "income_winsorized"]

    t_stat, t_p = stats.ttest_ind(males, females, equal_var=False, nan_policy="omit")
    mw_stat, mw_p = stats.mannwhitneyu(males, females, alternative="two-sided")

    return {
        "t_test": {"stat": float(t_stat), "p_value": float(t_p), "H0": "mean_male == mean_female"},
        "mann_whitney": {"stat": float(mw_stat), "p_value": float(mw_p), "H0": "distributions_equal"}
    }

# ======================================================
# Regression
# ======================================================
def regression_model(df):
    X = df[[
        "is_female", "race_black", "race_brown", "race_yellow", "race_indigenous",
        "school_years", "age", "age2"
    ]].copy()
    X = sm.add_constant(X, has_constant="add")
    y = df["log_income"]

    model = sm.OLS(y, X, missing="drop").fit(cov_type="HC1")
    return model

# ======================================================
# Visualization
# ======================================================
def plot_income_box(df, path):
    plt.figure()
    sns.boxplot(data=df, x="gender", y="income_winsorized",
                palette={"Male": "#4C72B0", "Female": "#55A868"}, showfliers=False)
    plt.title("Income distribution by gender — men earn more on average")
    plt.xlabel("")
    plt.ylabel("Monthly income (R$)")
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

def plot_edu_scatter(df, path):
    plt.figure()
    sns.regplot(data=df, x="school_years", y="log_income",
                scatter_kws={"s": 40, "alpha": 0.7, "color": "#4C72B0"},
                line_kws={"color": "#E17C05", "linewidth": 2})
    plt.title("Education vs Income — higher education levels lead to higher income")
    plt.xlabel("Years of education")
    plt.ylabel("Log of monthly income (winsorized)")
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

def plot_corr_heatmap(df, path):
    cols = ["income_winsorized", "log_income", "is_female",
            "race_black", "race_brown", "race_yellow", "race_indigenous",
            "school_years", "age", "age2"]
    corr = df[cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="YlGnBu",
                linewidths=0.5, cbar_kws={"label": "Pearson correlation"})
    plt.title("Correlation between income, education, and demographics")
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

# ======================================================
# Report summary
# ======================================================
def write_summary(desc, tests, model, outpath, nrows):
    lines = [
        "# Statistical Summary — Gender & Income Inequality\n",
        f"Total observations analyzed: **{nrows:,}**\n",
        "## Descriptive statistics\n",
        "### Overall\n",
        desc["overall"].round(2).to_markdown(index=False),
        "\n### By gender\n",
        desc["by_gender"].round(2).to_markdown(index=False),
        "\n### By race\n",
        desc["by_race"].round(2).to_markdown(index=False),
        "\n## Hypothesis tests\n",
        f"- Welch t-test (Male vs Female): **t={tests['t_test']['stat']:.3f}**, **p={tests['t_test']['p_value']:.4f}**",
        f"- Mann–Whitney: **U={tests['mann_whitney']['stat']:.3f}**, **p={tests['mann_whitney']['p_value']:.4f}**",
        "\n## Linear regression (log of income)\n",
        "Model: `log_income ~ gender + race + school_years + age + age²`\n",
        "```\n" + model.summary().as_text() + "\n```"
    ]
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ======================================================
# Main
# ======================================================
def main():
    parser = argparse.ArgumentParser(description="Gender & Income Inequality Analysis (Open Data)")
    parser.add_argument("--year", type=int, default=2022)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--billing_project", type=str, default="")
    parser.add_argument("--local_csv", type=str, default="data/raw/data.csv")
    args = parser.parse_args()

    ensure_dirs()
    df, source = load_data(args.year, args.limit, args.billing_project, args.local_csv)

    df = clean_data(df)
    desc = descriptive_stats(df)
    tests = hypothesis_tests(df)
    model = regression_model(df)

    # Save summary tables
    desc["by_gender"].to_csv("report/descriptive_by_gender.csv", index=False)
    desc["by_race"].to_csv("report/descriptive_by_race.csv", index=False)
    desc["overall"].to_csv("report/descriptive_overall.csv", index=False)
    with open("report/test_results.json", "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2)

    # Plots
    plot_income_box(df, "figures/income_by_gender.png")
    plot_edu_scatter(df, "figures/education_vs_income.png")
    plot_corr_heatmap(df, "figures/correlation_matrix.png")

    # Report
    write_summary(desc, tests, model, "report/summary.md", len(df))

    print("✅ Analysis completed successfully.")
    print("Source:", source)
    print("Figures saved in /figures, reports in /report")

if __name__ == "__main__":
    main()
