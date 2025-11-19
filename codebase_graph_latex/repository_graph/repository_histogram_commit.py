from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.store_developer_data import * 

FILE_NAME = __name__
BASE_FILE_NAME = "repository_1.tex"
GRAPH_CAPTION = "By {freq}."
MAX_X_AXIS = 4
MAX_Y_AXIS = 8

FIGURE_CAPTION = "Histogram of new {component} touched (x-axis) against number of developers (y-axis)." \
    " Graphs for {number} {group}" 

def get_commit_and_daily(developers):
    commit_data = []
    daily_data = []
    for key, developer in developers.items():
        daily_data.append(round(developer[KNOWN_Y_AXIS][-1] / developer[YEAR_PERIOD][-1], 2))
        commit_data.append(round(developer[KNOWN_Y_AXIS][-1] / developer[NUMBER_OF_COMMIT][-1], 2))
    return commit_data, daily_data

def generate_summary_histogram(commit_data, daily_data, repository_id, path, component):
    latex_repo = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For " + component + " with total } \n"
    latex_repo += "\n"
    read_write_file.create_directory(path)
    latex_repo += latex_start_graph()
    latex_repo += developer_graph(FILE_NAME, daily_data, component, repository_id, "Day", "", GRAPH_CAPTION.format(freq="Day"), max_x_axis=max(max(daily_data),max(commit_data)) + 1, max_y_axis=MAX_Y_AXIS) 
    latex_repo += developer_graph(FILE_NAME, commit_data, component, repository_id, "Commit", "", GRAPH_CAPTION.format(freq="Commit"), max_x_axis=max(max(daily_data),max(commit_data)) + 1, max_y_axis=MAX_Y_AXIS) 
    latex_repo += "  \\caption{" + FIGURE_CAPTION.format(component=component, group=SUSTAINED_JOINER_DESC.lower(), number=str(len(daily_data))) + "} \n"
    latex_repo += latex_end_graph()
    return latex_repo

def generate_and_save():
    path = DIRECTORY
    for component in COMPONENTS:
        latex += generate_summary_histogram(path, component)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
