from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.store_developer_data import * 

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
GRAPH_CAPTION = "By {freq} for {category} {number} developers."
MAX_X_AXIS = 4
MAX_Y_AXIS = 50

FIGURE_CAPTION = "Histogram of new {component} touched (x-axis) against number of developers (y-axis) from " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " " + str(len(DEVELOPER_CATEGORY)) + " categories of developers from {number_of_repositories} sampled from GitHub." 


def get_commit_and_daily(developers):
    commit_data = []
    daily_data = []
    for key, developer in developers.items():
        daily_data.append(round(developer[KNOWN_Y_AXIS][-1] / developer[YEAR_PERIOD][-1], 2))
        commit_data.append(round(developer[KNOWN_Y_AXIS][-1] / developer[NUMBER_OF_COMMIT][-1], 2))
    return commit_data, daily_data

def generate_summary_histogram(commit_data, daily_data, component, category):
    latex_repo = developer_graph(FILE_NAME, daily_data, component, 0, category + "Day", "", GRAPH_CAPTION.format(freq="Day", number=str(len(daily_data)), category=category), max_x_axis=max(max(daily_data),max(commit_data)) + 1, max_y_axis=MAX_Y_AXIS) 
    latex_repo += developer_graph(FILE_NAME, commit_data, component, 0, category + "Commit", "", GRAPH_CAPTION.format(freq="Commit", number=str(len(commit_data)), category=category), max_x_axis=max(max(daily_data),max(commit_data)) + 1, max_y_axis=MAX_Y_AXIS) 
    return latex_repo

def generate_component_summary_historgram(component, number_of_repositories):
    latex = ""
    all_developers = {}
    set_graph_number(2)
    for category in DEVELOPER_CATEGORY:
        developers = developer_component_knowledge[category][component]
        all_developers = all_developers | developers
        commit_data, daily_data = get_commit_and_daily(developers)
        latex += generate_summary_histogram(commit_data, daily_data, component, category)
    commit_data, daily_data = get_commit_and_daily(all_developers)
    latex_start = generate_summary_histogram(commit_data, daily_data, component, "All")
    latex = latex_start_graph() + latex_start + latex
    latex += "  \\caption{" + FIGURE_CAPTION.format(component=component, number_of_repositories=number_of_repositories) + "} \n"
    latex += latex_end_graph()
    return latex

def generate_and_save(number_of_repositories):
    latex = get_section_start(FILE_NAME, "sub") + "For components with total } \n"
    for component in COMPONENTS:
        latex += generate_component_summary_historgram(component, number_of_repositories)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, DIRECTORY)
    latex = "\\input{" + DIRECTORY + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
