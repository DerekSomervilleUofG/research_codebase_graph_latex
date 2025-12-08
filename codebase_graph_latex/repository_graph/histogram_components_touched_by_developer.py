from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.store_developer_data import * 
import math

FILE_NAME = __name__
BASE_FILE_NAME = REPOSITORY_SUMMARY_1_FILE
GRAPH_CAPTION = "{category} (n={number}). "
ALL_GRAPH_CAPTION = "By {freq}. "
MAX_Y_AXIS = {"all": 1300, TRANSIENT: 100, MODERATE: 80, SUSTAINED: 24}
MAX_X_AXIS = {"all": 25, TRANSIENT + "_packages": 5, MODERATE + "_packages": 1, SUSTAINED + "_packages": 1,
              TRANSIENT + "_classes": 50, MODERATE + "_classes": 15, SUSTAINED + "_classes": 15,
              TRANSIENT + "_methods": 100, MODERATE + "_methods": 40, SUSTAINED + "_methods": 40}

FIGURE_CAPTION = "Histogram of the number of developers (y-axis) against the average {component} touched by {freq} (x-axis) from " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " (" + str(len(DEVELOPER_CATEGORY)) + ") categories of developers from {number_of_repositories} repositories sampled from GitHub." 
ALL_FIGURE_CAPTION = "Histogram of the number of developers (y-axis) against the average {component} touched by day and commit (x-axis) from all {num} developers from {number_of_repositories} repositories sampled from GitHub." 


def get_commit_and_daily(developers):
    commit_data = []
    daily_data = []
    for key, developer in developers.items():
        daily_data.append(round(developer[KNOWN_Y_AXIS][-1] / developer[YEAR_PERIOD][-1], 2))
        commit_data.append(round(developer[KNOWN_Y_AXIS][-1] / developer[NUMBER_OF_COMMIT][-1], 2))
    return commit_data, daily_data

def generate_summary_histogram(commit_data, daily_data, component, category):
    latex_repo = developer_graph(FILE_NAME, daily_data, component, 0, 
                                     category + "Day",
                                     param_x_axis="Touched " + component,
                                     param_caption=ALL_GRAPH_CAPTION.format(freq="Day"), 
                                     max_x_axis=max(max(daily_data),max(commit_data)) + 1, 
                                     max_y_axis=MAX_Y_AXIS[category])
    latex_repo += developer_graph(FILE_NAME, commit_data, component, 0, category + "Commit", 
                                    param_x_axis="Touched " + component,
                                    param_caption=ALL_GRAPH_CAPTION.format(freq="Commit"), 
                                    max_x_axis=max(max(daily_data),max(commit_data)) + 1, 
                                    max_y_axis=MAX_Y_AXIS[category]) 
    return latex_repo

def generate_component_summary_historgram(component, number_of_repositories):
    latex_day = latex_start_graph()
    all_developers = {}
    for category in DEVELOPER_CATEGORY:
        developers = developer_component_knowledge[category][component]
        all_developers = all_developers | developers
        commit_data, daily_data = get_commit_and_daily(developers)
        weights = np.ones_like(daily_data) * (100.0 / len(daily_data))
        latex_day += developer_percentage_graph(FILE_NAME, daily_data, weights, component, 0, 
                                     category + "Day", "", 
                                     GRAPH_CAPTION.format(number=str(len(daily_data)), category=category.capitalize()), 
                                     max_x_axis=MAX_X_AXIS[category.split(" ")[0] + "_" + component])
    latex_commit = latex_start_graph() 
    for category in DEVELOPER_CATEGORY:
        developers = developer_component_knowledge[category][component]
        commit_data, daily_data = get_commit_and_daily(developers)
        weights = np.ones_like(commit_data) * (100.0 / len(commit_data))
        latex_commit += developer_percentage_graph(FILE_NAME, commit_data, weights, component, 0, 
                                       category + "Commit", "", 
                                       GRAPH_CAPTION.format(number=str(len(commit_data)), category=category.capitalize()), 
                                       max_x_axis=MAX_X_AXIS[category.split(" ")[0] + "_" + component])
    commit_data, daily_data = get_commit_and_daily(all_developers)
    latex_start = latex_start_graph()
    latex_start += generate_summary_histogram(commit_data, daily_data, component, "all")
    latex_start += "\\caption{" + ALL_FIGURE_CAPTION.format(component=component, num=len(daily_data), number_of_repositories=number_of_repositories) 
    latex_start += "} \n"
    latex_start += latex_end_graph()
    latex_day = latex_start + latex_day
    latex_day += "\\caption{" + FIGURE_CAPTION.format(component=component, number_of_repositories=number_of_repositories, freq="day") 
    latex_day += "} \n"
    latex_day += latex_end_graph()
    latex_commit += "\\caption{" + FIGURE_CAPTION.format(component=component, number_of_repositories=number_of_repositories, freq="commit") 
    latex_commit += "} \n"
    latex_commit += latex_end_graph()
    return latex_day + latex_commit

def generate_and_save(number_of_repositories):
    latex = get_section_start(FILE_NAME, "sub") + "For components with total } \n"
    for component in COMPONENTS:
        latex += generate_component_summary_historgram(component, number_of_repositories)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, DIRECTORY)
    latex = "\\input{" + DIRECTORY + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
