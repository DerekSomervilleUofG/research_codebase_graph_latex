from utility.ReadWriteFile import ReadWriteFile
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_repository_summary_table import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *
from codebase_graph_latex.calculate import *

BATCH_SIZE = 100
FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex" 

read_write_file = ReadWriteFile()


def section_heading():
    section = "\\section{Repository Summary Table} \n"
    section += "\\label{sec:" + FILE_NAME.replace(" ", "_") + "} \n"
    return section

def summary_table_start(number_of_repository):
    table_name = "Summary of " + word_engine.number_to_words(number_of_repository) + " open-source repositories identified from GitHub "
    table_name +=  SUSTAINED_JOINER_DESC
    table_name += "Five developers each worked on two repositories. "
    headings = ["ID", "Repo Name", 
                TRANSIENT.capitalize() + " " + FOUNDER.capitalize(),
                MODERATE.capitalize() + " " + FOUNDER.capitalize(),
                SUSTAINED.capitalize() + " " + FOUNDER.capitalize(),
                TRANSIENT.capitalize() + " Later " + JOINER.capitalize(),
                MODERATE.capitalize() + " Later " + JOINER.capitalize(),
                SUSTAINED.capitalize() + " Later " + JOINER.capitalize(),
                "Commit", "Start", "End"]
    return start_latex_table(table_name, headings, "rlrrrrrrrrl", "Summary of OOS GitHub Repositories")
        
def summary_table_end():
    table = "\\bottomrule\n"
    table += "\\end{tabular}\n"
    table += "}\n"
    table += "\\end{table} \n"
    table += "\\label{" + FILE_NAME + "}\n"
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
    total_transient_founder = 0
    total_moderate_founder = 0
    total_sustained_founder = 0
    total_transient_joiner = 0
    total_moderate_joiner = 0
    total_sustained_joiner = 0
    total_commit = 0
    latex_table = ""
    number_of_repository = 0
    for repository in repositories:
        if repository[REPOSITORY_ID] in repo_contribution:
            total_transient_founder += repo_contribution.get(repository[REPOSITORY_ID])[TRANSIENT_FOUNDER]
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
            latex_table += " & " + get_date_time(repository[MIN_DATE]).strftime('%d-%m-%Y')
            if get_integer(repository[MAX_DATE]) < 20240300000000:
                latex_table += " & " + get_date_time(repository[MAX_DATE]).strftime('%d-%m-%Y')
            else:
                latex_table += " & Ongoing"
            latex_table += " \\\\ \n"
            number_of_repository += 1
    latex_table += total_row(total_transient_founder, total_moderate_founder, total_sustained_founder, total_transient_joiner, total_moderate_joiner, total_sustained_joiner, total_commit)
    return latex_table, number_of_repository

def generate_and_save(repo_contribution):
    repositories = get_all_data(query())
    latex_table, number_of_repository = create_repository_summary_page(repositories, repo_contribution)
    latex_table = section_heading() + summary_table_start(number_of_repository) + latex_table
    latex_table += table_end(FILE_NAME)
    save_to_latex_file(get_base_file_name(FILE_NAME), BASE_FILE_NAME, latex_table, DIRECTORY)
    return number_of_repository

