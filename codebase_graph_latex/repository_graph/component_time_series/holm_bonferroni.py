import pandas as pd
import numpy as np
from itertools import combinations
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
from codebase_graph_latex.repository_graph.component_time_series.ART_anova import get_data_frame
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_heading(time_series):
    latex = get_section_start(FILE_NAME, "").replace(" ", "-") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "\\label{sec:" + FILE_NAME.replace(" ", "_") + "} \n"
    latex += "A Pairwise Post-hoc Analysis with Holm-Bonferroni Correction table for all components touched on average. \n"
    latex += generate_holm_explanation_latex()
    return latex

def section_sub_sub_heading(component, time_series):
    # Added missing initialization assignment bugfix from previous script instance
    latex = get_section_start(FILE_NAME, "subsub") 
    latex += "For " + component + " touched for " + time_series + "} \n"
    return latex

def generate_holm_explanation_latex():
    return r"""
\paragraph{Post-hoc Pairwise Analysis (Holm-Bonferroni):}
Following the multi-factor significance analysis, non-parametric pairwise comparisons 
were executed to isolate directional stochastic dominance patterns between groups. 
To counteract family-wise Type I error inflation across multiple group permutations 
without experiencing the severe statistical power depletion of a traditional 
Bonferroni adjustment, a sequentially rejective Holm-Bonferroni step-down 
correction is applied.
"""

def generate_holm_formula_latex():
    """
    Returns a LaTeX string defining the Holm-Bonferroni sequential step-down
    multi-comparison correction method.
    """
    latex = r"""
\subsubsection*{Post-hoc Pairwise Analysis: Holm-Bonferroni Correction}
To evaluate specific distribution differences between isolated developer interaction 
groups without violating normality or homoscedastic constraints, we implement a 
two-sample rank-order framework adjusted by the sequentially rejective Holm method.

The raw $P$-values for a set of $m$ concurrent hypotheses are sorted in ascending 
order:
\begin{equation}
    P_{(1)} \le P_{2} \le \dots \le P_{(m)}
\end{equation}

Each index $i$ ($1 \le i \le m$) is evaluated sequentially against a dynamically 
scaled significance threshold. The condition for rejecting the local null hypothesis 
$H_{(i)}$ is defined as:
\begin{equation}
    P_{(i)} \le \frac{\alpha}{m - i + 1}
\end{equation}

Where:
\begin{itemize}
    \item $\alpha$ is the nominal family-wise error criteria cutoff (configured to $0.05$).
    \item $m$ is the total number of simultaneous pairwise comparisons evaluated.
    \item $i$ is the ordered ranking position of the active sub-test segment.
\end{itemize}
The sequence terminates at the first instance where $P_{(i)} > \frac{\alpha}{m - i + 1}$, 
retaining all remaining null structures.
"""
    return latex

def generate_holm_latex(df, component, number_of_commits):
    # 1. Generate the standardized taxonomy label configuration [cite: 48, 85]
    df['Group'] = df['Role'] + " " + df['Tenure']
    unique_groups = sorted(df['Group'].unique())
    number_of_developers = len(df)
    # 2. Extract every unique combinations pair combination slot
    pair_combos = list(combinations(unique_groups, 2))
    
    # Storage maps to track raw vector calculations
    raw_p_values = []
    mean_differences = []
    comparison_meta = []
    
    # 3. Calculate separate raw metrics for every permutation slice
    for g1, g2 in pair_combos:
        v1 = df[df['Group'] == g1]['Value'].values
        v2 = df[df['Group'] == g2]['Value'].values
        
        # Calculate mean difference
        mdiff = np.mean(v1) - np.mean(v2)
        
        # Calculate non-parametric Mann-Whitney U probability [cite: 132, 133]
        # alternative='two-sided' mirrors the exploration test envelope
        try:
            _, p_raw = mannwhitneyu(v1, v2, alternative='two-sided')
        except ValueError:
            p_raw = 1.0  # Safe handler fallback for zero variance edge-cases
            
        raw_p_values.append(p_raw)
        mean_differences.append(mdiff)
        comparison_meta.append((g1, g2))
        
    # 4. Apply the sequentially rejective Holm-Bonferroni correction
    reject_array, adj_p_values, _, _ = multipletests(
        pvals=raw_p_values, 
        alpha=0.05, 
        method='holm'
    )
    
    latex_output_significant = ""
    latex_output_not_significant = ""
    
    # 5. Loop over the correction results arrays to construct LaTeX table rows
    for i in range(len(pair_combos)):
        g1, g2 = comparison_meta[i]
        group1 = g1.replace("_", "\\_")
        group2 = g2.replace("_", "\\_")
        
        latex =  f"{component} & {number_of_commits} & {number_of_developers} & "
        latex += f"{group1} & {group2} & "
        latex += f"{mean_differences[i]:.2f} & {adj_p_values[i]:.4f} \\\\ \n"
        
        if reject_array[i]:
            latex_output_significant += latex
        else:
            latex_output_not_significant += latex
            
    return latex_output_significant, latex_output_not_significant

def generate_and_save(component, developers, number_of_commits):
    base_file_name = get_base_file_name(FILE_NAME)
    sig_file_name = base_file_name + "_significant"
    not_sig_file_name = base_file_name + "_not_significant" 
    df = get_data_frame(developers, KNOWN_Y_AXIS)
    table_name = "Holm-Bonferroni Pairwise results for " + component + " and number of commits"
    commit_prefix = "all commits"
    headings = ["Component", "Commits", "Number of Developers", "Group A", "Group B", "Mean Diff", "Adj $P$ Value"]
    
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_heading(commit_prefix)
        save_to_latex_file(sig_file_name, base_file_name + ".tex", latex, DIRECTORY)
        save_to_latex_file(not_sig_file_name, base_file_name + ".tex", "", DIRECTORY)
    
    if number_of_commits == START_COMMIT_NUMBER:
        latex = start_latex_table("Significant " + table_name, headings, "l r r l l r r", "Significant Holm-Bonferroni Pairwise results for " + component)
        read_write_file.append_to_file(sig_file_name + ".tex", latex, DIRECTORY)
        latex = start_latex_table("Not Significant one and two commits " + table_name, headings, "l r r l l r r", "Not Significant Holm-Bonferroni Pairwise one and two commits results" + component)
        read_write_file.append_to_file(not_sig_file_name + ".tex", latex, DIRECTORY)
        
    sig_latex_table, not_sig_latex_table = generate_holm_latex(df, component, number_of_commits)
    read_write_file.append_to_file(sig_file_name + ".tex", sig_latex_table, DIRECTORY)
    read_write_file.append_to_file(not_sig_file_name + ".tex", not_sig_latex_table, DIRECTORY)
    
    if number_of_commits == 2:
        read_write_file.append_to_file(not_sig_file_name + ".tex", table_end(FILE_NAME  + "_no_sig_one_and_two" + component), DIRECTORY)
        latex = start_latex_table("Not Significant five and ten comits " + table_name, headings, "l r r l l r r", "Not Significant Holm-Bonferroni Pairwise five and ten commits results" + component)
        read_write_file.append_to_file(not_sig_file_name + ".tex", latex, DIRECTORY)
 
    if number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(sig_file_name + ".tex", table_end(FILE_NAME + "_sig_" + component ), DIRECTORY)
        read_write_file.append_to_file(not_sig_file_name + ".tex", table_end(FILE_NAME  + "_no_sig_five_and_ten" + component), DIRECTORY)
    
    if component == "methods" and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(base_file_name + ".tex", generate_holm_formula_latex() + "\n\\newpage \n", DIRECTORY)