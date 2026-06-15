from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.store_developer_data import * 
import statistics
import numpy

FILE_NAME = __name__
BASE_FILE_NAME = REPOSITORY_SUMMARY_1_FILE
GRAPH_CAPTION = "{category} (n={number}, max={max_pct}). "
ALL_GRAPH_CAPTION = "By {freq} (max={max_pct})."
MAX_Y_AXIS = {"all": 85, TRANSIENT: 100, MODERATE: 80, SUSTAINED: 75, "packages_" + TRANSIENT: 90, "packages_" + SUSTAINED: 60, "packages_" + MODERATE: 75, "classes_" + SUSTAINED: 90, "classes_" + MODERATE: 100, "methods_" + MODERATE: 100, "methods_" + SUSTAINED: 75}
MAX_X_AXIS = {"all": 25, TRANSIENT + "_packages": 5, MODERATE + "_packages": 1, SUSTAINED + "_packages": 1,
              TRANSIENT + "_classes": 50, MODERATE + "_classes": 15, SUSTAINED + "_classes": 15,
              TRANSIENT + "_methods": 100, MODERATE + "_methods": 40, SUSTAINED + "_methods": 40}
BINS = {TRANSIENT + "_packages": [0, 1, 2, 3, 4, 5], MODERATE + "_packages": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], SUSTAINED + "_packages": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
              TRANSIENT + "_classes": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50], MODERATE + "_classes": [0, 2, 4, 6, 8, 10, 12, 14, 16], SUSTAINED + "_classes": [0, 2, 4, 6, 8, 10, 12, 14, 16],
              TRANSIENT + "_methods": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], MODERATE + "_methods": [0, 5, 10, 15, 20, 25, 30, 35, 40], SUSTAINED + "_methods": [0, 5, 10, 15, 20, 25, 30, 35, 40]}
FIGURE_CAPTION = "Histogram of percentage of  developers (y-axis) against the average {component} touched by {freq} (x-axis) from " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " (" + str(len(DEVELOPER_CATEGORY)) + ") categories of developers from {number_of_repositories} repositories sampled from GitHub." 
ALL_FIGURE_CAPTION = "Histogram of percentage of all developers (y-axis) against the average {component} touched by day and commit (x-axis) from all {num} developers from {number_of_repositories} repositories sampled from GitHub." 

def get_max_y_axis(category, component):
    y_axis_max = MAX_Y_AXIS.get(component + "_" +category.split(" ")[0], 0)
    if y_axis_max == 0:
        y_axis_max = y_axis_max = MAX_Y_AXIS.get(category.split(" ")[0], 0)
    return y_axis_max

def get_commit_and_daily(developers):
    commit_data = []
    daily_data = []
    for key, developer in developers.items():
        daily = round(developer[KNOWN_Y_AXIS][-1] / developer[YEAR_PERIOD][-1], 2)
        if daily == 0:
            daily = 0.01
        commit = round(developer[KNOWN_Y_AXIS][-1] / developer[NUMBER_OF_COMMIT][-1], 2)
        if commit == 0:
            commit = 0.01
        daily_data.append(daily)
        commit_data.append(commit)
    return commit_data, daily_data

def generate_summary_histogram(commit_data, daily_data, component, category):
    weights = np.ones_like(daily_data) * (100.0 / len(daily_data))
    daily_data = numpy.round(numpy.log10(daily_data), 3)
    counts_daily, _ = numpy.histogram(daily_data, weights=weights)
    max_daily_pct = round(max(counts_daily), 1) if len(counts_daily) > 0 else 0.0
    commit_data = numpy.round(numpy.log10(commit_data), 3)
    latex_repo = developer_percentage_graph(FILE_NAME, daily_data, weights, component, 0,
                                     category + "Day",
                                     param_x_axis=component.capitalize() + " touched (log)",
                                     param_caption=ALL_GRAPH_CAPTION.format(freq="Day", max_pct=max_daily_pct), 
                                     max_x_axis=max(max(daily_data),max(commit_data)), 
                                     max_y_axis=MAX_Y_AXIS[category])
    weights = np.ones_like(commit_data) * (100.0 / len(commit_data))
    counts_commit, _ = numpy.histogram(commit_data, weights=weights)
    max_commit_pct = round(max(counts_commit), 1) if len(counts_commit) > 0 else 0.0
    latex_repo += developer_percentage_graph(FILE_NAME, commit_data, weights, component, 0, category + "Commit", 
                                    param_x_axis=component.capitalize() + " touched (log)",
                                    param_caption=ALL_GRAPH_CAPTION.format(freq="Commit", max_pct=max_commit_pct), 
                                    max_x_axis=max(max(daily_data),max(commit_data)), 
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
        bin = BINS[category.split(" ")[0] + "_" + component]
        counts, _ = numpy.histogram(daily_data, bins=bin, weights=weights)
        max_pct_val = round(max(counts), 1) if len(counts) > 0 else 0.0
        latex_day += developer_percentage_graph(FILE_NAME, daily_data, weights, component, 0, 
                                     category + "Day", "", 
                                     GRAPH_CAPTION.format(number=str(len(daily_data)), category=category.capitalize(), max_pct=max_pct_val), 
                                     max_x_axis=MAX_X_AXIS[category.split(" ")[0] + "_" + component], 
                                    max_y_axis=get_max_y_axis(category, component),
                                    bins=bin)
    latex_commit = latex_start_graph() 
    for category in DEVELOPER_CATEGORY:
        developers = developer_component_knowledge[category][component]
        commit_data, daily_data = get_commit_and_daily(developers)
        weights = np.ones_like(commit_data) * (100.0 / len(commit_data))
        bin = BINS[category.split(" ")[0] + "_" + component]
        counts, _ = numpy.histogram(commit_data, bins=bin, weights=weights)
        max_pct_val = round(max(counts), 1) if len(counts) > 0 else 0.0
        latex_commit += developer_percentage_graph(FILE_NAME, commit_data, weights, component, 0, 
                                       category + "Commit", "", 
                                       GRAPH_CAPTION.format(number=str(len(commit_data)), category=category.capitalize(), max_pct=max_pct_val), 
                                       max_x_axis=MAX_X_AXIS[category.split(" ")[0] + "_" + component], 
                                        max_y_axis=get_max_y_axis(category, component),
                                    bins=bin)
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
    latex = get_section_start(FILE_NAME, "") + "For components with total } \n"
    for component in COMPONENTS:
        latex += generate_component_summary_historgram(component, number_of_repositories)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, DIRECTORY)
    latex = "\\input{" + DIRECTORY + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
