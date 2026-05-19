from scipy import stats
import pandas as pd
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *
from codebase_graph_latex.repository_graph.component_time_series.normality_homoscedasticity import get_table_latex
from codebase_graph_latex.repository_graph.component_time_series.normality_homoscedasticity import generate_normal_comparison_latex

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
previous_file_name = None
previous_normal_file_name = None
previous_a_category = None

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n\n"
    latex += "A Welch $t$-test was employed to determine if the mean contributions of Group A "
    latex += "differ significantly from Group B. This test is appropriate for continuous data "
    latex += "and is robust to unequal variances. \n \n"  
    latex += "Complementarily, the Mann-Whitney $U$ (MWU) test was used to assess stochastic dominance "
    latex += "by ranking data points. This non-parametric approach does not require a normal distribution "
    latex += "and is highly resistant to outliers. \n \n"
    latex += "The Brunner-Munzel test was employed as a robust non-parametric method to determine "
    latex += "if the relative treatment effects of Group A differ significantly from Group B. "
    latex += "This test is highly appropriate for skewed count data and is completely robust to "
    latex += "unequal variances and large group size imbalances. Complementarily, Cliff's $\\delta$ "
    latex += "and the Probability of Superiority ($PS$) are provided as robust non-parametric effect sizes "
    latex += "to quantify the directional dominance magnitude between the samples. \n \n"
    latex += "Columns below:  \n"

    latex += r"""\begin{itemize}
                    \item{\textbf{Component} - Packages, classes or method touched.}
                    \item{\textbf{First *n* commits} - A sample of the first x number of commits for developers. }
                    \item{\textbf{Contributor Category} Transient, Moderate or Sustained. "vs." equals versus.}
                    \item{\textbf{Sample A $\mu$} - The mean average of the first sample A. In brackets the number of developers for sample A. }
                    \item{\textbf{Sample B $\mu$} - The mean average of the second sample B. In brackets the number of developers for sample b.}
                    \item{\textbf{Welch Statisic} - This is the magnitude of the change, greater than 2.0 generally indicates a significant change. }
                    \item{\textbf{Welch $P$} - A significance test of the difference between sample A and sample B. A $p$ \textless{} 0.05 indicates a significant difference between samples. }
                    \item{\textbf{MWU $P$} - The Mann-Whitney $p$-value. A significance test of the difference between sample A and sample B. A $p$ \textless{} 0.05 indicates a significant difference between samples.} 
                    \item{\textbf{BM $P$} - The Brunner-Munzel asymptotic $p$-value. A $p$ \textless{} 0.05 indicates a significant difference in relative effects.}
                    \item{\textbf{Brunner-Munzel W} - The robust test statistic. Large absolute values indicate a significant structural shift.} 
                    \item{\textbf{Cliff's $\delta$} - Non-parametric effect size bound between -1 and +1, evaluating directional dominance.}
                    \item{\textbf{Prob. of Superiority ($PS$)} - The empirical probability ($0$ to $1$) that a randomly selected developer from Sample A outranked a developer from Sample B.} 
                \end{itemize}
    """
    latex += "\n"
    return latex

