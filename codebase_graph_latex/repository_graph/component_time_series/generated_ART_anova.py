from statsmodels.formula.api import ols
import statsmodels.api as sm
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import numpy2ri

from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data
from codebase_graph_latex.latex_table import *
import os
import sys

# Force the R library directory explicitly into the Windows environment path
# (Adjust the R version numbers below if yours is slightly different, e.g., R-4.4.1)
os.environ["R_LIBS_USER"] = r"C:\Program Files\R\R-4.6.0\library"
os.environ["PATH"] = r"C:\Program Files\R\R-4.6.0\bin\x64;" + os.environ["PATH"]

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "An \\textbf{Aligned Rank Transform (ART)} Anova table for all components touched on average. "
    latex += generate_art_anova_explanation_latex()
    return latex

def section_sub_sub_heading(commit_prefix):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + commit_prefix + "} \n"
    return latex

def generate_art_anova_explanation_latex():
    latex = r"""
The statistical significance of architectural exploration is evaluated using a dual-framework modeling methodology. A standard parametric ordinary least squares (\textbf{OLS}) ANOVA is presented alongside a robust non-parametric ANOVA. This side-by-side presentation explicitly demonstrates where extreme right-skew and outlier-induced variance in repository mining data mask true behavioral effects in traditional linear models, which the rank-transformed framework uncovers.

\paragraph{Explanation of Combined Table Columns:}
\begin{itemize}
    \item \textbf{Component / Commits ($n$) / Devs ($N$):} Define the experimental scope, tracking the architectural tier (packages, classes, or methods), the longitudinal lifecycle snapshot threshold, and the active developer population size.
    \item \textbf{Factor:} The independent categorical variables or interactions being tested for statistical significance.
    
    \item \textbf{OLS df:} Parametric numerator degrees of freedom based on factor grouping configurations.
    \item \textbf{OLS F-Stat:} The traditional variance ratio metric calculated from raw values.
    \item \textbf{OLS $P$-Value:} Parametric significance probability. Note how heteroscedastic noise frequently inflates these values toward non-significance ($p > 0.05$).
    \item \textbf{OLS $\eta^2$ (Eta-Squared):} The total proportion of raw variance explained exclusively by this standalone factor.
    
    \item \textbf{ART df (Resid):} Formatted as $df_{\mathrm{effect}}~(df_{\mathrm{residual}})$. Because the ART methodology conducts independent alignment procedures for each factor before ranking, it assigns the exact denominator error degrees of freedom dynamically alongside its numerator.
    \item \textbf{ART F-Stat:} The robust variance ratio calculated over the aligned, ranked data layers.
    \item \textbf{ART $P$-Value:} Non-parametric significance probability, providing the authoritative test for heavy-tailed software metrics.
    \item \textbf{ART Part. $\eta^2$ (Partial Eta-Squared):} The effect size over ranked data layers, indicating the proportion of variance explained by this specific factor after controlling for alternate main effects.
\end{itemize}

\paragraph{Explanation of Fixed Table Rows:}
\begin{itemize}
    \item \textbf{Role (F/LJ):} Isolates the \textit{Main Role Effect} to evaluate whether the timing of project entry (Founder vs. Later Joiner) significantly alters exploration breadth on its own.
    \item \textbf{Category (T/M/S or M/S):} Isolates the \textit{Main Category Effect} to determine whether a contributor's eventual longevity footprint (Transient, Moderate, or Sustained) dictates early behavior.
    \item \textbf{Interaction:} Evaluates the \textit{Interaction Effect} ($\mathrm{Role} \times \mathrm{Category}$). A significant interaction indicates that the impact of entry role is not uniform, but behaves completely differently depending on the eventual tenure category of the contributor.
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
    \item $\alpha_i$ represents the effect of the \textbf{Role} (Founder vs. Later Joiner).
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

def get_data_frame(developers_dict, unit):
    rows = []
    for cat_name, dev_data in developers_dict.items():
        role = "Founder" if "founder" in cat_name.lower() else "Later Joiner"
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

def generate_anova_latex(df, component, commit_prefix, number_of_commits, category):
    component = component.replace("_", "-")
    number_of_developers = len(df)

    # --- PART A: STANDARD OLS ANOVA ---
    model = ols('Value ~ C(Role) * C(Tenure)', data=df).fit()
    ols_table = sm.stats.anova_lm(model, typ=3)
    ss_total = ols_table['sum_sq'].sum()
    ols_table['eta_sq'] = ols_table['sum_sq'] / ss_total

    # --- PART B: ART ANOVA ---
    artool = importr('ARTool')
    stats = importr('stats')
    
    with localconverter(robjects.default_converter + pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(df)
        robjects.globalenv['r_df'] = r_df
        
        robjects.r('''
            art_mod <- ARTool::art(Value ~ factor(Role) * factor(Tenure), data = r_df)
            art_anova_res <- stats::anova(art_mod)
        ''')
        art_table = robjects.conversion.rpy2py(robjects.globalenv['art_anova_res'])
    
    # Calculate Partial Eta Squared safely, handling edge case NaNs defensively
    f_val = art_table['F value'].fillna(0)
    df_eff = art_table['Df'].fillna(0)
    df_res = art_table['Df.res'].fillna(1)
    art_table['eta_p_sq'] = (f_val * df_eff) / ((f_val * df_eff) + df_res)

    # --- PART C: SIDE-BY-SIDE MATRIX LAYOUT GENERATION ---
    # Map the exact keys returned by statsmodels and ARTool to a clean target key
    factor_mapping = [
        {
            'label': 'Role (F/LJ)',
            'ols_key': 'C(Role)',
            'art_key': 'factor(Role)'
        },
        {
            'label': category,
            'ols_key': 'C(Tenure)',
            'art_key': 'factor(Tenure)'
        },
        {
            'label': 'Interaction',
            'ols_key': 'C(Role):C(Tenure)',
            'art_key': 'factor(Role):factor(Tenure)'
        }
    ]

    latex_output = ""
    
    for factor in factor_mapping:
        lbl = factor['label']
        
        # 1. Extract Parametric OLS Metrics Safely
        ols_row = ols_table.loc[factor['ols_key']] if factor['ols_key'] in ols_table.index else None
        if ols_row is not None:
            ols_df = f"{ols_row['df']:.0f}"
            ols_f = f"{ols_row['F']:.2f}"
            p_val = ols_row['PR(>F)']
            ols_p = f"{p_val:.4f}" if not pd.isna(p_val) else "1.0000"
            ols_eta = f"{ols_row['eta_sq']:.4f}"
        else:
            ols_df, ols_f, ols_p, ols_eta = "-", "-", "-", "-"

        # 2. Extract Non-Parametric ART Metrics Safely
        art_row = art_table.loc[factor['art_key']] if factor['art_key'] in art_table.index else None
        if art_row is not None:
            art_df_num = art_row['Df']
            art_df_den = art_row['Df.res']
            art_df = f"{art_df_num:.0f} ({art_df_den:.0f})"
            art_f = f"{art_row['F value']:.2f}"
            art_p = f"{art_row['Pr(>F)']:.4f}"
            art_eta_p = f"{art_row['eta_p_sq']:.4f}"
        else:
            art_df, art_f, art_p, art_eta_p = "-", "-", "-", "-"

        # 3. Concatenate side-by-side data columns cleanly into 12 total columns
        latex_output += (
            f"{component} & {number_of_commits} & {number_of_developers} & {lbl} & "
            f"{ols_df} & {ols_f} & {ols_p} & {ols_eta} & "
            f"{art_df} & {art_f} & {art_p} & {art_eta_p} \\\\ \n"
        )
        
    return latex_output

def generate_and_save(component, developers, number_of_commits):
    path = DIRECTORY
    base_file_name = get_base_file_name(FILE_NAME)
    file_name = base_file_name + "_transient"
    df = get_data_frame(developers, TIME_SERIES_NUMBER_OF_COMMIT)
    table_name = "ART Anova results for all components, number of commits and categories of developers"
    commit_prefix = "all commits"
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_heading(commit_prefix)
        read_write_file.append_to_file(base_file_name + ".tex", latex, DIRECTORY)
        headings = [
            "Component", 
            "First $n$ commits", 
            "Number of Developers", 
            "Factor", 
            "OLS df", 
            "OLS F-Stat", 
            "OLS $P$ Value", 
            "OLS $\eta^2$", 
            "ART df (Resid)", 
            "ART F-Stat", 
            "ART $P$ Value", 
            "ART Part. $\eta^2$"]
        latex = start_latex_table(table_name, headings, "l r r l ccc r ccc r")
        save_to_latex_file(file_name, base_file_name + ".tex", latex, path)   
    if number_of_commits == 1:     
        category = "Category (T/M/S)"
    else:
        category = "Category (M/S)"
    latex_table = generate_anova_latex(df, component, commit_prefix, number_of_commits, category).replace("_", "\\_")
    read_write_file.append_to_file(file_name + ".tex", latex_table, path)
    if component == "methods" and number_of_commits == 10:
        read_write_file.append_to_file(file_name + ".tex", table_end(), path)
        read_write_file.append_to_file(base_file_name + ".tex", generate_statistical_formula_latex() + "\n\\newpage \n", path)
         