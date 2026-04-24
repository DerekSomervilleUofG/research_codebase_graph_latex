import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from codebase_graph_latex.repository_graph.component_time_series.anova_generate import get_data_frame
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "An Tukey Honestly Significant Difference table for all components touched on average. \n"
    latex += generate_tukey_explanation_latex()
    return latex

def section_sub_sub_heading(component, time_series):
    latex = r"\begin{landscape}" + "\n"
    latex += get_section_start(FILE_NAME, "subsub") 
    latex += "For " + component + " touched for " + time_series + "} \n"
    return latex

def generate_tukey_explanation_latex():
    return r"""
\paragraph{Post-hoc Analysis (Tukey HSD):}
Following the ANOVA, a Tukey Honestly Significant Difference (HSD) test was performed. 
While ANOVA identifies if at least one group differs, Tukey HSD performs pairwise 
comparisons to identify specific differences between developer roles and tenure 
categories while controlling for Type I error rates across multiple comparisons.
"""
def generate_tukey_formula_latex():
    """
    Returns a LaTeX string defining the Tukey HSD post-hoc test
    used to identify specific differences between developer groups.
    """
    latex = r"""
\subsubsection*{Post-hoc Analysis: Tukey HSD}
Following the Two-Way ANOVA, a Tukey Honestly Significant Difference (HSD) test 
is used to conduct pairwise comparisons. This test determines which specific 
group means differ significantly while maintaining a constant family-wise 
error rate.

The studentized range statistic ($q$) for comparing two group means is defined as:

\begin{equation}
    q = \frac{\bar{Y}_{max} - \bar{Y}_{min}}{\sqrt{\frac{MS_{residual}}{n}}}
\end{equation}

Where:
\begin{itemize}
    \item $\bar{Y}_{max}$ and $\bar{Y}_{min}$ are the larger and smaller means of the two groups being compared.
    \item $MS_{residual}$ is the Mean Square Error derived from the ANOVA residual.
    \item $n$ is the number of observations in each group (adjusted for unequal sample sizes via the harmonic mean).
\end{itemize}

A pair of groups is considered significantly different if the absolute difference 
between their means exceeds the Honestly Significant Difference (HSD):

\begin{equation}
    HSD = q_{\alpha, k, df} \sqrt{\frac{MS_{residual}}{n}}
\end{equation}

Where $q_{\alpha, k, df}$ is the critical value from the studentized range 
distribution based on the significance level ($\alpha = 0.05$), the number 
of groups ($k$), and the degrees of freedom ($df$) from the ANOVA residual.
"""
    return latex

def generate_tukey_latex(df, component, number_of_commits):
    # 1. Create the interaction group column [cite: 48, 85]
    df['Group'] = df['Role'] + " " + df['Tenure']
    
    # 2. Run Tukey HSD [cite: 132, 133]
    tukey = pairwise_tukeyhsd(endog=df['Value'], groups=df['Group'], alpha=0.05)
    
    # 3. Convert summary to a DataFrame for iteration
    # The first row [0] is the header, [1:] is the data
    tukey_results = pd.DataFrame(data=tukey.summary().data[1:], 
                                columns=tukey.summary().data[0])
    
    latex_output = ""

    for _, row in tukey_results.iterrows():
        # Only include significant results to keep dissertation tables manageable [cite: 29, 31]
        if not row['reject']:
            continue
            
        p_val = row['p-adj']
        group1 = str(row['group1']).replace("_", "\\_")
        group2 = str(row['group2']).replace("_", "\\_")
        
        # Formatting for your LaTeX table structure
        latex =  f"{number_of_commits} & "
        latex += f"{group1} & {group2} & "
        latex += f"{row['meandiff']:.2f} & {p_val:.4f} \\\\ \n"
        
        latex_output += latex
        
    return latex_output

def generate_and_save(component, developers, number_of_commits):
    path = "repository/" 
    base_file_name = get_base_file_name(FILE_NAME)
    file_name = base_file_name + "_" + component
    table_name = "Tukey HSD results for "+ component + " and number of commits"
    commit_prefix = "all commits"
    headings = ["Commits", "Group A", "Group B", "Mean Diff", "Adj $P$ Value"]
    if component == "classes" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_heading(commit_prefix)
        save_to_latex_file(base_file_name, BASE_FILE_NAME, latex, path)
    if number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_sub_heading(component, commit_prefix)
        latex += start_latex_table(table_name, headings, "r r r r r")
        save_to_latex_file(file_name, base_file_name + ".tex", latex, path)
    latex_table = generate_tukey_latex(get_data_frame(developers, True, TIME_SERIES_NUMBER_OF_COMMIT), component, number_of_commits).replace("_", "\\_")
    read_write_file.append_to_file(file_name + ".tex", latex_table, path)
    if number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(file_name + ".tex", table_end() + "\n \\newpage \n", path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(base_file_name + ".tex", generate_tukey_formula_latex() + "\n \\newpage \n", path)
         