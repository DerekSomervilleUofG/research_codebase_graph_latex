from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.constants import *

FILE_NAME = __name__

def generate_glossary():
    latex = get_section_start(FILE_NAME, "sub") + "Summary} \n"
    latex += "\\begin{itemize} \n "
    latex += "\\item The " + FOUNDER + " developer starts in the first six months of a project. \n"
    latex += "\\item The late " + JOINER + " developers start after six months. \n"
    latex += "\\item " + SUSTAINED.capitalize() + " developers make " + str(DEVELOPER_HAS_NUMNER_OF_COMMITS) 
    latex += " or more commits and commit for " + str(DEVELOPER_PERIOD) + " days or more. \n"
    latex += "\\item " + TRANSIENT.capitalize() + " developers have fewer commits or commit for a shorter period. \n"
    latex += "\\end{itemize} \n"
    latex += "\\newpage \n"
    return latex