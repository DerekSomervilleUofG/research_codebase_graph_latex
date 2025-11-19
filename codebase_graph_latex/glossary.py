from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.constants import *
import inflect

word_engine = inflect.engine()
FILE_NAME = __name__

def generate_glossary():
    latex = get_section_start(FILE_NAME, "sub") + "Summary} \n"
    latex += "\\begin{itemize} \n "
    latex += "\\item The " + FOUNDER + " developer starts in the first six months of a project. \n"
    latex += "\\item Late " + JOINER + " developers begin after six months. \n"
    latex += "\\item " + TRANSIENT.capitalize() + " developers have " + word_engine.number_to_words(TRANSIENT_COMMITS) + " (" + str(TRANSIENT_COMMITS) + ")"
    latex += " or fewer commits. \n"
    latex += "\\item " + MODERATE.capitalize() + " developers have more than " + word_engine.number_to_words(TRANSIENT_COMMITS) + " (" + str(TRANSIENT_COMMITS) + ")"
    latex += " commits but fewer than " + str(DEVELOPER_HAS_NUMNER_OF_COMMITS) 
    latex += " commits or commits for less than " + str(DEVELOPER_PERIOD) + " days. \n"
    latex += "\\item " + SUSTAINED.capitalize() + " developers make " + str(DEVELOPER_HAS_NUMNER_OF_COMMITS) 
    latex += " or more commits and commit for " + str(DEVELOPER_PERIOD) + " days or more. \n"
    latex += "\\end{itemize} \n"
    latex += "\\newpage \n"
    return latex