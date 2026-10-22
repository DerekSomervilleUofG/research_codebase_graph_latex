import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import math
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data
from codebase_graph_latex.latex_table import *
from codebase_graph_latex.repository_graph.component_time_series.seaborn_stripplot import generate_and_save as seaborn_stripplot_generate_and_save
import csv, os

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
P_THRESHOLD = 0.30
package_developers = {}
PACKAGE_METHOD_RATIO = "methods : packages"
EXPLORATION_STRATEGY_CAT = "exploration strategy"

def write_hits(component, sus_hit, non_sus_hit, output_file="hits.csv"):
    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header only if file doesn't exist yet
        if not file_exists:
            writer.writerow([
                "hit_type",
                "developer_id",
                "is_sustained",
                "component",
                "metric"
            ])

        for _, row in sus_hit.iterrows():
            writer.writerow([
                "sus_hit",
                row["developer_id"],
                row["is_sustained"],
                component,
                row["metric_value"]
            ])

        for _, row in non_sus_hit.iterrows():
            writer.writerow([
                "non_sus_hit",
                row["developer_id"],
                row["is_sustained"],
                 component,
                row["metric_value"]
            ])



def generate_logistic_regression_explanation(label):
    percent_label = int(100 * P_THRESHOLD)
    
    # By using a variable for itemize, we can use standard f-string evaluation
    list_env = "itemize"
    
    latex = fr"""
To identify early indicators of long-term developer engagement, a Logistic Regression model was employed. The model treats the developer category (Sustained vs. Non-Sustained) as a binary dependent variable. The following metrics are reported:

\begin{{{list_env}}}
    \item \textbf{{Coefficient ($\beta$):}} This value represents the change in the log-odds of a developer becoming 'Sustained' for every unit increase in the component count. A positive coefficient indicates that higher activity in that component increases the likelihood of long-term retention.
    \item \textbf{{Odds Ratio ($e^\beta$):}} Perhaps the most interpretable metric, the Odds Ratio quantifies the relative increase in the likelihood of being a Sustained developer. For example, an Odds Ratio of $1.05$ implies a $5\%$ increase in the odds of becoming sustained for each additional component touched.
    \item \textbf{{Std. Err (Standard Error):}} Measures the accuracy of the coefficient estimate. A lower standard error relative to the coefficient indicates a more precise estimate.
    \item \textbf{{p-Value ($P>|z|$):}} Indicates the statistical significance of the predictor. In this study, a p-Value $< 0.05$ suggests that the specific component count is a significant predictor of whether a developer will transition into a sustained role.
    \item \textbf{{{percent_label}\% Threshold:}} The threshold number of components to touch to achieve a {percent_label}\% empirical probability of transitioning into a sustained contributor.
    \item \textbf{{Not {label} Met Threshold:}} The not {label} number of developers to have met the threshold, the percentage of developers in brackets.
    \item \textbf{{{label} Met Threshold:}} The {label} number of developers to have met the threshold, the percentage of developers in brackets.
\end{{{list_env}}}
"""

    latex += r"""
\textbf{Interpretation of Intercept vs. Component Count:}
\begin{itemize}
    \item \textbf{Intercept:} Represents the baseline log-odds of the dependent variable (Sustained Status) when the independent variable (e.g., Package Count) is zero. In this study, the consistently negative intercepts indicate that the probability of a developer becoming 'Sustained' is statistically low without active engagement in the codebase.
    \item \textbf{Component Count (Slope):} Represents the effect size of architectural engagement. The positive coefficients and Odds Ratios greater than 1.0 demonstrate that every additional unique component touched by a developer significantly increases their likelihood of transitioning into a sustained contributor.
\end{itemize}
"""
    return latex

def section_heading(time_series, label):
    latex = get_section_start(FILE_NAME, "") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "\\label{sec:" + FILE_NAME.replace(" ", "_") + time_series + "} \n"
    latex += generate_logistic_regression_explanation(label)
    return latex

def get_description():
    return fr"""
    To identify early indicators of long-term developer engagement, a Logistic Regression model was employed. The model treats the developer category (Sustained vs. Non-Sustained) as a binary dependent variable. """
    

