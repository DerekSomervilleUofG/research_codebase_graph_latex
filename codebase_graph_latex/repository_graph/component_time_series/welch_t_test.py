from scipy import stats
import pandas as pd
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import populate_touched_data


FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n"
    latex += "A Welch T Test table for all components touched on average. \n"
    return latex

def section_sub_sub_heading(component, time_series):
    latex = get_section_start(FILE_NAME, "subsub") 
    latex += "For " + component + " touched for a " + time_series + "} \n"
    latex += "A Welch T Test table for " + component + " touched on average. \n"
    return latex

def generate_simple_comparison_latex(developers_dict, unit, component):
    founders_values = []
    joiners_values = []

    for cat_name, dev_data in developers_dict.items():
        touched_data = populate_touched_data(dev_data, unit)
        final_values = [series[-1] for series in touched_data]
        
        if "founder" in cat_name.lower():
            founders_values.extend(final_values)
        else:
            joiners_values.extend(final_values)

    # 1. Welch's T-Test (Parametric)
    t_stat, t_p = stats.ttest_ind(founders_values, joiners_values, equal_var=False)
    
    # 2. Mann-Whitney U (Non-Parametric)
    u_stat, u_p = stats.mannwhitneyu(founders_values, joiners_values)

    # Build a simple DataFrame for the LaTeX table
    results = pd.DataFrame({
        "Metric": ["Welch's t-test", "Mann-Whitney U"],
        "Statistic": [t_stat, u_stat],
        "p-Value": [t_p, u_p]
    })

    component_clean = component.replace("_", "-")
    return results.to_latex(
        position="h!",
        index=False,
        caption=f"Comparison of Founders vs Late Joiners for {component_clean}",
        label=f"tab:compare-{component_clean}",
        float_format="%.4f"
    )

def generate_statistical_formula_latex():
    """
    Returns a LaTeX string defining both the Two-Way ANOVA and 
    Welch's t-test models for developer analysis.
    """
    latex = r"""
\subsubsection*{Statistical Models}

\paragraph{Two-Way ANOVA with Interaction}
The differences across all categories are assessed using a Two-Way ANOVA. The value for an individual developer metric ($Y_{ijk}$) is modeled as:

\begin{equation}
    Y_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \epsilon_{ijk}
\end{equation}

Where $\mu$ is the grand mean, $\alpha_i$ is the \textbf{Role} effect, $\beta_j$ is the \textbf{Tenure} effect, $(\alpha\beta)_{ij}$ is the interaction, and $\epsilon_{ijk}$ is the residual error. The significance is determined by the $F$-statistic:
\begin{equation}
    F = \frac{MS_{factor}}{MS_{residual}}
\end{equation}

\paragraph{Welch's t-test}
To specifically compare the two primary roles (\textbf{Founders} vs. \textbf{Late Joiners}) without assuming equal variances or sample sizes, Welch's $t$-test is employed. The $t$-statistic is defined as:

\begin{equation}
    t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{N_1} + \frac{s_2^2}{N_2}}}
\end{equation}

Where:
\begin{itemize}
    \item $\bar{X}_1, \bar{X}_2$ are the sample means of Founders and Late Joiners.
    \item $s_1^2, s_2^2$ are the sample variances.
    \item $N_1, N_2$ are the sample sizes.
\end{itemize}

The degrees of freedom ($\nu$) for this test are calculated using the Welch-Satterthwaite equation:
\begin{equation}
    \nu \approx \frac{\left(\frac{s_1^2}{N_1} + \frac{s_2^2}{N_2}\right)^2}{\frac{(s_1^2/N_1)^2}{N_1-1} + \frac{(s_2^2/N_2)^2}{N_2-1}}
\end{equation}
"""
    return latex

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
    latex_table = generate_simple_comparison_latex(developers, TIME_SERIES_NUMBER_OF_COMMIT, component).replace("_", "\\_")
    read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", latex_table, path)
    if component == "methods":
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", generate_statistical_formula_latex() + "\n \\newpage \n", path)
         