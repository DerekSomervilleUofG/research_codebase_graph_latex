from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *

FILE_NAME = __name__

CAPTION = "{type} additional {component} touched "
FIGURE_CAPTION = "Additional {component} touched by month. "

def section_sub_heading(repository_id, component):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " Equation for frequency predict " + component + " touched} \n"
    latex += "Poisson / Negative Binomial regression (core result) for " + component + " touched. \n "
    
    latex += r"""
    \begin{equation}
    \log(\mu_{it}) = \alpha + \beta_1 \cdot \text{Packages}_{it} + \beta_2 \cdot 
    \text{Files}_{it} + \beta_3 \cdot \text{Methods}_{it} + \sum_{d=2}^{7} \gamma_d \cdot \mathbf{1}\{\text{DOW}_t = d\}
    \end{equation} \n"""
    latex += "\\newpage \n"
    return latex

def generate_developer(path, component, data, type):
    return ""

def generate_latex(path, component, founder_transient_developers, founder_sustained_developers, joiner_transient_developers, joiner_sustained_developers):
    all_data = founder_transient_developers | founder_sustained_developers | joiner_transient_developers | joiner_sustained_developers
    latex = generate_developer(path + component + "/", component, all_data, "All")
    latex += generate_developer(path + component + "/", component,founder_transient_developers, FOUNDER + " " + TRANSIENT)
    latex += generate_developer(path + component + "/", component, founder_sustained_developers, 
                                                FOUNDER + " " + SUSTAINED)
    latex += generate_developer(path + component + "/", component, joiner_transient_developers,  
                                                JOINER + " " + TRANSIENT)
    latex += generate_developer(path + component + "/", component, joiner_sustained_developers, 
                                                JOINER + " " + SUSTAINED)
    return latex

def generate_and_save(repository_id, component, founder_transient_developers, founder_sustained_developers, joiner_transient_developers, joiner_sustained_developers):
    path = "repository/" + str(repository_id) + "/" 
    base_file_name = "repository2.tex"
    latex = section_sub_heading(repository_id, component)
    latex += generate_latex(path, component, founder_transient_developers, founder_sustained_developers, joiner_transient_developers, joiner_sustained_developers)
    read_write_file.write_file(get_base_file_name(FILE_NAME) + "." + component + ".tex", latex, path)
    base_latex =  "\\input{" + path + get_base_file_name(FILE_NAME) + "." + component + "}\n"
    read_write_file.append_to_file(base_file_name, 
                                   base_latex, 
                                    DIRECTORY)