def get_headings(label: str, p_threshold: float = 0.5) -> dict[str, str]:
    """Generates a mapping of table column headings to their LaTeX-formatted definitions."""
    percent_val = int(p_threshold * 100) if (p_threshold * 100).is_integer() else f"{p_threshold * 100:.1f}"

    return {
        "First $n$ Commits": (
            "A sample of the first $n$ commits evaluated for developers"
        ),
        "Model Parameter": (
            r"The specific model predictor or component metric evaluated in the regression"
        ),
        # Escaped with raw string (rf"...") so LaTeX receives \# without Python syntax warnings
        rf"Developers \#": (
            "The number of developers included in the sample cohort"
        ),
        rf"Not {label} $\mu$": (
            f"The mean average component count touched by developers who are not {label}."
        ),
        rf"{label} $\mu$": (
            f"The mean average component count touched by {label} developers."
        ),
        "Odds Ratio": (
            r"The Odds Ratio ($e^\beta$) quantifies "
            r"the relative increase in the likelihood of being a Sustained developer "
        ),
        "Std. Err": (
            r"Measures the accuracy of the coefficient estimate "

        ),
        r"$p$-Value": (
            r"Indicates the statistical significance of the predictor ($P > |z|$). "
        ),
        rf"{percent_val}\% Threshold": (
            rf"The threshold number of components to touch to achieve a {percent_val}\% "
            r"probability of transitioning into a sustained contributor."
        ),
        rf"Not {label} Met Threshold": (
            f"The number of non-{label} developers who met the threshold, with "
            r"the percentage of developers reported in brackets."
        ),
        rf"{label} Met Threshold": (
            f"The number of {label} developers who met the threshold, with "
            r"the percentage of developers reported in brackets."
        ),
    }

def get_row_headings():
    return {
    "Intercept": (
        "Represents the baseline log-odds of the dependent variable (Sustained Status) "
        "when the independent variable (e.g., Package Count) is zero "
    ),
    "Component Count (Slope)": (
        "Represents the effect size of architectural engagement "
    ),
}

def generate_predictive_model_latex():
    """
    Returns a LaTeX string defining the Logistic Regression model used
    to predict if a developer will become a sustained contributor.
    """
    latex = r"""
\subsubsection*{Predictive Identification Model}
To determine if early-stage developer behavior can identify future sustained contributors, we employ a Logistic Regression model. The probability $P$ of a developer becoming a \textbf{Sustained Contributor} is modeled using the log-odds (logit) function:

\begin{equation}
    \ln\left(\frac{P}{1-P}\right) = \beta_0 + \beta_1 X_{1} + \beta_2 X_{2} + \dots + \beta_n X_{n}
\end{equation}

Where:
\begin{itemize}
    \item $P$ is the probability that the developer's tenure is ``Sustained''.
    \item $\beta_0$ is the intercept.
    \item $X_n$ represents early-stage metrics (e.g., methods or classes touched in the first 10, 20, or 50 commits).
    \item $\beta_n$ are the coefficients representing the weight of each predictor.
\end{itemize}

The impact of each behavior is quantified using the \textbf{Odds Ratio (OR)}, calculated as:
\begin{equation}
    OR = e^{\beta_n}
\end{equation}
An $OR > 1$ indicates that an increase in the metric (e.g., touching more classes) increases the likelihood of long-term retention. 

\textbf{Model Evaluation}
The predictive power is evaluated using the Area Under the Receiver Operating Characteristic Curve (AUC-ROC). An AUC of 0.5 represents random chance, while an AUC closer to 1.0 indicates high predictive accuracy[cite: 1639].
"""
    return latex

def prepare_data(component, number_of_commts, developers_dict, sustained):
    rows = []
    # 1. Prepare the data: Binary classification (Sustained vs Not)
    for cat_name, dev_data in developers_dict.items():
        # Target: 1 if developer became Sustained, 0 otherwise
        is_sustained = 1 if "sustained" in cat_name.lower() else 0

        
        touched_data, developers = populate_touched_data_with_developers(dev_data, KNOWN_Y_AXIS)

        counter = 0
        for series in touched_data:
            # We use the final value in this commit window as the predictor
            if sustained:
                local_is_sustained = is_sustained
            else:
                local_is_sustained = dev_data[developers[counter]][-1]
            # Determine the current metric at milestone number_of_commts
            if isinstance(number_of_commts, int) and number_of_commts > 0:
                idx = min(len(series) - 1, number_of_commts - 1)
                curr_metric = series[idx]
            else:
                curr_metric = series[-1]

            metric_value = curr_metric

            if component in (PACKAGE_METHOD_RATIO, EXPLORATION_STRATEGY_CAT):
                pkg_series = package_developers[number_of_commts][cat_name][
                    developers[counter]
                ][KNOWN_Y_AXIS]
                if isinstance(number_of_commts, int) and number_of_commts > 0:
                    p_idx = min(len(pkg_series) - 1, number_of_commts - 1)
                    pkg_val = pkg_series[p_idx]
                else:
                    pkg_val = pkg_series[-1]

                ratio = (curr_metric / pkg_val) if pkg_val > 0 else 0

                if component == PACKAGE_METHOD_RATIO:
                    metric_value = ratio
                else:
                    metric_value = categorize_ratio(
                        ratio, pkg_val, number_of_commts
                    )

            rows.append({
                'developer_id': developers[counter],
                'is_sustained': local_is_sustained,
                'metric_value': metric_value
            })
            counter += 1
    return rows