def generate_mann_whitney_formula_latex(sample_a_b):
    """
    Returns a LaTeX string defining the Mann-Whitney U test model
    for developer architectural component analysis.
    """
    group_a = sample_a_b[0].capitalize()
    group_b = sample_a_b[1].capitalize()
    latex = r"""

\paragraph{Mann-Whitney U Test}
To evaluate the differences in the stochastic dominance of architectural component exploration between primary roles (\textbf{Sample A} vs. \textbf{Sample B}) without assuming a normal distribution, the non-parametric Mann-Whitney $U$ test (Wilcoxon rank-sum test) is employed. 

The data from both independent groups are combined and ranked globally from lowest ($1$) to highest ($N_1 + N_2$), resolving ties by assigning the average rank. The $U$ statistic for Sample A ($U_1$) is calculated as:

\begin{equation}
    U_1 = R_1 - \frac{N_1(N_1 + 1)}{2}
\end{equation}

Where:
\begin{itemize}
    \item $N_1$ is the sample size of Sample A.
    \item $R_1$ is the sum of the ranks assigned to Sample A.
    \item The total number of pairwise comparisons (maximum possible pairs) is defined by $N_1 \times N_2$.
\end{itemize}

\paragraph{Normal Approximation for Large Samples}
Given the substantial sample sizes present in repository participant metrics, the distribution of the $U$ statistic rapidly approaches a normal distribution. The asymptotic significance is determined using a standard normal $Z$-score approximation:

\begin{equation}
    Z = \frac{U_1 - \mu_U}{\sigma_U}
\end{equation}

Where the expected mean ($\mu_U$) and standard deviation ($\sigma_U$) under the null hypothesis of identical distributions are defined as:

\begin{equation}
    \mu_U = \frac{N_1 N_2}{2}, \quad \sigma_U = \sqrt{\frac{N_1 N_2 (N_1 + N_2 + 1)}{12}}
    \label{eq:mwu_normal}
\end{equation}

A calculated $p$-value lower than the alpha threshold ($p < 0.05$) indicates a statistically significant difference in the rank-order distributions of the two groups, demonstrating that one developer role systematically outranks the other in codebase exploration.
"""
    return latex

def generate_bruner_munzel_formula_latex(sample_a_b):
    """
    Returns a LaTeX string defining the Brunner-Munzel model 
    and Cliff's Delta effect size for developer analysis.
    """
    group_a = sample_a_b[0].capitalize()
    group_b = sample_a_b[1].capitalize()
    latex = r"""

\paragraph{Brunner-Munzel Test}
To test for differences in the stochastic distributions of primary roles (\textbf{Sample A} vs. \textbf{Sample B}) without assuming normal distribution or variance homogeneity, the Brunner-Munzel test is applied. The test statistic $W$ is defined as:

\begin{equation}
    W = \sqrt{\frac{N_1 N_2}{N_1 + N_2}} \cdot \frac{\hat{p} - \frac{1}{2}}{\sqrt{\hat{\sigma}^2}}
\end{equation}

Where $\hat{p}$ represents the relative treatment effect (Probability of Superiority), reflecting the probability that a random observation from Sample A is larger than one from Sample B plus half the probability that they are equal.

\paragraph{Cliff's $\delta$ Effect Size}
To complement hypothesis significance testing with a distribution-free magnitude metric, Cliff's $\delta$ is tracked to express the degree of dominance of one sample over the other:

\begin{equation}
    \delta = \frac{\sum_{i=1}^{N_1} \sum_{j=1}^{N_2} \mathrm{sign}(X_{1i} - X_{2j})}{N_1 N_2}
\end{equation}

Where the $\mathrm{sign}$ function yields $+1$ when an element of Sample A is larger than Sample B, $0$ if equal, and $-1$ if smaller. Effect sizes are interpreted using standard empirical thresholds ($|\delta| < 0.147$ is negligible, $\ge 0.147$ is small, $\ge 0.330$ is medium, and $\ge 0.474$ is large).
"""
    return latex

def generate_welch_formula_latex(sample_a_b):
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

def generate_formula_latex(sample_a_b):
    latex = generate_welch_formula_latex(sample_a_b)
    latex += generate_mann_whitney_formula_latex(sample_a_b)
    latex += generate_bruner_munzel_formula_latex(sample_a_b)
    return latex

