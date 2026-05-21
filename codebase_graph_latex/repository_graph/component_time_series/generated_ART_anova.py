from statsmodels.formula.api import ols
import statsmodels.api as sm
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter

from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data
from codebase_graph_latex.latex_table import *
import os
import sys

# Force the R library directory explicitly into the Windows environment path
# (Adjust the R version numbers below if yours is slightly different, e.g., R-4.4.1)
os.environ["R_LIBS_USER"] = r"C:\Program Files\R\R-4.4.0\library"
os.environ["PATH"] = r"C:\Program Files\R\R-4.4.0\bin\x64;" + os.environ["PATH"]

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "An ART Anova table for all components touched on avepip install rpy2rage. \n"
    latex += generate_anova_explanation_latex()
    return latex

def section_sub_sub_heading(commit_prefix):
    latex = r"\begin{landscape}" + "\n"
    latex += get_section_start(FILE_NAME, "subsub") 
    latex += "For all components touched for " + commit_prefix + "} \n"
    return latex

def generate_anova_explanation_latex():
    latex = r"""
The Non-Parametric Factorial analysis evaluates the influence of two independent categorical variables—\textit{Role} (Founder vs. Later Joiner) and \textit{Tenure} (Moderate vs. Sustained)—on the unique architectural components touched. Because the data exhibits significant non-normality and heteroscedasticity, an \textbf{Aligned Rank Transform (ART) ANOVA} is implemented.

\paragraph{Explanation of Table Columns:}
\begin{itemize}
    \item \textbf{df / df (Resid):} The numerator degrees of freedom for the factor, followed by the denominator error degrees of freedom calculated uniquely for that factor's alignment field.
    \item \textbf{F-statistic:} The robust variance ratio calculated over the aligned, ranked data layers.
    \item \textbf{p-Value ($PR(>F)$):} The significance value. Values under $\alpha = 0.05$ document robust significance remaining after controlling for alternate factors.
    \item \textbf{Part. $\eta^2$ (Partial Eta Squared):} The effect size, indicating the proportion of variance explained by this specific factor after stripping away alternate main effects.
\end{itemize}

\paragraph{Explanation of Table Rows:}
\begin{itemize}
    \item \textbf{Intercept:} Represents the baseline value of the dependent variable when all categorical factors are at their reference levels.
    \item \textbf{Role(F/L):} Tests the \textit{Main Role Effect} of being a Founder versus a Later Joiner. The p-Value above 0.05 indicates that the timing of project entry does not significantly change the breadth of early-stage component exploration.
    \item \textbf{Category(M/S):} Tests the \textit{Main Category Effect} of the eventual contributor category (Transient vs Moderate vs. Sustained). 
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

    # --- PART A: STANDARD OLS ANOVA ---
    model = ols('Value ~ C(Role) * C(Tenure)', data=df).fit()
    ols_table = sm.stats.anova_lm(model, typ=3)
    ss_total = ols_table['sum_sq'].sum()
    ols_table['eta_sq'] = ols_table['sum_sq'] / ss_total

    # --- PART B: ART ANOVA (Using Modern Converter Context) ---
    artool = importr('ARTool')
    stats = importr('stats')
    
    # Use the modern localconverter context to cleanly turn pandas into R frames
    with localconverter(robjects.default_converter + pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(df)
        
        # Assign the data frame directly to the R environment global space
        robjects.globalenv['r_df'] = r_df
        
        # Run the Aligned Rank Transform model
        art_model = artool.art(robjects.Formula('Value ~ factor(Role) * factor(Tenure)'), data=r_df)
        r_anova_table = stats.anova(art_model)
        
        # Convert the R result table cleanly back into a Pandas DataFrame
        art_table = robjects.conversion.rpy2py(r_anova_table)
    
    # Calculate Partial Eta Squared for ART ANOVA: (F * df) / ((F * df) + df_res)
    art_table['eta_p_sq'] = (art_table['F value'] * art_table['Df']) / \
                            ((art_table['F value'] * art_table['Df']) + art_table['Df.res'])

    # --- PART C: GENERATE EXPANDED LATEX ---
    name_map_ols = {
        'C(Role)': 'Role (F/LJ)',
        'C(Tenure)': category,
        'C(Role):C(Tenure)': 'Interaction',
        'Residual': 'Residual'
    }
    
    # Note: R handles factors in lowercase, mapping appropriately
    name_map_art = {
        'factor(Role)': 'Role (F/LJ)',
        'factor(Tenure)': category,
        'factor(Role):factor(Tenure)': 'Interaction'
    }

    latex_output = ""
    
    # 1. Append OLS ANOVA Rows
    for index, row in ols_table.iterrows():
        if index == 'Intercept': continue
        label = name_map_ols.get(index, index)
        
        if index == 'Residual':
            latex_output += f"{component} & {number_of_commits} & OLS & {label} & {row['sum_sq']:.2f} & {row['df']:.0f} & - & - & - & - \\\\ \n"
        else:
            latex_output += f"{component} & {number_of_commits} & OLS & {label} & {row['sum_sq']:.2f} & {row['df']:.0f} & {row['F']:.2f} & {row['PR(>F)']:.4f} & {row['eta_sq']:.4f} & - \\\\ \n"
            
    latex_output += r"\hline " + "\n"

    # 2. Append ART ANOVA Rows
    for index, row in art_table.iterrows():
        clean_index = str(index).strip()
        label = name_map_art.get(clean_index, clean_index)
        
        latex_output += f"{component} & {number_of_commits} & ART & {label} & - & {row['Df']:.0f} & {row['F value']:.2f} & {row['Pr(>F)']:.4f} & - & {row['eta_p_sq']:.4f} \\\\ \n"

    return latex_output

def generate_and_save(component, developers, number_of_commits):
    path = DIRECTORY
    base_file_name = get_base_file_name(FILE_NAME)
    file_name = base_file_name + "_transient"
    df = get_data_frame(developers, TIME_SERIES_NUMBER_OF_COMMIT)
    table_name = "Anova results for all components, number of commits and " + str(len(df)) + " developers"
    commit_prefix = "all commits"
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_heading(commit_prefix)
        save_to_latex_file(base_file_name, BASE_FILE_NAME, latex, path)
        headings = ["Component", "First *n* commits", "Factor", "df", "df (Resid)", "F-Stat", "$P$ Value", "Part. $\eta^2$"]
        commit_prefix += " excluding transient developers" 
        table_name += " excluding transient developers"
        latex = section_sub_sub_heading(commit_prefix)
        latex += start_latex_table(table_name, headings, "l r l r r r r r")
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
         