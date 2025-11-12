from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_developer_commit import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_1.tex"
GRAPH_CAPTION = "Average number of new commits by {number} (x-axis) against the number of {contributor} developers (y-axis)"
FIGURE_CAPTION = "  \\caption{The average number of commits made against the number of " + FOUNDER + " and " + JOINER + " developers.}"

def get_developer_commit_by_contributor_stage(repository_id, contributor_stage):
    developers = []
    for developer in get_all_data(query(repository_id, contributor_stage)):
        developers.append(developer[COUNT])
    return developers

def generate_developer_commit_latex(repository_id, contributor_stage):
    developers = get_developer_commit_by_contributor_stage(repository_id, contributor_stage)
    title = "commits by " + contributor_stage + "s"
    return developer_graph(FILE_NAME, developers, title, repository_id, title, "", 
                           param_caption=GRAPH_CAPTION.format(contributor=contributor_stage, number=len(developers))) 

def generate_developer_commit(repository_id):
    latex_content = get_section_start(FILE_NAME, "sub") + "Repository " + str(repository_id) + " Developer Commits } \n" 
    latex_content += latex_start_graph()
    latex_content += generate_developer_commit_latex(repository_id, FOUNDER)
    latex_content += generate_developer_commit_latex(repository_id, JOINER)
    latex_content += FIGURE_CAPTION
    latex_content += latex_end_graph()
    return latex_content

def generate_and_save(repository_id):
    path = "repository/" + str(repository_id) + "/" 
    latex = generate_developer_commit(repository_id)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
