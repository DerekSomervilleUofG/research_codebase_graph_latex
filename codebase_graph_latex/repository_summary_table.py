from utility.ReadWriteFile import ReadWriteFile
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_repository_summary_table import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.calculate import *
import inflect

BATCH_SIZE = 100
FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex" 

read_write_file = ReadWriteFile()
word_engine = inflect.engine()

def section_heading(number_of_repository):
    section = "\\begin{landscape}"
    section += "\\subsection{Repository Summary Table} \n"
    section += "\\begin{table}[h!]\n"
    section += "\\centering\n"
    section += "\\caption{Summary of " + word_engine.number_to_words(number_of_repository) + " open-source repositories identified from GitHub"
    section += " that have at least 1000 pull requests and at least " + word_engine.number_to_words(MINIMUM_NUMBER_OF_COMMTIS) 
    section += " " + SUSTAINED + " late " + JOINER + " developers. " + SUSTAINED_JOINER_DESC
    section += DEVELOPER_IGNORE 
    section += "Please note that five developers each worked on two repositories. "
    section += " } \n"
    return section

def summary_table_start():
    table = "\\begin{tabular}{rlrrrrrrrrr}\n"
    table += "\\toprule\n"
    table += "\\textbf{ID} & \\textbf{Repo Name} "
    table += " & \\makecell{\\textbf{" + TRANSIENT.capitalize() + "} \\\\ \\textbf{" + FOUNDER.capitalize() + "} } " 
    table += " & \\makecell{\\textbf{" + MODERATE.capitalize() + "} \\\\ \\textbf{" + FOUNDER.capitalize() + "} } " 
    table += " & \\makecell{\\textbf{" + SUSTAINED.capitalize() + "} \\\\ \\textbf{" + FOUNDER.capitalize() + "} } " 
    table += " & \\makecell{\\textbf{" + TRANSIENT.capitalize() + "} \\\\ \\textbf{" + JOINER.capitalize() + "} } " 
    table += " & \\makecell{\\textbf{" + MODERATE.capitalize() + "} \\\\ \\textbf{" + JOINER.capitalize() + "} } " 
    table += " & \\makecell{\\textbf{" + SUSTAINED.capitalize() + "} \\\\ \\textbf{" + JOINER.capitalize() + "} } " 
    table += " & \\textbf{Commit} & \\textbf{Start} & \\textbf{End} \\\\ \n"
    table += "\\midrule\n"
    return table
        
def summary_table_end():
    table = "\\bottomrule\n"
    table += "\\end{tabular}\n"
    table += "\\end{table}\n"
    table += "\\end{landscape} \n"
    table += "\\newpage \n"
    return table

def total_row(total_transient_founder, total_moderate_founder, total_sustained_founder, total_transient_joiner, total_moderate_joiner, total_sustained_joiner, total_commit):
    latex = "\\hline \n"
    latex += " & Total & " + str(total_transient_founder) + " & " + str(total_moderate_founder) + " & " + str(total_sustained_founder)
    latex += " & " +  str(total_transient_joiner) + " & " + str(total_moderate_joiner) + " & " + str(total_sustained_joiner) 
    latex += " & " + str(total_commit) + " &  & \\\\ \n"
    latex += "\\hline \n"
    return latex

def create_repository_summary_page(repositories, repo_contribution):
    global number_of_repository
    total_trainsient_founder = 0
    total_moderate_founder = 0
    total_sustained_founder = 0
    total_transient_joiner = 0
    total_moderate_joiner = 0
    total_sustained_joiner = 0
    total_commit = 0
    latex_table = ""
    number_of_repository = 0
    for repository in repositories:
        total_trainsient_founder += repo_contribution.get(repository[REPOSITORY_ID])[TRANSIENT_FOUNDER]
        total_moderate_founder += repo_contribution.get(repository[REPOSITORY_ID])[MODERATE_FOUNDER]
        total_sustained_founder += repo_contribution.get(repository[REPOSITORY_ID])[SUSTAINED_FOUNDER]
        total_transient_joiner += repo_contribution.get(repository[REPOSITORY_ID])[TRANSIENT_JOINER]
        total_moderate_joiner += repo_contribution.get(repository[REPOSITORY_ID])[MODERATE_JOINER]
        total_sustained_joiner += repo_contribution.get(repository[REPOSITORY_ID])[SUSTAINED_JOINER]
        latex_table +=  str(repository[REPOSITORY_ID]) 
        latex_table += " & " + repository[REPO_NAME]
        latex_table += " & " + str(repo_contribution.get(repository[REPOSITORY_ID])[TRANSIENT_FOUNDER])
        latex_table += " & " + str(repo_contribution.get(repository[REPOSITORY_ID])[MODERATE_FOUNDER])
        latex_table += " & " + str(repo_contribution.get(repository[REPOSITORY_ID])[SUSTAINED_FOUNDER])
        latex_table += " & " + str(repo_contribution.get(repository[REPOSITORY_ID])[TRANSIENT_JOINER])
        latex_table += " & " + str(repo_contribution.get(repository[REPOSITORY_ID])[MODERATE_JOINER])
        latex_table += " & " + str(repo_contribution.get(repository[REPOSITORY_ID])[SUSTAINED_JOINER])
        latex_table += " & " + str(repository[COMMIT_COUNT])
        total_commit += repository[COMMIT_COUNT]
        latex_table += " & " + get_date_time(repository[MIN_DATE]).strftime('%Y-%b-%d')
        if get_integer(repository[MAX_DATE]) < 20240300000000:
            latex_table += " & " + get_date_time(repository[MAX_DATE]).strftime('%Y-%b-%d')
        else:
            latex_table += " & On going"
        latex_table += " \\\\ \n"
        number_of_repository += 1
    latex_table += total_row(total_trainsient_founder, total_moderate_founder, total_sustained_founder, total_transient_joiner, total_moderate_joiner, total_sustained_joiner, total_commit)
    return latex_table, number_of_repository

def generate_and_save(repo_contribution):
    latex_table, number_of_repository = create_repository_summary_page(get_all_data(query()), repo_contribution)
    latex_table = section_heading(number_of_repository) + summary_table_start() + latex_table
    latex_table += summary_table_end()
    read_write_file.write_file(get_file_name(FILE_NAME), latex_table, DIRECTORY)  
    latex = "\\input{repository/" + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY) 
    return number_of_repository