def cliffts_delta_and_ps(group_a, group_b):
    """
    Calculates Cliff's Delta (d) and the Probability of Superiority (PS)
    for two independent groups using vectorized numpy operations.
    """
    if len(group_a) == 0 or len(group_b) == 0:
        return 0.0, 0.5
    
    # Vectorized pairwise comparison matrix
    # Sign returns 1 if a > b, 0 if a == b, -1 if a < b
    diff_matrix = np.sign(np.asarray(group_a)[:, None] - np.asarray(group_b))
    delta = np.mean(diff_matrix)
    
    # Direct mathematical conversion to Probability of Superiority
    ps = (delta + 1) / 2
    return delta, ps

def determine_category(cat_name, categories):
    first_category_full = cat_name.split(" ")[0]
    if first_category_full not in categories:
        categories.insert(len(categories) // 2,first_category_full)
    second_category_full = cat_name.replace(first_category_full, "").strip()
    if second_category_full not in categories:
        categories.append(second_category_full)
    

def formate_list(sample_list, samples):
    if len(sample_list) == 4:
        category = "All"
    elif len(sample_list) == 2:
        category = sample_list[0]
    elif len(sample_list) == 1:
        category = samples[0] + " \& " + samples[1]
    elif len(sample_list) == 0:
        category = "No data"
    else:
        category = ",".join(sample_list[:-2]) + " \& " + sample_list[-2] 
    return category.capitalize()


def filter_data(developers_dict, samples, unit):
    sample_a_values = []
    sample_b_values = []
    a_categories = []
    b_categories = []
    for cat_name, dev_data in developers_dict.items():
        touched_data = populate_touched_data(dev_data, unit)
        final_values = [series[-1] for series in touched_data]
        
        if samples[0] in cat_name.lower():
            sample_a_values.extend(final_values)
            determine_category(cat_name, a_categories)
        elif isinstance(samples[1], str) and samples[1] in cat_name.lower():
            sample_b_values.extend(final_values)
        elif len(samples[1]) == 2 and samples[1][0] in cat_name.lower():
            sample_b_values.extend(final_values)
        elif len(samples[1]) == 2 and samples[1][1] in cat_name.lower():
            sample_b_values.extend(final_values)

    return sample_a_values, sample_b_values, formate_list(a_categories, samples)

def generate_simple_comparison_latex(sample_a_values, sample_b_values, component, a_category, number_of_commits, normal_file_name):
    
    total_pairs = len(sample_a_values) * len(sample_b_values)
    # 1. Welch's T-Test (Parametric)
    t_stat, t_p = stats.ttest_ind(sample_a_values, sample_b_values, equal_var=False)
    
    # 2. Mann-Whitney U (Non-Parametric)
    u_stat, u_p = stats.mannwhitneyu(sample_a_values, sample_b_values)

    if len(sample_a_values) > 0 and len(sample_b_values) > 0:
        bm_stat, bm_p = stats.brunnermunzel(sample_a_values, sample_b_values)
        delta, ps = cliffts_delta_and_ps(sample_a_values, sample_b_values)
    else:
        bm_stat, bm_p, delta, ps = 0, 1.0, 0, 0.5

    mean_a = np.mean(sample_a_values) if sample_a_values else 0
    mean_b = np.mean(sample_b_values) if sample_b_values else 0
    # Build a simple DataFrame for the LaTeX table
    a_number = str(len(sample_a_values))
    b_number = str(len(sample_b_values))
    component_clean = component.replace("_", "-").capitalize() 
    latex =  f"{component_clean} & {number_of_commits} & "
    latex +=  f"{a_category} & "
    latex += f" {mean_a:.2f} ({a_number}) & {mean_b:.2f} ({b_number}) & "
    generate_normal_comparison_latex(latex, sample_a_values, sample_b_values, normal_file_name, u_p, bm_p)
    latex += f"{t_stat:.2f} & {t_p:.4f} & "
    latex += f"{u_p:.4f} & "
    latex += f"{bm_p:.4f} & {bm_stat:.2f} & "
    latex += f"{delta:.3f} & {ps:.3f} \\\\ \n"
    return latex

def generate_and_save(component, developers, number_of_commits, sample_a_b, file_name, normal_file_name):
    global previous_file_name, previous_a_category, previous_normal_file_name
    path = "repository/" 
    commit_prefix = "all commits"
    sample_a_values, sample_b_values, a_category = filter_data(developers, sample_a_b, TIME_SERIES_NUMBER_OF_COMMIT)
    if component == "methods" and sample_a_b[0] == MODERATE and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(previous_file_name + ".tex", table_end(), path)
        read_write_file.append_to_file(previous_normal_file_name + ".tex", table_end(), path)
    if component == "packages" and sample_a_b[0] in [FOUNDER] and number_of_commits == START_COMMIT_NUMBER:
        number_of_commit_desc = "1, 5, 10 and 20 "
        category_compare = "different categories of " + FOUNDER + " versus different categories of late " + JOINER + " "
        sample_a = sample_a_b[0].capitalize()
        if isinstance(sample_a_b[1], str):
            sample_b = sample_a_b[1].capitalize()
        elif len(sample_a_b[1]) == 2:
            sample_b = sample_a_b[1][0].capitalize() + r" \& " + sample_a_b[1][1]
    if component == "packages" and sample_a_b[0] in [TRANSIENT] and number_of_commits == START_COMMIT_NUMBER:
        number_of_commit_desc = "1, 5 and 10 "
        category_compare = " sample a category versus sample b category " 
        sample_a = "Sample A"
        sample_b = "Sample B"
    if sample_a_b[0] in [TRANSIENT, MODERATE]:
        if isinstance(sample_a_b[1], str):
            a_category = sample_a_b[0].capitalize() + r" vs. " + sample_a_b[1]
        elif len(sample_a_b[1]) == 2:
            a_category = sample_a_b[0].capitalize() + r" vs. " + sample_a_b[1][0] + r" \& " + sample_a_b[1][1]
    
    if component == "packages" and (sample_a_b[0] in [FOUNDER] or sample_a_b[1] in [MODERATE]) and number_of_commits == START_COMMIT_NUMBER:
        headings = ["Component", "First *n* commits", "Contributory Category", sample_a + r" $\mu$", sample_b + r" $\mu$", "Welch Statistic", "Welch $P$", "MWU $P$", "BM $P$", "Brunner-Munzel $W$", "Cliff's $\\delta$", "Prob. Sup. ($PS$)" ]
        table_name = "Statistical significance tests of " + category_compare
        table_name += " touches of different granularities of component (package, class, method) after " + number_of_commit_desc + " commits for contributors. "
        table_name += "The significance has been calculated for the following statsitical tests: Welch $t$-test, Mann-Whitney and Brunner Munzel. "
        latex = r"\begin{landscape}" + "\n"        
        latex += start_latex_table(table_name , headings, "l r p{4cm} r r r r r r r r r r r r r")
        read_write_file.append_to_file(file_name + ".tex", latex, path)
        latex = r"\begin{landscape}" + "\n"   
        latex += get_table_latex(category_compare, sample_a, sample_b)
        read_write_file.append_to_file(normal_file_name + ".tex", latex, path)
        
    if len(sample_a_values) > 0 and previous_a_category != a_category:
        latex_table = generate_simple_comparison_latex(sample_a_values, sample_b_values, component, a_category, number_of_commits, normal_file_name).replace("_", "\\_")
        read_write_file.append_to_file(file_name + ".tex", latex_table, path)
        previous_a_category = a_category
    if component == "methods" and sample_a_b[0] == MODERATE and number_of_commits == END_COMMIT_NUMBER:
        read_write_file.append_to_file(file_name + ".tex", table_end(), path)
        read_write_file.append_to_file(file_name + ".tex", generate_formula_latex(sample_a_b) + "\n\\newpage \n", path)
        read_write_file.append_to_file(normal_file_name + ".tex", table_end(), path)
        
    previous_file_name = file_name
    previous_normal_file_name = normal_file_name
         