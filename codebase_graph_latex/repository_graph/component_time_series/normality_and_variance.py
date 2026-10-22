from scipy import stats
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
SIGNIFICANT_P = 0.05

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "") 
    latex += "For all components touched for " + time_series + "} \n\n"
    #latex += diagnostic_table()
    latex += "\n"
    return latex

def diagnostic_table():
    latex = r"""\begin{table}[htbp]
\centering
\caption{Diagnostic $P$-Value Thresholds Required for Statistical Method Selection}
\label{tab:diagnostic_threshold_matrix}
\begin{tabular}{lccc}
\toprule
\textbf{Statistical Method} & \textbf{Shapiro-Wilk A ($P$)} & \textbf{Shapiro-Wilk B ($P$)} & \textbf{Levene's Test ($P$)} \\
\midrule
\textbf{Student's $t$-test} & $\ge 0.05$ (Normal) & $\ge 0.05$ (Normal) & $\ge 0.05$ (Equal Variance) \\
\textbf{Standard ANOVA}     & $\ge 0.05$ (Normal) & $\ge 0.05$ (Normal) & $\ge 0.05$ (Equal Variance) \\
\textbf{Tukey HSD}     & $\ge 0.05$ (Normal) & $\ge 0.05$ (Normal) & $\ge 0.05$ (Equal Variance) \\
\textbf{Welch's $t$-test}   & $\ge 0.05$ (Normal) & $\ge 0.05$ (Normal) & \textless{} 0.05 (Unequal Variance) \\
\textbf{Mann-Whitney $U$ test} & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Skewed) & $\ge 0.05$ (Equal Variance) \\
\textbf{Brunner-Münzel test}   & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Unequal Variance) \\
\textbf{ART Anova test}   & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Unequal Variance) \\
\textbf{Holm Bonferroni}   & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Skewed) & \textless{} 0.05 (Unequal Variance) \\
\bottomrule
\end{tabular}
\end{table}
"""
    return latex

def get_table_name(component, category_compare, commit_describe, headings):
    latex = "Statistical significance tests of the difference of number of " + component + " touched "
    latex += "by " + category_compare + " after various first " + commit_describe + " commits and for "
    latex += rf"different cohorts of contributors (all, moderate and sustained). "
    latex += "All distributions were found to be non-normal, so statistical tests were selected "
    latex += "based on the variance equality of distributions (Brumner-Munzel or Mann-Whitney). "
    latex += generate_table_name_headings(headings)
    return latex

def get_headings(sample_a, sample_b):
    return {
        "First $n$ commits": "A sample of the first x number of commits for developers.",
        "Contributory Category": 'Transient, Moderate or Sustained. "vs." equals versus.',
        rf"{sample_a} $\mu$": f"The mean average of the first sample ({sample_a}).",
        rf"{sample_a} \#": f"The number of developers in the first sample ({sample_a}).",
        rf"{sample_b} $\mu$": f"The mean average of the second sample ({sample_b}).",
        rf"{sample_b} \#": f"The number of developers in the second sample ({sample_b}).",
        "Variance Equality $P$": f"The Levene variance equality $p$-value between {sample_a} and {sample_b}.",
        "Statistical Models": "A recommended statistical model of Welch $t$-test; Mann-Whitney; Brunner Münzel.",
        "Model $P$": "The $P$-value of the recommended statistical test.",
    }

def get_latex_heading():
    return "r p{4cm} c c c c r l r "

def get_table_latex(component, category_compare, headings, number_of_commits_description, heading_def):
    return start_latex_table(get_table_name(component, category_compare, number_of_commits_description, heading_def), headings, get_latex_heading(), "Statistical Significance Normality and Variance tests for " + component + " for " + category_compare + " for " + number_of_commits_description)

def format_p(val):
        if val < 0.001:
            return r"\textless 0.001"  # Keeps it clean and academically correct
        return f"{val:.4f}"

def generate_normal_comparison_latex(latex, sample_a_values, sample_b_values, file_name, u_p, bm_p):
    shapiro_stat_a, shapiro_p_a = stats.shapiro(sample_a_values)
    shapiro_stat_b, shapiro_p_b = stats.shapiro(sample_b_values)
    levene_stat, levene_p = stats.levene(sample_a_values, sample_b_values)
    recommended = ""
    if shapiro_p_a >= SIGNIFICANT_P or shapiro_p_b >= SIGNIFICANT_P:
        recommended = "Welch $t$"
    if levene_p >= SIGNIFICANT_P:
        if recommended == "":
            recommended = "Mann-Whitney"
        else:
            recommended += "Mann-Whitney"
        p_value = u_p
    else:
        if recommended == "":
            recommended = "Brunner-Münzel"
        else:
            recommended += "Brunner-Münzel"
        p_value = bm_p
    shapiro_p_a = format_p(shapiro_p_a)
    shapiro_p_b = format_p(shapiro_p_b)
    levene_p = format_p(levene_p)
    latex += f"{levene_p} &  {recommended} & {p_value:.4f} \\\\ \n"
    read_write_file.append_to_file(file_name + ".tex", latex, DIRECTORY)