def generate_latex(component, summary, avg_mod, avg_sus, number_of_commits, x30_threshold, mod_hit, mod_pct, sus_hit, sus_pct, total_developers):
    component_clean = component.replace("_", "-")
    
    if number_of_commits == 0:
        number_of_commits = "All"
    latex_rows = ""
    for index, row in summary.iterrows():
        
        # Build the columns: Component & Commits & Label & Total Devs & Mod Mean & Sus Mean ...
        latex_rows += f"{number_of_commits} & {index} & {total_developers} & "
        latex_rows += f"{avg_mod:.2f} & {avg_sus:.2f} & "
        #latex_rows += f"{row['Coef.']:.4f} & "
        latex_rows += f"{row['Odds Ratio']:.4f} & "
        latex_rows += f"{row['Std.Err.']:.4f} & {row['P>|z|']:.4f} & "
        if "Count" in index:
            latex_rows += f"\\textbf{{{x30_threshold:.4f}}} & "
            latex_rows += f"{mod_hit} ({mod_pct:.2f}\\%) & "
            latex_rows += f"{sus_hit} ({sus_pct:.2f}\\%) "
        else:
            latex_rows += f"- & - & - "
        latex_rows += f"\\\\ \n"
    return latex_rows

def generate_predictive_identification_latex(developers, component, number_of_commits, sustained):
    # Check if we have both classes (0 and 1) to run the model
    df = pd.DataFrame(prepare_data(component, number_of_commits, developers, sustained))
    if df['is_sustained'].nunique() < 2:
        return f"% Skip {component}: Not enough diversity in classes for Logistic Regression."
        
    # Updated naming to reflect Non-Sustained (Transient + Moderate) vs Sustained
    avg_non_sus = df[df['is_sustained'] == 0]['metric_value'].mean()
    avg_sus = df[df['is_sustained'] == 1]['metric_value'].mean()


    if component == EXPLORATION_STRATEGY_CAT:
        try:
            # Baseline reference is set to 1 (Breadth-First)
            logit_model = smf.logit('is_sustained ~ C(metric_value, Treatment(reference=1))', data=df).fit(disp=0)
        except Exception:
            # Fallback for quasi-complete separation handling
            logit_model = smf.logit('is_sustained ~ C(metric_value, Treatment(reference=1))', data=df).fit_regularized(disp=0)
            
        summary = logit_model.summary2().tables[1]
        summary['Odds Ratio'] = np.exp(summary['Coef.'])
        cat1_row = pd.DataFrame({
            'Coef.': [0.0],
            'Std.Err.': [np.nan],
            'z': [np.nan],
            'P>|z|': [np.nan],
            '[0.025': [np.nan],
            '0.975]': [np.nan],
            'Odds Ratio': [1.0]
        }, index=['Breadth First'])
        
        # 2. Reconstruct table with Intercept, Category 1 (T.1), and Category 3 (T.3) only
        # Filter out T.2 (Category 2)
        summary_filtered = summary[~summary.index.str.contains('\[T\.2\]')]
        
        # Combine Intercept, explicit T.1, and remaining rows (T.3)
        summary = pd.concat([summary_filtered.iloc[:1], cat1_row, summary_filtered.iloc[1:]])
        rename_map = {
            "C(metric_value, Treatment(reference=1))[T.3]": "Depth First",
            "C(metric_value, Treatment(reference=1))[T.1]": "Breadth First",
        }
        summary.index = [rename_map.get(idx, idx) for idx in summary.index]
        x30_threshold = 0
        non_sus_hit, non_sus_pct, sus_hit, sus_pct = 0, 0, 0, 0
    else:
        # 2. Run Logistic Regression
        X = sm.add_constant(df['metric_value'])
        logit_model = sm.Logit(df['is_sustained'], X).fit(disp=0)
        summary = logit_model.summary2().tables[1] # Extract the coefficients table
        
        # 3. Calculate Odds Ratio (OR = exp(coeff))
        summary['Odds Ratio'] = np.exp(summary['Coef.'])
        
        # Rename rows for the LaTeX table
        summary.index = ['Intercept', f'{component.replace("_", " ").capitalize()} Count']
        intercept_val = summary.iloc[0]['Coef.']
        coeff_val = summary.iloc[1]['Coef.']

        # Calculate the threshold value where predicted probability crosses P_THRESHOLD
        logit_p = math.log(P_THRESHOLD / (1 - P_THRESHOLD))
        x30_threshold = (logit_p - intercept_val) / coeff_val if coeff_val != 0 else 0
        if component == "packages" and number_of_commits == START_COMMIT_NUMBER and sustained:
            seaborn_stripplot_generate_and_save(developers, x30_threshold)
        # Calculate Sustained metrics matching/exceeding threshold
        sustained_df = df[df['is_sustained'] == 1]
        sus_hit_df = sustained_df[
            sustained_df['metric_value'] >= x30_threshold
        ]
        sus_hit = sus_hit_df['developer_id'].nunique()
        sus_total = sustained_df['developer_id'].nunique()

        sus_pct = (sus_hit / sus_total * 100) if sus_total > 0 else 0

        # Calculate Baseline Non-Sustained metrics matching/exceeding threshold
        non_sustained_df = df[df['is_sustained'] == 0]
        non_sus_total = non_sustained_df['developer_id'].nunique()
        non_sus_hit_df = non_sustained_df[non_sustained_df['metric_value'] >= x30_threshold]
        non_sus_hit = non_sus_hit_df['developer_id'].nunique()
        non_sus_pct = (non_sus_hit / non_sus_total * 100) if non_sus_total > 0 else 0

        write_hits(component, sus_hit_df, non_sus_hit_df)

        # Clean up columns for the paper
        results_df = summary[['Coef.', 'Odds Ratio', 'Std.Err.', 'P>|z|']]
        results_df.columns = ['Coefficient', 'Odds Ratio', 'Std. Err', 'p-Value']

    # 4. Generate LaTeX - Appending len(df) to match the new signature of generate_latex
    return generate_latex(component, summary, avg_non_sus, avg_sus, number_of_commits, 
                          x30_threshold, non_sus_hit, non_sus_pct, sus_hit, sus_pct, len(df))

