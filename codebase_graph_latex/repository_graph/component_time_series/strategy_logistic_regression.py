import pandas as pd
import statsmodels.api as sm
import numpy as np
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "A Strategy Logistic Regression table for all components touched on average. \n"
    return latex

def section_sub_sub_heading(component, time_series):
    latex = get_section_start(FILE_NAME, "subsub") 
    latex += "For " + component + " touched for a " + time_series + "} \n"
    latex += "A Strategy Logistic Regression table for " + component + " touched on average. \n"
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

def generate_predictive_identification_latex(developers_dict, unit, component):
    rows = []
    
    # 1. Prepare the data: Binary classification (Sustained vs Not)
    for cat_name, dev_data in developers_dict.items():
        # Target: 1 if developer became Sustained, 0 otherwise
        is_sustained = 1 if "sustained" in cat_name.lower() else 0
        
        touched_data = populate_touched_data(dev_data, unit)
        
        for series in touched_data:
            # We use the final value in this commit window as the predictor
            rows.append({
                'is_sustained': is_sustained,
                'metric_value': series[-1]
            })
            
    df = pd.DataFrame(rows)
    
    # Check if we have both classes (0 and 1) to run the model
    if df['is_sustained'].nunique() < 2:
        return f"% Skip {component}: Not enough diversity in classes for Logistic Regression."

    # 2. Run Logistic Regression
    # Y = is_sustained, X = metric_value (e.g., methods touched)
    X = sm.add_constant(df['metric_value'])
    logit_model = sm.Logit(df['is_sustained'], X).fit(disp=0)
    summary = logit_model.summary2().tables[1] # Extract the coefficients table
    
    # 3. Calculate Odds Ratio (OR = exp(coeff))
    summary['Odds Ratio'] = np.exp(summary['Coef.'])
    
    # Rename rows for the LaTeX table
    summary.index = ['Intercept', f'{component.replace("_", " ").capitalize()} Count']
    
    # Clean up columns for the paper
    results_df = summary[['Coef.', 'Odds Ratio', 'Std.Err.', 'P>|z|']]
    results_df.columns = ['Coefficient', 'Odds Ratio', 'Std. Err', 'p-Value']

    # 4. Generate LaTeX
    component_clean = component.replace("_", "-")
    return results_df.to_latex(
        position="h!",
        index=True,
        caption=f"Logistic Regression: Predicting Sustained Contribution via {component_clean} (First Commits)",
        label=f"tab:predict-{component_clean}",
        float_format="%.4f"
    )

def generate_and_save(component, developers, number_of_commits):
    path = "repository/" 
    file_name = FILE_NAME
    commit_prefix = "all commits"
    if number_of_commits > 0:
        file_name += "_" + str(number_of_commits)
        commit_prefix = "first " + word_engine.number_to_words(number_of_commits) + " commits"
    if component == "packages":
        latex = section_sub_heading(commit_prefix)
        latex += section_sub_sub_heading(component, commit_prefix)
        read_write_file.write_file(get_base_file_name(file_name) + ".tex", 
                               latex, path)
        latex = "\\input{" + path + get_base_file_name(file_name) + "}\n"
        read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
    else:
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", 
                               section_sub_sub_heading(component, commit_prefix), path)
    latex_table = generate_predictive_identification_latex(developers, TIME_SERIES_NUMBER_OF_COMMIT, component).replace("_", "\\_")
    read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", latex_table, path)
    if component == "methods":
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", generate_predictive_model_latex() + "\n \\newpage \n", path)
         