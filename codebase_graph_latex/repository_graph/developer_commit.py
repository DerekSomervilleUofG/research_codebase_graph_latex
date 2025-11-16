from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_developer_commit import *
from codebase_graph_latex.store_developer_data import * 

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
MINIMUM_COMMITS = 10
GRAPH_CAPTION = "{contributor} {number}"
FIGURE_CAPTION = "  \\caption{Histomagram of number of commits made by four categories of developers, excluding developers with less than " + word_engine.number_to_words(MINIMUM_COMMITS) + " (" + str(MINIMUM_COMMITS) +  ")}"
MAX_Y_AXIS = 60
MAX_Y_AXIS_ALL = 300
MAX_X_AXIS = 1200
component = "packages"

def get_developer_data(stage_developers):
    developers = []
    for id, developer in stage_developers.items():
        if developer[NUMBER_OF_COMMIT][-1] >= MINIMUM_COMMITS:
            developers.append(developer[NUMBER_OF_COMMIT][-1])
    return developers

def get_developer_commit_by_contributor_stage(contributor_stage):
    stage_developers = developer_component_knowledge[contributor_stage][component]
    return get_developer_data(stage_developers)

def generate_developer_commit_latex(contributor_stage):
    developers = get_developer_commit_by_contributor_stage(contributor_stage)
    title = "Number of commits"
    return developer_graph(FILE_NAME, developers, title, 0, title,
                           param_caption=GRAPH_CAPTION.format(contributor=contributor_stage, number=len(developers)), 
                           param_x_axis=title, 
                           max_x_axis=MAX_X_AXIS, 
                           max_y_axis=MAX_Y_AXIS), developers

def generate_all_developer_commit(transient_founder, transient_joiner, sustained_founder, sustained_joiner):
    all_developers = transient_founder + transient_joiner + sustained_founder + sustained_joiner
    title = "Number of commits"
    return developer_graph(FILE_NAME, all_developers, title, 0, title,
                           sub_graph=False,
                           param_caption=GRAPH_CAPTION.format(contributor="All", number=len(all_developers)), 
                           param_x_axis=title, 
                           max_x_axis=MAX_X_AXIS, 
                           max_y_axis=MAX_Y_AXIS_ALL)    


def generate_developer_commit():
    latex_graph = latex_start_graph()
    latex, transient_founder = generate_developer_commit_latex(TRANSIENT_FOUNDER)
    latex_graph += latex
    latex, transient_joiner = generate_developer_commit_latex(TRANSIENT_JOINER)
    latex_graph += latex
    latex, sustained_founder = generate_developer_commit_latex(SUSTAINED_FOUNDER)
    latex_graph += latex
    latex, sustained_joiner = generate_developer_commit_latex(SUSTAINED_JOINER)
    latex_graph += latex
    latex_graph += FIGURE_CAPTION
    latex_graph += latex_end_graph()
    latex = generate_all_developer_commit(transient_founder, transient_joiner, sustained_founder, sustained_joiner)
    return latex + latex_graph

def generate_and_save():
    path = DIRECTORY 
    latex = get_section_start(FILE_NAME, "sub") + " Developer Commits } \n" 
    latex += generate_developer_commit()
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