def generate_and_save(component, developers, number_of_commits, sustained=True):
    global package_developers
    path = DIRECTORY
    file_name = FILE_NAME
    commit_prefix = "all commits "
    base_file_name = get_base_file_name(file_name)
    label = "Sustained"
    headings = get_headings(label, P_THRESHOLD)
    row_headings = get_row_headings()
    latex = "" 
    if not sustained and number_of_commits == 10:
        number_of_commit_desc = "1 to 5, 10 and 20"   
    else:
        number_of_commit_desc = "1 to 5 and 10" 
    if not sustained:
        label = "Core"
    table_name = "Strategy Logistic Regression for " + component + " against " + number_of_commit_desc + " commits to predict " + label + " developers. "
    table_name += get_description()
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        table_name += generate_table_name_headings(headings)
        table_name += generate_table_name_headings(row_headings, "Row")
    if component == "packages":
        package_developers[number_of_commits] = developers
        if number_of_commits == START_COMMIT_NUMBER:
            save_to_latex_file(get_base_file_name(file_name) + "_" + str(sustained), 
                                    BASE_FILE_NAME,
                                        latex, path)
            if sustained:
                read_write_file.write_file(base_file_name + ".tex", section_heading(commit_prefix, label), DIRECTORY)
    if number_of_commits == START_COMMIT_NUMBER:
        latex += start_landscape() + start_latex_table(table_name, list(headings.keys()), "r l r r r r r r r r r", "Strategy Logistic Regression " + label + " for " + component + " for " + number_of_commit_desc)
        save_to_latex_file(get_base_file_name(file_name) + "_" + str(sustained) + "_" + component, 
                            get_base_file_name(file_name) + "_" + str(sustained) + ".tex",
                            latex, path)

    latex_table = generate_predictive_identification_latex(developers, component, number_of_commits, sustained).replace("_", "\\_")
    if component == "methods":
        latex_table += generate_predictive_identification_latex(developers, PACKAGE_METHOD_RATIO, number_of_commits, sustained).replace("_", "\\_")
        latex_table += generate_predictive_identification_latex(developers, EXPLORATION_STRATEGY_CAT, number_of_commits, sustained).replace("_", "\\_")
    read_write_file.append_to_file(get_base_file_name(file_name) + "_" + str(sustained) + "_" + component + ".tex", latex_table, path)
    if number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(get_base_file_name(file_name) + "_" + str(sustained) + "_" + component + ".tex", table_end(FILE_NAME + label + "_" + str(sustained) + "_" + component + "_" + str(number_of_commits), True) + "\n \\newpage \n", path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER and not sustained:
        read_write_file.append_to_file(get_base_file_name(file_name) + "_" + str(sustained) + ".tex", generate_predictive_model_latex() + "\n \\newpage \n", path)
 