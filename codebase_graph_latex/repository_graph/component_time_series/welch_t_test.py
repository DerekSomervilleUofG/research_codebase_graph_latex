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
    latex += "and is robust to unequal variances. "  
    latex += "Complementarily, the Mann-Whitney $U$ (MWU) test was used to assess stochastic dominance "
    latex += "by ranking data points. This non-parametric approach does not require a normal distribution "
    latex += "and is highly resistant to outliers. Columns below:  \n"
    latex += r"""\begin{itemize}
                    \item{\textbf{Component} - Packages, classes or method touched.}
                    \item{\textbf{Number of first commits} - A sample of the first x number of commits for developers. }
                    \item{\textbf{Sample A $\mu$} - The mean average of the first sample A. }
                    \item{\textbf{Sample B $\mu$} - The mean average of the second sample B. }
                    \item{\textbf{Welch Statisic} - This is the magnitude of the change, greater than 2.0 generally indicates a significant change. }
                    \item{\textbf{Welch $P$} - A significance test of the difference between sample A and sample B. A $p$ \textless{} 0.05 indicates a significant difference between samples. }
                    \item{\textbf{MWU Statsitcal (Number of Pairs)} - The Mann-Whitney $U$ Statistic represents the number of pairwise comparisons where one group outranks the
other, with the total possible pairs provided in brackets.}
                    \item{\textbf{MWU $P$} - The Mann-Whitney $p$-value. A significance test of the difference between sample A and sample B. A $p$ \textless{} 0.05 indicates a significant difference between samples.} 
                \end{itemize}
    """
    latex += "\n"
    return latex

def section_sub_sub_heading(time_series):
    # Use raw strings (r"") to avoid issues with backslashes
    latex = r"\begin{landscape}" + "\n"
    latex += get_section_start(FILE_NAME, "subsub") 
    latex += "For all components touched for " + time_series + "} \n\n"    
    latex += "\n"
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

def determine_category(cat_name, sample_name, categories):
    category = cat_name.replace(sample_name, "").strip()
    if category not in categories:
        categories.append(category)

def filter_data(developers_dict, samples, unit):
    sample_a_values = []
    sample_b_values = []
    categories = []
    for cat_name, dev_data in developers_dict.items():
        touched_data = populate_touched_data(dev_data, unit)
        final_values = [series[-1] for series in touched_data]
        
        if samples[0] in cat_name.lower():
            sample_a_values.extend(final_values)
            determine_category(cat_name, samples[0], categories)
        elif samples[1] in cat_name.lower():
            sample_b_values.extend(final_values)
    if len(categories) == 2:
        category = categories[0] + " \& " + categories[1]
    elif len(categories) == 0:
        category = samples[0] + " \& " + samples[1]
    else:
        category = " ".join(categories)
    return sample_a_values, sample_b_values, category

def generate_simple_comparison_latex(sample_a_values, sample_b_values, category, component, samples, number_of_commits):
    
    total_pairs = len(sample_a_values) * len(sample_b_values)
    # 1. Welch's T-Test (Parametric)
    t_stat, t_p = stats.ttest_ind(sample_a_values, sample_b_values, equal_var=False)
    
    # 2. Mann-Whitney U (Non-Parametric)
    u_stat, u_p = stats.mannwhitneyu(sample_a_values, sample_b_values)

    mean_a = np.mean(sample_a_values) if sample_a_values else 0
    mean_b = np.mean(sample_b_values) if sample_b_values else 0
    # Build a simple DataFrame for the LaTeX table
    
    component_clean = component.replace("_", "-").capitalize() 
    latex =  f"{category} & {component_clean} & {number_of_commits} & "
    latex += f" {mean_a:.2f} & {mean_b:.2f} & "
    latex += f"{t_stat:.2f} & {t_p:.4f} & "
    latex += f"{u_stat:,.1f} ({total_pairs:,d}) & {u_p:.4f}  \\\\ \n"
    return latex

def generate_and_save(component, developers, number_of_commits, sample_a_b, file_name):
    path = "repository/" 
    commit_prefix = "all commits"
    sample_a_values, sample_b_values, category = filter_data(developers, sample_a_b, TIME_SERIES_NUMBER_OF_COMMIT)
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_sub_heading(commit_prefix + " by " + sample_a_b[0].capitalize() + "(" + str(len(sample_a_values))  + ") against " + sample_a_b[1].capitalize()) + "(" + str(len(sample_b_values)) + ")"  
        headings = ["Categories", "Component", "Number of First Commits", sample_a_b[0].capitalize() + " $\mu$", sample_a_b[1].capitalize()  + " $\mu$", "Welch Statistic", "Welch $P$", "MWU Statistic (Number of Pairs)", "MWU $P$" ]
        latex += start_latex_table("Welch t-test and Mann-Whitney U results for components and number of commits " + " by " + sample_a_b[0].lower() + " (" + str(len(sample_a_values))  + ") against " + sample_a_b[1].lower() + " (" + str(len(sample_b_values)) + ")" , headings, "l l r r r r r r r")
        read_write_file.append_to_file(file_name + ".tex", latex, path)
    latex_table = generate_simple_comparison_latex(sample_a_values, sample_b_values, category, component, sample_a_b, number_of_commits).replace("_", "\\_")
    read_write_file.append_to_file(file_name + ".tex", latex_table, path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(file_name + ".tex", table_end(), path)
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER and SUSTAINED + " late " + JOINER in sample_a_b[1]:
        read_write_file.append_to_file(file_name + ".tex", generate_statistical_formula_latex(sample_a_b) + "\n \\newpage \n", path)
         