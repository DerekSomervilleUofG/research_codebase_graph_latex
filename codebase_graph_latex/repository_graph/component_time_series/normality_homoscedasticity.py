from scipy import stats
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

FILE_NAME = __name__
SIGNIFICANT_P = 0.05

def section_sub_heading(time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    latex += "For all components touched for " + time_series + "} \n\n"
    latex += "A Shapiro-Wilk Test evaluates whether a sample distribution significantly differs from the normal distribution. "
    latex += "A Levene's test if the indepedent samples have equal variance.  \n\n"  
    latex += "Columns below:  \n"

    latex += r"""\begin{itemize}
                    \item{\textbf{Component} - Packages, classes or method touched.}
                    \item{\textbf{First *n* commits} - A sample of the first x number of commits for developers. }
                    \item{\textbf{Contributor Category} Transient, Moderate or Sustained. "vs." equals versus.}
                    \item{\textbf{Sample A $\mu$} - The mean average of the first sample A. In brackets the number of developers for sample A. }
                    \item{\textbf{Sample B $\mu$} - The mean average of the second sample B. In brackets the number of developers for sample b.}
                    \item{\textbf{Sample A Normality $P$} - The shaprio normality $P$ value of sample A. } 
                    \item{\textbf{Sample B Normality $P$} - The shaprio normality $P$ value of sample B. }
                    \item{\textbf{Variance Equality $P$} - The Levene variance equality p-values between sample A and B. }
                    \item{\textbf{Statistical Model} - A recommonded statistical model of Welch $t$ test; Mann-Whitney; Brunner Munzel }
                    \item{\textbf{Model $P$} - The $P$ value of the recommended test Welch $t$ test; Mann-Whitney; Brunner Munzel }
                \end{itemize}
    """
    latex += "\n"
    return latex

def get_table_name(category_compare):
    return "A Shapiro-Wilk test of " + category_compare + " sample normaility and a Levene's varience test between samples"

def get_headings(sample_a, sample_b):
    headings = ["Component", "First *n* commits", "Contributory Category", sample_a + r" $\mu$", sample_b + r" $\mu$", sample_a + " Normality $P$", sample_b + " Normality $P$", "Variance Equality $P$", "Statistical Models", "Model $P$"]
    return headings

def get_latex_heading():
    return "l r p{4cm} r r r r r l r "

def get_table_latex(category_compare, sample_a, sample_b):
    return start_latex_table(get_table_name(category_compare), get_headings(sample_a, sample_b), get_latex_heading())

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
            recommended += ", Mann-Whitney"
        p_value = u_p
    else:
        if recommended == "":
            recommended = "Brunner-Munzel"
        else:
            recommended += ", Brunner-Munzel"
        p_value = bm_p
    shapiro_p_a = format_p(shapiro_p_a)
    shapiro_p_b = format_p(shapiro_p_b)
    levene_p = format_p(levene_p)
    latex += f"{shapiro_p_a} & {shapiro_p_b} & "
    latex += f"{levene_p} &  {recommended} & {p_value:.4f} \\\\ \n"
    read_write_file.append_to_file(file_name + ".tex", latex, DIRECTORY)