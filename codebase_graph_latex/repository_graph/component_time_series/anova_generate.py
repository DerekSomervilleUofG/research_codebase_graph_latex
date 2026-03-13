from statsmodels.formula.api import ols
import statsmodels.api as sm
import pandas as pd

from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "An Anova table for all components touched on average. \n"
    return latex

def section_sub_sub_heading(component, time_series):
    latex = get_section_start(FILE_NAME, "subsub") 
    latex += "For " + component + " touched for a " + time_series + "} \n"
    latex += "An Anova table for " + component + " touched on average. \n"
    return latex

def generate_statistical_formula_latex():
    """
    Returns a LaTeX string defining the Two-Way ANOVA model used
    for the developer category analysis.
    """
    latex = r"""
\subsubsection*{Statistical Model}
The differences between developer categories are assessed using a Two-Way ANOVA 
with interaction. The value for any individual developer metric ($Y_{ijk}$) 
is modeled as:

\begin{equation}
    Y_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \epsilon_{ijk}
\end{equation}

Where:
\begin{itemize}
    \item $\mu$ is the grand mean of the touched components.
    \item $\alpha_i$ represents the effect of the \textbf{Role} (Founder vs. Late Joiner).
    \item $\beta_j$ represents the effect of the \textbf{Tenure} (Transient, Moderate, Sustained).
    \item $(\alpha\beta)_{ij}$ is the interaction effect between Role and Tenure.
    \item $\epsilon_{ijk}$ is the residual error.
\end{itemize}

The $F$-statistic for each factor is calculated by:
\begin{equation}
    F = \frac{SS_{factor} / df_{factor}}{SS_{residual} / df_{residual}}
\end{equation}
"""
    return latex

# Example Usage:
# formula_tex = generate_statistical_formula_latex()
# read_write_file.write_file("anova_formula.tex", formula_tex, "repository/")


def generate_anova_latex(developers_dict, unit, component):
    rows = []
    component = component.replace("_", "-")
    # 1. Flatten the nested dictionary into a DataFrame
    for cat_name, dev_data in developers_dict.items():
        # Identify Role and Tenure from your key names
        role = "Founder" if "founder" in cat_name.lower() else "Late Joiner"
        tenure = cat_name.split(" ")[0].capitalize() # Transient, Moderate, Sustained
        
        # Get the numerical data for these developers
        touched_data = populate_touched_data(dev_data, unit)
        
        for dev_series in touched_data:
            # We compare the final cumulative amount touched
            rows.append({
                'Role': role,
                'Tenure': tenure,
                'Value': dev_series[-1] 
            })
    
    df = pd.DataFrame(rows)
    
    # 2. Run the Two-Way ANOVA
    # C() tells statsmodels these are Categorical variables
    model = ols('Value ~ C(Role) * C(Tenure)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)
    
    # 3. Format the table for LaTeX
    latex_table = anova_table.to_latex(
        position="h!",
        index=True, 
        caption=f"Two-Way ANOVA for {component} touched by Developer Category",
        label = f"tab:anova-{component}",
        float_format="%.4f",
        column_format="lrrrr"
    )
    
    return latex_table.replace("sum_sq", "Sum Sq").replace("PR(>F)", "p-Value")

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
    latex_table = generate_anova_latex(developers, TIME_SERIES_NUMBER_OF_COMMIT, component).replace("_", "\\_")
    read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", latex_table, path)
    if component == "methods":
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", generate_statistical_formula_latex() + "\n \\newpage \n", path)
         