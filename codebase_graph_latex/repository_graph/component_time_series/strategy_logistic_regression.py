import pandas as pd
import statsmodels.api as sm
import numpy as np
import math
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
def generate_logistic_regression_explanation():
    latex = r"""
To identify early indicators of long-term developer engagement, a Logistic Regression model was employed. The model treats the developer category (Sustained vs. Non-Sustained) as a binary dependent variable. The following metrics are reported:

\begin{itemize}
    \item \textbf{Coefficient ($\beta$):} This value represents the change in the log-odds of a developer becoming 'Sustained' for every unit increase in the component count. A positive coefficient indicates that higher activity in that component increases the likelihood of long-term retention.
    \item \textbf{Odds Ratio ($e^\beta$):} Perhaps the most interpretable metric, the Odds Ratio quantifies the relative increase in the likelihood of being a Sustained developer. For example, an Odds Ratio of $1.05$ implies a $5\%$ increase in the odds of becoming sustained for each additional component touched.
    \item \textbf{Std. Err (Standard Error):} Measures the accuracy of the coefficient estimate. A lower standard error relative to the coefficient indicates a more precise estimate.
    \item \textbf{p-Value ($P>|z|$):} Indicates the statistical significance of the predictor. In this study, a p-Value $< 0.05$ suggests that the specific component count is a significant predictor of whether a developer will transition into a sustained role.
    \item \textbf{50\% Threshold:} The threshold number of components to touch to have a 50% chance of becoming a sustained developer.
    \item \textbf{Moderate Met Threshold:} The moderate number of developers to have met the threshold, the percentate of developers in brackets.
    \item \textbf{Sustained Met Threshold:} The sustained number of developers to have met the threshold, the percentate of developers in brackets.
    
\end{itemize}
"""

    latex += r"""
\textbf{Interpretation of Intercept vs. Component Count:}
\begin{itemize}
    \item \textbf{Intercept:} Represents the baseline log-odds of the dependent variable (Sustained Status) when the independent variable (e.g., Package Count) is zero. In this study, the consistently negative intercepts indicate that the probability of a developer becoming 'Sustained' is statistically low without active engagement in the codebase.
    \item \textbf{Component Count (Slope):} Represents the effect size of architectural engagement. The positive coefficients and Odds Ratios greater than 1.0 demonstrate that every additional unique component touched by a developer significantly increases their likelihood of transitioning into a sustained contributor.
\end{itemize}
"""
    return latex

def section_sub_heading(time_series):
    latex = "\\begin{landscape}\n"
    latex += get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += generate_logistic_regression_explanation()
    return latex

def generate_predictive_model_latex():
    """
    Returns a LaTeX string defining the Logistic Regression model used
    to predict if a developer will become a sustained contributor.
    """
    latex = r"""
\subsubsection*{Predictive Identification Model}
To determine if early-stage developer behavior can identify future sustained contributors, we employ a Logistic Regression model. The probability $P$ of a developer becoming a \textbf{Sustained Contributor} is modeled using the log-odds (logit) function:

\begin{equation}
    \ln\left(\frac{P}{1-P}\right) = \beta_0 + \beta_1 X_{1} + \beta_2 X_{2} + \dots + \beta_n X_{n} + \epsilon
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

\paragraph{Model Evaluation}
The predictive power is evaluated using the Area Under the Receiver Operating Characteristic Curve (AUC-ROC). An AUC of 0.5 represents random chance, while an AUC closer to 1.0 indicates high predictive accuracy.
"""
    return latex

def prepare_data(developers_dict, unit):
    rows = []
    # 1. Prepare the data: Binary classification (Sustained vs Not)
    for cat_name, dev_data in developers_dict.items():
        # Target: 1 if developer became Sustained, 0 otherwise
        is_sustained = 1 if "sustained" in cat_name.lower() else 0
        
        touched_data = populate_touched_data(dev_data)
        
        for series in touched_data:
            # We use the final value in this commit window as the predictor
            rows.append({
                'is_sustained': is_sustained,
                'metric_value': series[-1]
            })
    return rows

