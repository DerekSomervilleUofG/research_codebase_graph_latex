from statsmodels.formula.api import ols
import statsmodels.api as sm
import pandas as pd

from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "An Anova table for all components touched on average. \n"
    latex += generate_anova_explanation_latex()
    return latex

def section_sub_sub_heading(commit_prefix):
    latex = r"\begin{landscape}" + "\n"
    latex += get_section_start(FILE_NAME, "subsub") 
    latex += "For all components touched for a " + commit_prefix + "} \n"
    return latex

def generate_anova_explanation_latex():
    latex = r"""
The Two-Way ANOVA evaluates the influence of two independent categorical variables—\textit{Role} (Founder vs. Late Joiner) and \textit{Tenure} (Moderate vs. Sustained)—on the number of unique architectural components touched. The analysis excludes and includes Transient developers to isolate the behaviors of contributors with established project engagement.

\paragraph{Explanation of Table Columns:}
\begin{itemize}
    \item \textbf{Sum Sq (Sum of Squares):} Represents the total variation explained by that specific factor. A higher Sum Sq relative to the Residual indicates that the factor has a strong influence on the outcome.
    \item \textbf{df (Degrees of Freedom):} The number of independent values that can vary in the calculation. For categorical variables, this is typically $N-1$ levels.
    \item \textbf{F (F-statistic):} The ratio of the variance explained by the factor to the variance unexplained (Residual). A larger F-value suggests the factor is more likely to be significant.
    \item \textbf{p-Value ($PR(>F)$):} The probability that the observed differences occurred by chance. Using a significance threshold of $\alpha = 0.05$, values above this indicate no statistically significant effect.
    \item \textbf{ETA Sq} The effect size, quantifies the proportion of the total variance in your dependent variable. 
\end{itemize}

\paragraph{Explanation of Table Rows:}
\begin{itemize}
    \item \textbf{Intercept:} Represents the baseline value of the dependent variable when all categorical factors are at their reference levels.
    \item \textbf{Role(F/L):} Tests the \textit{Main Role Effect} of being a Founder versus a Late Joiner. The p-Value above 0.05 indicates that the timing of project entry does not significantly change the breadth of early-stage component exploration.
    \item \textbf{Category(M/S):} Tests the \textit{Main Category Effect} of the eventual contributor catregory (Transient vs Moderate vs. Sustained). 
    \item \textbf{Interaction:} Tests the \textit{Interaction Effect}. It evaluates if the effect of being a Founder is different for the different categories. 
    \item \textbf{Residual:} Represents the ``noise'' or variance within the groups that cannot be explained by Role or Tenure. 
\end{itemize}
"""
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

def get_data_frame(developers_dict, include_transient, unit):
    rows = []
    for cat_name, dev_data in developers_dict.items():
        if not include_transient and TRANSIENT in cat_name:
            continue
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
    
    return pd.DataFrame(rows)

def generate_anova_latex(developers_dict, unit, component, commit_prefix, number_of_commits, include_transient, category):
    component = component.replace("_", "-")

    df = get_data_frame(developers_dict, include_transient, unit)    
    # 2. Run the Two-Way ANOVA
    # C() tells statsmodels these are Categorical variables
    model = ols('Value ~ C(Role) * C(Tenure)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)
    
    ss_total = anova_table['sum_sq'].sum()
    anova_table['eta_sq'] = anova_table['sum_sq'] / ss_total

    # 3. Manually Generate LaTeX Rows
    # Mapping statsmodels names to readable labels
    name_map = {
        'C(Role)': 'Role (F/L)',
        'C(Tenure)': category,
        'C(Role):C(Tenure)': 'Interaction',
        'Residual': 'Residual'
    }

    latex_output = ""
    for index, row in anova_table.iterrows():
        if index == 'Intercept': continue # Usually omitted in final papers to save space
        
        label = name_map.get(index, index)
        p_val = row['PR(>F)']
        
        # Follows your requested format: Component & Window & Label & SumSq & df & F & P & EtaSq
        latex =  f"{component} & {number_of_commits} & {label} & "
        latex += f"{row['sum_sq']:.2f} & {row['df']:.0f} & "
        latex += f"{row['F']:.2f} & {p_val:.4f} & "
        
        # Handle the Residual row (which has no F or P)
        if index == 'Residual':
            latex = f"{component} & {number_of_commits} & {label} & {row['sum_sq']:.2f} & {row['df']:.0f} & - & -  \\\\ \n"
        else:
            latex += f"{row['eta_sq']:.4f} \\\\ \n"
            
        latex_output += latex

    return latex_output

def generate_and_save(component, developers, number_of_commits, include_transent=False):
    path = "repository/" 
    base_file_name = get_base_file_name(FILE_NAME)
    file_name = base_file_name + "_transient"
    table_name = "Anova results for compents and number of commits"
    if not include_transent:
        file_name += "_not"
    commit_prefix = "all commits"
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER and include_transent:
        latex = section_sub_heading(commit_prefix)
        save_to_latex_file(base_file_name, BASE_FILE_NAME, latex, path)
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        headings = ["Component", "Number of First Commits", "Factor", "Sum Squared", "df", "F-Stat", "$P$ Value", "ETA Sq"]
        if include_transent:
            commit_prefix += " including transient"
            table_name += " including transient"
        else:
            commit_prefix += " excluding tranient" 
            table_name += " excluding transient"
        latex = section_sub_sub_heading(commit_prefix)
        latex += start_latex_table(table_name, headings, "l r l r r r r r")
        save_to_latex_file(file_name, base_file_name + ".tex", latex, path)        
    if include_transent:
        category = "Category (T/M/S)"
    else:
        category = "Category (M/S)"
    latex_table = generate_anova_latex(developers, TIME_SERIES_NUMBER_OF_COMMIT, component, commit_prefix, number_of_commits, include_transent, category).replace("_", "\\_")
    read_write_file.append_to_file(file_name + ".tex", latex_table, path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(file_name + ".tex", table_end() + "\n \\newpage \n", path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER and not include_transent:
        read_write_file.append_to_file(base_file_name + ".tex", generate_statistical_formula_latex() + "\n \\newpage \n", path)
         