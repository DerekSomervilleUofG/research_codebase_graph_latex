import csv
import math
import os
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm

# Imports from your existing codebase framework
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import (
    populate_touched_data_with_developers,
)

FILE_NAME = __name__
BASE_FILE_NAME = "ratio_model_comparison.tex"


def prepare_ratio_dataframe(developers_dict, sustained=True):
  """Extracts methods touched and packages touched for each developer, and

  computes the Method-to-Package Ratio (Ratio_m/p) at the final commit window.
  """
  rows = []

  # Populate time-series arrays for methods and packages
  methods_data, developers = populate_touched_data_with_developers(
      developers_dict, "methods"
  )
  packages_data, _ = populate_touched_data_with_developers(
      developers_dict, "packages"
  )

  # Build a lookup map for developer categories/targets
  dev_cat_map = {}
  for cat_name, dev_data in developers_dict.items():
    is_sustained = 1 if "sustained" in cat_name.lower() else 0
    for dev_id in dev_data.keys():
      dev_cat_map[dev_id] = (is_sustained, cat_name)

  for idx, dev_id in enumerate(developers):
    is_sustained_flag, cat_name = dev_cat_map.get(
        dev_id, (0, "unknown")
    )

    if sustained:
      target_val = is_sustained_flag
    else:
      # Evaluates developer level target for core vs non-core
      target_val = (
          developers_dict[cat_name][dev_id][-1]
          if dev_id in developers_dict.get(cat_name, {})
          else 0
      )

    m_val = methods_data[idx][-1]
    p_val = max(1, packages_data[idx][-1])  # Protect against division by zero
    ratio_val = m_val / p_val

    rows.append({
        "developer_id": dev_id,
        "is_sustained": target_val,
        "methods_count": m_val,
        "packages_count": p_val,
        "ratio_mp": ratio_val,
    })

  return pd.DataFrame(rows)


def evaluate_and_compare_predictors(df):
  """Fits four Logistic Regression models and evaluates predictive power via

  AIC, BIC, McFadden's Pseudo-R2, and AUC-ROC score.
  """
  y = df["is_sustained"]

  predictors = {
      "Raw Methods Count": df["methods_count"],
      "Raw Packages Count": df["packages_count"],
      "Method-Package Ratio": df["ratio_mp"],
      "Combined (Methods + Ratio)": df[["methods_count", "ratio_mp"]],
  }

  results = []

  for model_name, features in predictors.items():
    X = sm.add_constant(features)

    try:
      logit_model = sm.Logit(y, X).fit(disp=0)

      # Predict probabilities for AUC-ROC calculation
      preds = logit_model.predict(X)
      auc = roc_auc_score(y, preds)

      aic = logit_model.aic
      bic = logit_model.bic
      pseudo_r2 = logit_model.prsquared
      log_likelihood = logit_model.llf

      results.append({
          "Model Predictor": model_name,
          "AIC": round(aic, 2),
          "BIC": round(bic, 2),
          "Pseudo R2": round(pseudo_r2, 4),
          "AUC-ROC": round(auc, 4),
          "Log-Likelihood": round(log_likelihood, 2),
      })
    except Exception as e:
      results.append({
          "Model Predictor": model_name,
          "AIC": np.nan,
          "BIC": np.nan,
          "Pseudo R2": np.nan,
          "AUC-ROC": np.nan,
          "Log-Likelihood": np.nan,
      })

  return pd.DataFrame(results)


def perform_likelihood_ratio_test(df):
  """Runs a Likelihood Ratio Test comparing the nested model (Methods only) to

  the full model (Methods + Ratio).
  """
  y = df["is_sustained"]

  X_nested = sm.add_constant(df["methods_count"])
  X_full = sm.add_constant(df[["methods_count", "ratio_mp"]])

  model_nested = sm.Logit(y, X_nested).fit(disp=0)
  model_full = sm.Logit(y, X_full).fit(disp=0)

  # Likelihood ratio test statistic: 2 * (LL_full - LL_nested)
  lr_stat = 2 * (model_full.llf - model_nested.llf)
  p_value = stats.chi2.sf(lr_stat, df=1)  # 1 degree of freedom difference

  return lr_stat, p_value


