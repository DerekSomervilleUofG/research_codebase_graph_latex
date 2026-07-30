from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.store_developer_data import * 

import statistics
import numpy

FILE_NAME = __name__
BASE_FILE_NAME = REPOSITORY_SUMMARY_1_FILE
GRAPH_CAPTION = "{category} (n={number}, $\mu$={mean}, med={median}, mod={mode},  $\\max_y$={max_pct}, $\\max_x$={max_touched}) "
ALL_GRAPH_CAPTION = "By {freq} (max={max_pct})."
MAX_Y_AXIS = {"all": 85, TRANSIENT: 100, MODERATE: 80, SUSTAINED: 75, 
              "packages_" + TRANSIENT: 90, "packages_" + SUSTAINED: 60, "packages_" + MODERATE: 75, "commit_packages_" + MODERATE: 35, 
              "classes_" + SUSTAINED: 40, "classes_" + MODERATE: 75, "commit_classes_" + MODERATE: 15, "commit_classes_" + SUSTAINED: 25, 
              "methods_" + MODERATE: 80, "methods_" + SUSTAINED: 50, "commit_methods_" + MODERATE: 20, "commit_methods_" + SUSTAINED: 25}
MAX_X_AXIS = {"all": 25, "packages" + TRANSIENT: 5, "commit_packages_" + MODERATE: 5, "packages_" + MODERATE: 1, "packages_" + SUSTAINED: 1,
              "classes_" + TRANSIENT: 35, "classes_" + MODERATE: 15, "classes_" + SUSTAINED: 15,
              "methods_" + TRANSIENT: 50, "methods_" + MODERATE: 40, "methods_" + SUSTAINED: 40}
BINS = {"packages_" + TRANSIENT: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], "commit_packages_" + MODERATE: [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5], "packages_" + MODERATE: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], "packages_" + SUSTAINED: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
              "classes_" + TRANSIENT: [0, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50], "classes_" + MODERATE: [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16], "classes_" + SUSTAINED: [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16],
              "methods_" + TRANSIENT: [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], "methods_" + MODERATE: [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40], "methods_" + SUSTAINED: [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40]}
FIGURE_CAPTION = "Histogram of percentage of  developers (y-axis) against the average {component} touched by {freq} (x-axis) from " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " (" + str(len(DEVELOPER_CATEGORY)) + ") categories of developers from {number_of_repositories} repositories sampled from GitHub." 
ALL_FIGURE_CAPTION = "Histogram of percentage of all developers (y-axis) against the average {component} touched by day and commit (x-axis) from all {num} developers from {number_of_repositories} repositories sampled from GitHub." 

def get_bins(frequency, category, component):
    bin = BINS.get(frequency + "_" + component + "_" + category.split(" ")[0], 0)
    if bin == 0:
        bin = BINS.get(component + "_" + category.split(" ")[0], 0)
        if bin == 0:
            bin = BINS.get(category.split(" ")[0], 0)
    return bin

def get_max_y_axis(frequency, category, component):
    y_axis_max = MAX_Y_AXIS.get(frequency + "_" + component + "_" + category.split(" ")[0], 0)
    if y_axis_max == 0:
        y_axis_max = MAX_Y_AXIS.get(component + "_" + category.split(" ")[0], 0)
        if y_axis_max == 0:
            y_axis_max = MAX_Y_AXIS.get(category.split(" ")[0], 0)
    return y_axis_max

def get_max_x_axis(frequency, category, component):
    x_axis_max = MAX_X_AXIS.get(frequency + "_" + component + "_" + category.split(" ")[0], 0)
    if x_axis_max == 0:
        x_axis_max = MAX_X_AXIS.get(component + "_" + category.split(" ")[0], 0)
        if x_axis_max == 0:
            x_axis_max = MAX_X_AXIS.get(category.split(" ")[0], 0)
    return x_axis_max

def get_commit_and_daily(developers, frequency):
    data = []
    for key, developer in developers.items():
        if frequency == "daily":
            data_row = round(developer[KNOWN_Y_AXIS][-1] / developer[YEAR_PERIOD][-1], 1)
        else:
            data_row = round(developer[KNOWN_Y_AXIS][-1] / developer[NUMBER_OF_COMMIT][-1], 1)
        if data_row == 0:
            data_row = 0.01
        
        data.append(data_row)

    return data

def generate_component_summary_historgram_by_component(component, number_of_repositories, frequency):
    latex = latex_start_graph()
    all_developers = {}
    for category in DEVELOPER_CATEGORY:
        developers = developer_component_knowledge[category][component]
        all_developers = all_developers | developers
        data = get_commit_and_daily(developers, frequency)
        weights = np.ones_like(data) * (100.0 / len(data))
        counts, _ = numpy.histogram(data, bins=get_bins(frequency, category, component), weights=weights)
        max_pct_val = round(max(counts), 1) if len(counts) > 0 else 0.0
        max_touched = max(data)
        if len(data) > 0:
            # Rounding to 2 decimal places keeps the caption from becoming too wide
            mean_val = round(numpy.mean(data), 2)
            median_val = round(numpy.median(data), 2)
            try:
                # statistics.mode will throw a ModeError if data is empty or completely uniform
                mode_val = round(statistics.mode(data), 2)
            except statistics.StatisticsError:
                # Fallback to mean/median approximation or an empty placeholder if no clear mode
                mode_val = "-" 
            max_touched = round(max(data), 2)
        else:
            mean_val, median_val, mode_val = 0.0, 0.0, 0.0
        latex += developer_percentage_graph(FILE_NAME, data, weights, component, 0, 
                                     category + frequency, "", 
                                     GRAPH_CAPTION.format(number=str(len(data)), mean=mean_val, median=median_val, mode=mode_val, category=category.capitalize(), max_pct=max_pct_val, max_touched=max_touched), 
                                     max_x_axis=get_max_x_axis(frequency, category, component), 
                                    max_y_axis=get_max_y_axis(frequency, category, component),
                                    bins=get_bins(frequency, category, component),
                                    log_x=False)
    latex += "\\caption[Hstogram of " + component + " Touched By Developer for " + frequency + "]{" + FIGURE_CAPTION.format(component=component, number_of_repositories=number_of_repositories, freq=frequency) 
    latex += "} \n"
    latex += latex_end_graph(FILE_NAME + "_" + component + "_" + frequency)

    return latex

def generate_component_summary_historgram(file_name, number_of_repositories, frequency):
    latex = get_section_start(FILE_NAME, "sub") + "For components touched " + frequency
    latex += "} \n"
    latex += "\\label{subsec:" + FILE_NAME.replace(" ", "_") + frequency + "} \n"
    for component in COMPONENTS:
        latex += generate_component_summary_historgram_by_component(component, number_of_repositories, frequency)
    save_to_latex_file(file_name + "_" + frequency, file_name + ".tex", latex, DIRECTORY)

def generate_and_save(number_of_repositories):
    file_name = get_base_file_name(FILE_NAME)
    latex = get_section_start(FILE_NAME, "") + "For components with total } \n"
    latex += "\\label{sec:" + FILE_NAME.replace(" ", "_") + "} \n"
    save_to_latex_file(file_name, BASE_FILE_NAME, latex, DIRECTORY)
    generate_component_summary_historgram(file_name, number_of_repositories, "commit")
    generate_component_summary_historgram(file_name, number_of_repositories, "daily")
 