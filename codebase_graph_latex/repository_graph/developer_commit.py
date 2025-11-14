from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_developer_commit import *
from codebase_graph_latex.store_developer_data import * 

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
GRAPH_CAPTION = "Total commits (x-axis) against {number} {contributor} developers (y-axis)"
FIGURE_CAPTION = "  \\caption{The average number of commits made against the number of " + FOUNDER + " and " + JOINER + " developers.}"
MAX_Y_AXIS = 700
MAX_X_AXIS = 1500
MINIMUM_COMMITS = 10
component = "packages"

def get_developer_commit_by_contributor_stage(contributor_stage):
    stage_developers = developer_component_knowledge[contributor_stage][component]
    developers = []
    for id, developer in stage_developers.items():
        if developer[NUMBER_OF_COMMIT][-1] >= MINIMUM_COMMITS:
            developers.append(developer[NUMBER_OF_COMMIT][-1])
    return developers

def generate_developer_commit_latex(contributor_stage):
    developers = get_developer_commit_by_contributor_stage(contributor_stage)
    title = "commits by " + contributor_stage + "s"
    return developer_graph(FILE_NAME, developers, title, 0, title, "", 
                           param_caption=GRAPH_CAPTION.format(contributor=contributor_stage, number=len(developers)), param_x_axis=title, max_x_axis=MAX_X_AXIS, max_y_axis=MAX_Y_AXIS) 

def generate_developer_commit():
    latex_content = get_section_start(FILE_NAME, "sub") + " Developer Commits } \n" 
    latex_content += latex_start_graph()
    latex_content += generate_developer_commit_latex(TRANSIENT_FOUNDER)
    latex_content += generate_developer_commit_latex(TRANSIENT_JOINER)
    latex_content += generate_developer_commit_latex(SUSTAINED_FOUNDER)
    latex_content += generate_developer_commit_latex(SUSTAINED_JOINER)
    latex_content += FIGURE_CAPTION
    latex_content += latex_end_graph()
    return latex_content

def generate_and_save():
    path = DIRECTORY 
    latex = generate_developer_commit()
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