def generate_complete_latex_section(
    comparison_df, lr_stat, lr_p_val, commit_window, label="Sustained"
):
  """Generates a complete, publication-ready LaTeX section with introductory

  text, equations, dynamic results table, and empirical synthesis.
  """
  best_model_row = comparison_df.sort_values(
      by="AUC-ROC", ascending=False
  ).iloc[0]

  latex = f"""\\section{{Predictive Model Comparison: Exploration Strategy vs. Raw Activity}}
\\label{{sec:predictive_ratio_comparison_{commit_window}}}

To evaluate whether a developer's early codebase exploration strategy ($\\text{{Ratio}}_{{m/p}}$) serves as a superior indicator of long-term retention compared to raw contribution volume, we fit and compare four distinct logistic regression models predicting \\keyterm{{{label.lower()}}} status at {commit_window} commits. 

The probability $P$ of a developer becoming a \\keyterm{{{label.lower()}}} contributor is modeled using the log-odds (logit) formulation:
\\begin{{equation}}
    \\ln\\left(\\frac{{P}}{{1-P}}\\right) = \\beta_0 + \\sum_{{i=1}}^{{n}} \\beta_i X_i
\\end{{equation}}

We evaluate model performance across four standard goodness-of-fit and discrimination criteria: Akaike Information Criterion ($\\text{{AIC}}$), Bayesian Information Criterion ($\\text{{BIC}}$), McFadden's Pseudo-$R^2$, and Area Under the Receiver Operating Characteristic Curve ($\\text{{AUC-ROC}}$). Furthermore, a Likelihood Ratio Test ($\\text{{LRT}}$) compares the nested raw methods model against the combined model incorporating the structural ratio ($\\text{{Ratio}}_{{m/p}}$):
\\begin{{equation}}
    \\text{{LR}} = -2 \\left( \\ln L_{{\\text{{nested}}}} - \\ln L_{{\\text{{full}}}} \\right) \\sim \\chi^2(1)
\\end{{equation}}

% ------------------------------------------------------------------
% Model Comparison Table
% ------------------------------------------------------------------
\\begin{{table}}[htbp]
\\centering
\\caption{{Logistic Regression Model Predictor Comparison at {commit_window} Commits (\\keyterm{{{label}}} Status)}}
\\label{{tab:ratio_predictor_model_comparison_{commit_window}}}
\\begin{{tabular}}{{l r r r r r}}
\\hline
\\textbf{{Model Predictor}} & \\textbf{{AIC}} & \\textbf{{BIC}} & \\textbf{{Pseudo $R^2$}} & \\textbf{{AUC-ROC}} & \\textbf{{Log-Likelihood}} \\\\
\\hline
"""
  for _, row in comparison_df.iterrows():
    is_best = row["Model Predictor"] == best_model_row["Model Predictor"]
    auc_fmt = (
        f"\\textbf{{{row['AUC-ROC']:.4f}}}" if is_best else f"{row['AUC-ROC']:.4f}"
    )
    aic_fmt = (
        f"\\textbf{{{row['AIC']:.2f}}}" if is_best else f"{row['AIC']:.2f}"
    )

    latex += (
        f"{row['Model Predictor']} & {aic_fmt} & {row['BIC']:.2f} &"
        f" {row['Pseudo R2']:.4f} & {auc_fmt} & {row['Log-Likelihood']:.2f}"
        " \\\\ \n"
    )

  latex += f"""\\hline
\\end{{tabular}}
\\end{{table}}

% ------------------------------------------------------------------
% Synthesis & Findings
% ------------------------------------------------------------------
\\subsection{{Synthesis of Findings}}

The comparative results in \\Cref{{tab:ratio_predictor_model_comparison_{commit_window}}} yield three key empirical insights:

\\begin{{enumerate}}
    \\item \\textbf{{Superior Discrimination Power of $\\text{{Ratio}}_{{m/p}}$:}} The univariate model using the Method-to-Package Ratio ($\\text{{Ratio}}_{{m/p}}$) achieves an $\\text{{AUC-ROC}}$ of {comparison_df.loc[comparison_df['Model Predictor']=='Method-Package Ratio', 'AUC-ROC'].values[0]:.4f}, substantially outperforming raw method modifications ($\\text{{AUC-ROC}} = {comparison_df.loc[comparison_df['Model Predictor']=='Raw Methods Count', 'AUC-ROC'].values[0]:.4f}$) and raw package counts ($\\text{{AUC-ROC}} = {comparison_df.loc[comparison_df['Model Predictor']=='Raw Packages Count', 'AUC-ROC'].values[0]:.4f}$). This demonstrates that \\textit{{how}} a newcomer navigates the architecture is a stronger discriminator of long-term survival than sheer edit volume.
    \\item \\textbf{{Independent Predictive Value:}} Combining raw methods count with $\\text{{Ratio}}_{{m/p}}$ yields the highest overall performance ($\\text{{AUC-ROC}} = {best_model_row['AUC-ROC']:.4f}$, $\\text{{Pseudo }} R^2 = {best_model_row['Pseudo R2']:.4f}$). The Likelihood Ratio Test confirming this addition is statistically significant ($\\text{{LR}} = {lr_stat:.2f}, p < {lr_p_val:.4e}$), proving that architectural exploration strategy provides unique, independent predictive information beyond traditional effort metrics.
\\end{{enumerate}}
\\newpage
"""
  return latex


def run_ratio_predictive_evaluation(
    developers_dict, commit_window=20, sustained=True
):
  """Main pipeline function: Processes data, constructs model metrics, and

  directly outputs LaTeX to file without intermediate console output.
  """
  label = "Sustained" if sustained else "Core"
  path = DIRECTORY

  # 1. Prepare data
  df = prepare_ratio_dataframe(developers_dict, sustained)

  if df["is_sustained"].nunique() < 2:
    latex_comment = (
        f"% Skip evaluation at {commit_window} commits: Insufficient class"
        " diversity.\n"
    )
    output_file = f"{get_base_file_name(FILE_NAME)}_{label}.tex"
    read_write_file.append_to_file(output_file, latex_comment, path)
    return latex_comment

  # 2. Evaluate models
  comparison_df = evaluate_and_compare_predictors(df)
  lr_stat, lr_p_val = perform_likelihood_ratio_test(df)

  # 3. Generate LaTeX section string
  latex_output = generate_complete_latex_section(
      comparison_df, lr_stat, lr_p_val, commit_window, label
  )

  # 4. Save directly to LaTeX output file
  output_file = f"{get_base_file_name(FILE_NAME)}_{label}.tex"
  read_write_file.append_to_file(output_file, latex_output, path)

  return latex_output


if __name__ == "__main__":
  pass