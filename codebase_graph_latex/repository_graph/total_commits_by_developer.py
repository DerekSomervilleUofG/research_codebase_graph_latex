from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_developer_commit import *
from codebase_graph_latex.store_developer_data import * 
import math

FILE_NAME = __name__
BASE_FILE_NAME = REPOSITORY_SUMMARY_1_FILE
MINIMUM_COMMITS = 3
GRAPH_CAPTION = "{contributor} (n={number}). "
FIGURE_CAPTION = "Histogram of number of developers (y-axis) against total commits made (x-axis)" + " in " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " (" + str(len(DEVELOPER_CATEGORY)) + ") categories. This is from {number__of_repositories} repositories sampled from GitHub, excluding developers with less than " + word_engine.number_to_words(MINIMUM_COMMITS) + " (" + str(MINIMUM_COMMITS) +  ") commits."
ALL_FIGURE_CAPTION = "Histogram of the number from all developers (n={number}) (y-axis) against the total number of commits (x-axis) in {number__of_repositories} repositories sampled from GitHub, excluding developers with less than " + word_engine.number_to_words(MINIMUM_COMMITS) + " (" + str(MINIMUM_COMMITS) +  ") commits. "
MAX_Y_AXIS = 80
MAX_Y_AXIS_TRANSIENT = 200
MAX_Y_AXIS_ALL = 1600
MAX_X_AXIS = 1200
MAX_X_AXIS_TRANSIENT = 20
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

def generate_developer_commit_latex(contributor_stage, developers, bins, max_x_axis=MAX_X_AXIS, max_y_axis=MAX_Y_AXIS):
    title = "Number of commits"
    return developer_graph(FILE_NAME, developers, title, 0, contributor_stage,
                           param_caption=GRAPH_CAPTION.format(contributor=contributor_stage.capitalize(), number=len(developers)), 
                           param_x_axis=title, 
                           max_x_axis=max_x_axis, 
                           max_y_axis=max_y_axis,
                           bins=bins)

def generate_all_developer_commit(number_of_repositories, transient_founder, transient_joiner, moderate_founder, moderate_joiner, sustained_founder, sustained_joiner):
    all_developers = transient_founder + transient_joiner + sustained_founder + sustained_joiner + moderate_founder + moderate_joiner, 
    title = "Number of commits"
    return developer_graph(FILE_NAME, all_developers, title, 0, title,
                           sub_graph=False,
                           param_caption=ALL_FIGURE_CAPTION.format(number=len(all_developers[0]), number__of_repositories=number_of_repositories), 
                           param_x_axis=title, 
                           max_x_axis=MAX_X_AXIS, 
                           max_y_axis=MAX_Y_AXIS_ALL,
                           figure_size=WIDE_FIGURE)    


def generate_developer_commit(number_of_repositories):
    transient_founder = get_developer_commit_by_contributor_stage(TRANSIENT_FOUNDER)
    transient_joiner = get_developer_commit_by_contributor_stage(TRANSIENT_JOINER)
    moderate_founder = get_developer_commit_by_contributor_stage(MODERATE_FOUNDER)
    moderate_joiner = get_developer_commit_by_contributor_stage(MODERATE_JOINER)
    sustained_founder = get_developer_commit_by_contributor_stage(SUSTAINED_FOUNDER)
    sustained_joiner = get_developer_commit_by_contributor_stage(SUSTAINED_JOINER)

    latex_graph = generate_all_developer_commit(number_of_repositories, transient_founder, transient_joiner, moderate_founder, moderate_joiner, sustained_founder, sustained_joiner)
    latex_graph += latex_start_graph()
    latex_graph += generate_developer_commit_latex(TRANSIENT_FOUNDER, transient_founder, math.ceil(BINS * (max(transient_founder)/max(transient_joiner))), max_x_axis=MAX_X_AXIS_TRANSIENT, max_y_axis=MAX_Y_AXIS_TRANSIENT)
    latex_graph += generate_developer_commit_latex(TRANSIENT_JOINER, transient_joiner, BINS, max_x_axis=MAX_X_AXIS_TRANSIENT, max_y_axis=MAX_Y_AXIS_TRANSIENT)
    latex_graph += generate_developer_commit_latex(MODERATE_FOUNDER, moderate_founder, math.ceil(BINS * (max(moderate_founder)/max(moderate_joiner))))
    latex_graph += generate_developer_commit_latex(MODERATE_JOINER, moderate_joiner, BINS)
    latex_graph += generate_developer_commit_latex(SUSTAINED_FOUNDER, sustained_founder, math.ceil(BINS * (max(sustained_founder)/max(sustained_joiner))))
    latex_graph += generate_developer_commit_latex(SUSTAINED_JOINER, sustained_joiner, BINS)
    latex_graph += "\\caption{" + FIGURE_CAPTION.format(number__of_repositories=number_of_repositories) + "} \n"
    latex_graph += latex_end_graph()
    return latex_graph

def generate_and_save(number_of_repositories):
    path = DIRECTORY 
    latex = get_section_start(FILE_NAME, "sub") + " Developer Commits } \n" 
    latex += generate_developer_commit(number_of_repositories)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
