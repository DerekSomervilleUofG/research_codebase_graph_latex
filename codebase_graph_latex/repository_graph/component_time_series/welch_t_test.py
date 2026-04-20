from scipy import stats
import pandas as pd
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n\n"
    latex += "A Welch $t$-test was employed to determine if the mean contributions of Group A "
    latex += "differ significantly from Group B. This test is appropriate for continuous data "
    latex += "and is robust to unequal variances. A Welch Statistic magnitude greater than 2.0 "
    latex += "generally indicates a significant difference ($p < 0.05$). \n\n"
    
    latex += "Complementarily, the Mann-Whitney $U$ (MWU) test was used to assess stochastic dominance "
    latex += "by ranking data points. This non-parametric approach does not require a normal distribution "
    latex += "and is highly resistant to outliers. The MWU Statistic represents the number of pairwise "
    latex += "comparisons where one group outranks the other, with the total possible pairs provided in brackets. "
    latex += "A $p$-value less than 0.05 is considered statistically significant. \n"
    
    latex += "\n"
    return latex

def section_sub_sub_heading(time_series):
    # Use raw strings (r"") to avoid issues with backslashes
    latex = r"\begin{landscape}" + "\n"
    latex += get_section_start(FILE_NAME, "subsub") 
    latex += "For all components touched for " + time_series + "} \n\n"    
    latex += "\n"
    return latex

def generate_simple_comparison_latex(developers_dict, unit, component, samples, number_of_commits):
    sample_a_values = []
    sample_b_values = []

    for cat_name, dev_data in developers_dict.items():
        touched_data = populate_touched_data(dev_data, unit)
        final_values = [series[-1] for series in touched_data]
        
        if samples[0] in cat_name.lower():
            sample_a_values.extend(final_values)
        elif samples[1]:
            sample_b_values.extend(final_values)
    total_pairs = len(sample_a_values) * len(sample_b_values)
    # 1. Welch's T-Test (Parametric)
    t_stat, t_p = stats.ttest_ind(sample_a_values, sample_b_values, equal_var=False)
    
    # 2. Mann-Whitney U (Non-Parametric)
    u_stat, u_p = stats.mannwhitneyu(sample_a_values, sample_b_values)

    mean_a = np.mean(sample_a_values) if sample_a_values else 0
    mean_b = np.mean(sample_b_values) if sample_b_values else 0

    # Build a simple DataFrame for the LaTeX table
    component_clean = component.replace("_", "-").capitalize() 
    latex =  f"{number_of_commits} & {component_clean} & "
    latex += f" {mean_a:.2f} & {mean_b:.2f} & "
    latex += f"{t_stat:.2f} & {t_p:.4f} & "
    latex += f"{u_stat:,.1f} ({total_pairs:,d}) & {u_p:.4f}  \\\\ \n"
    return latex

def generate_statistical_formula_latex(sample_a_b):
    """
    Returns a LaTeX string defining both the Two-Way ANOVA and 
    Welch's t-test models for developer analysis.
    """
    group_a = sample_a_b[0].capitalize()
    group_b = sample_a_b[1].capitalize()
    latex = r"""
\subsubsection*{Statistical Models}

\paragraph{Welch's t-test}
To specifically compare the two primary roles (\textbf{Sample A} vs. \textbf{Sample B}) without assuming equal variances or sample sizes, Welch's $t$-test is employed. The $t$-statistic is defined as:

\begin{equation}
    t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{N_1} + \frac{s_2^2}{N_2}}}
\end{equation}

Where:
\begin{itemize}
    \item $\bar{X}_1, \bar{X}_2$ are the sample means of Sample A and Sample B.
    \item $s_1^2, s_2^2$ are the sample variances.
    \item $N_1, N_2$ are the sample sizes.
\end{itemize}

The degrees of freedom ($\nu$) for this test are calculated using the Welch-Satterthwaite equation:
\begin{equation}
    \nu \approx \frac{\left(\frac{s_1^2}{N_1} + \frac{s_2^2}{N_2}\right)^2}{\frac{(s_1^2/N_1)^2}{N_1-1} + \frac{(s_2^2/N_2)^2}{N_2-1}}
\end{equation}
"""
    return latex

def generate_and_save(component, developers, number_of_commits, sample_a_b, file_name):
    path = "repository/" 
    commit_prefix = "all commits"
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_sub_heading(commit_prefix + " by " + sample_a_b[0].capitalize() + " against " + sample_a_b[1].capitalize())
        headings = ["Number of First Commits", "Component", sample_a_b[0].capitalize() + " $\mu$", sample_a_b[1].capitalize()  + " $\mu$", "Welch Statistic", "Welch $P$", "MWU Statistic (Number of Pairs)", "MWU $P$" ]
        latex += start_latex_table("Welch t-test and Mann-Whitney U Results for Components and number of commits " + " by " + sample_a_b[0].capitalize() + " against " + sample_a_b[1].capitalize(), headings)
        read_write_file.append_to_file(file_name + ".tex", latex, path)
    latex_table = generate_simple_comparison_latex(developers, TIME_SERIES_NUMBER_OF_COMMIT, component, sample_a_b, number_of_commits).replace("_", "\\_")
    read_write_file.append_to_file(file_name + ".tex", latex_table, path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(file_name + ".tex", table_end(), path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER and "moderate" in sample_a_b[0]:
        read_write_file.append_to_file(file_name + ".tex", generate_statistical_formula_latex(sample_a_b) + "\n \\newpage \n", path)
         