def generate_latex(component, summary, avg_mod, avg_sus, number_of_commits, x30_threshold, mod_hit, mod_pct, sus_hit, sus_pct):
    component_clean = component.replace("_", "-")
    
    if number_of_commits == 0:
        number_of_commits = "All"
    latex_rows = ""
    for index, row in summary.iterrows():
        
        # Build the columns: Commits & Label & Coeff & OR & StdErr & P
        latex_rows += f"{component_clean} & {number_of_commits} & {index} & "
        latex_rows += f"{avg_mod:.2f} & {avg_sus:.2f} & "
        latex_rows += f"{row['Coef.']:.4f} & {row['Odds Ratio']:.4f} & "
        latex_rows += f"{row['Std.Err.']:.4f} & {row['P>|z|']:.4f} & "
        if "Count" in index:
            latex_rows += f"\\textbf{{{x30_threshold:.4f}}} & "
            latex_rows += f"{mod_hit} ({mod_pct:.1f}\\%) & "
            latex_rows += f"{sus_hit} ({sus_pct:.1f}\\%) "
        else:
            latex_rows += f"- & - & - "
        latex_rows += f"\\\\ \n"
    return latex_rows

def generate_predictive_identification_latex(df, component, number_of_commits):
    
    
    
    # Check if we have both classes (0 and 1) to run the model
    if df['is_sustained'].nunique() < 2:
        return f"% Skip {component}: Not enough diversity in classes for Logistic Regression."
    avg_mod = df[df['is_sustained'] == 0]['metric_value'].mean()
    avg_sus = df[df['is_sustained'] == 1]['metric_value'].mean()

    # 2. Run Logistic Regression
    # Y = is_sustained, X = metric_value (e.g., methods touched)
    X = sm.add_constant(df['metric_value'])
    logit_model = sm.Logit(df['is_sustained'], X).fit(disp=0)
    summary = logit_model.summary2().tables[1] # Extract the coefficients table
    
    # 3. Calculate Odds Ratio (OR = exp(coeff))
    summary['Odds Ratio'] = np.exp(summary['Coef.'])
    
    # Rename rows for the LaTeX table
    summary.index = ['Intercept', f'{component.replace("_", " ").capitalize()} Count']
    intercept_val = summary.iloc[0]['Coef.']
    coeff_val = summary.iloc[1]['Coef.']
    # If the coefficient is positive, we calculate the crossover point
    
    p_threshold = 0.30
    logit_p = math.log(p_threshold / (1 - p_threshold))

    x30_threshold = (logit_p -intercept_val) / coeff_val if coeff_val != 0 else 0
    sustained_df = df[df['is_sustained'] == 1]
    sus_hit = len(sustained_df[sustained_df['metric_value'] >= x30_threshold])
    sus_pct = (sus_hit / len(sustained_df) * 100) if len(sustained_df) > 0 else 0
    moderate_df = df[df['is_sustained'] == 0]
    mod_hit = len(moderate_df[moderate_df['metric_value'] >= x30_threshold])
    mod_pct = (mod_hit / len(moderate_df) * 100) if len(moderate_df) > 0 else 0

    # Clean up columns for the paper
    results_df = summary[['Coef.', 'Odds Ratio', 'Std.Err.', 'P>|z|']]
    results_df.columns = ['Coefficient', 'Odds Ratio', 'Std. Err', 'p-Value']

    # 4. Generate LaTeX
    return generate_latex(component, summary, avg_mod, avg_sus, number_of_commits, x30_threshold, mod_hit, mod_pct, sus_hit, sus_pct)

def generate_and_save(component, developers, number_of_commits):
    path = "repository/" 
    file_name = FILE_NAME
    commit_prefix = "all commits"
    df = pd.DataFrame(prepare_data(developers, TIME_SERIES_NUMBER_OF_COMMIT))
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_heading(commit_prefix)
        
        headings = ["Component", "Number of First Commits", "Type", "Moderate $\mu$", "Sustained $\mu$", "Coefficient", "Odds Ratio", "Std. Err", "$p$-Value", "30\% Threshold", "Moderate Met Threshold", "Sustained Met Threshold"]
        latex += start_latex_table("Strategy Logistic Regression for all components against number of commits for " + str(len(df)) + " developers excluding trainsient", headings, "l r l r r r r r r r r r")
        save_to_latex_file(get_base_file_name(file_name), 
                           BASE_FILE_NAME,
                               latex, path)

    latex_table = generate_predictive_identification_latex(df, component, number_of_commits).replace("_", "\\_")
    read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", latex_table, path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", table_end() + generate_predictive_model_latex() + "\n \\newpage \n", path)
         