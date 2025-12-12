from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.calculate import *
from codebase_graph_latex.developer_data import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import math

FILE_NAME = __name__
GRAPH_CAPTION = "{type} developers (n={num})"
FIGURE_CAPTION_START = "Repository {repo} "
FIGURE_CAPTION = "A time series of the average (mean) total {component} touched (y-axis) against the number of {unit} (x-axis) for " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " (" + str(len(DEVELOPER_CATEGORY)) + ") categories of developer. " 
ALL_FIGURE_CAPTION = "A time series of the average (mean) total {component} touched (y-axis) against the number of {unit} (x-axis)  for all developers (n={num}). "
FIGURE_SUFFIX = "with \\color{Orange} positive (orange) \\color{Black} and \\color{Red} negative (red) \\color{Black} filled standard deviation. "

def section_sub_heading(repository_id, component, time_series):
    latex = get_section_start(FILE_NAME, "sub") 
    if repository_id > 0:
        latex += str(repository_id) + " "
    latex += "For " + component + " touched for " + time_series + "} \n"
    latex += "A time series of " + component + " touched on average. \n"
    return latex

def instansiate_data():
    data = {}
    data[MONTH] = []
    data[TOUCHED] = []
    return data

def populate_data_period(developers, max_days, UNIT=NUMBER_OF_MONTHS):
    previous_touched = 0
    data = instansiate_data()
    for id, values in developers.items():
        
        days = values[YEAR_PERIOD].copy()
        touched = values[KNOWN_Y_AXIS].copy()
        
        add_extra(days, max_days - len(days))
        add_extra(touched, max_days - len(touched))
        
        for i in range(max_days):
            data[MONTH].append(math.ceil((days[i]/ 365) * UNIT))
            if float(touched[i]) == 0:
                current_touched = previous_touched
            else:
                current_touched = float(touched[i])
            data[TOUCHED].append(current_touched - previous_touched)
            previous_touched = current_touched
    return data

def populate_total_data(developers, unit=NUMBER_OF_MONTHS):
    previous_touched = 0
    data = instansiate_data()
    for id, values in developers.items():
        
        period = values[find_developer_unit(unit)].copy()
        touched = values[find_developer_unit(unit) + 1].copy()
        
        for i in range(unit):
            data[MONTH].append(period[i])
            if float(touched[i]) == 0 or float(touched[i]) < previous_touched:
                current_touched = previous_touched
            else:
                current_touched = float(touched[i])
            data[TOUCHED].append(current_touched)
            previous_touched = current_touched
    return data

def populate_touched_data(developers, unit=NUMBER_OF_MONTHS):
    data = []
    data_to_append = []
    for id, values in developers.items():
        data_to_append = values[find_developer_unit(unit) + 1].copy()
        if len(data_to_append) < unit:
            if len(data_to_append) >= 1:
                last_item = data_to_append[-1]
            else:
                last_item = 0
            add_extra(data_to_append, unit - len(data_to_append), last_item)
        data.append(data_to_append[:unit])
    return data

def max_days(developers):
    return len(max(developers.values(), key=lambda dev: len(dev[YEAR_PERIOD]))[YEAR_PERIOD])

def get_x_axis_unit(unit):
    if unit == NUMBER_OF_MONTHS:
        x_axis = np.arange(1, unit + 1)
    elif unit == NUMBER_OF_WEEKS:
        x_axis = np.arange(0, unit + 1, 5)
    elif unit == TIME_SERIES_NUMBER_OF_COMMIT:
        x_axis = np.arange(0, unit + 1, 100)
    return x_axis

def calculate_standard_deviation(data, period, mean_touched, above=True):
    for i in range(period):
        for j in range(len(data)):
            if data[j][i] < mean_touched[i] and above or data[j][i] > mean_touched[i] and not above:
                data[j][i] = mean_touched[i]
    return np.nanstd(data, axis=0)

def calculate_std(mean_touched, data, unit):
    std_above = []
    std_below = []
    above = []
    below =[]
    for i in range(unit):
        above = []
        below =[]
        for developer in data:
            if developer[i] > mean_touched[i]:
                above.append(developer[i])
            if developer[i] < mean_touched[i]:
                below.append(developer[i])
        std_above.append(np.nanstd(above))
        std_below.append(np.nanstd(below))
    
    std_above = np.array(std_above)
    std_below = np.array(std_below)
    return std_above, std_below


def generate_graph(path, component, data, type, unit, y_axis_max, figure_size=SMALL_FIGURE):
    plt.figure(figsize=figure_size, dpi=1000)
    read_write_file.create_directory(path)
    data_frame = np.array(data)
    months = np.arange(1, unit + 1)
    if len(data) > 0:
        mean_touched = np.nanmean(data_frame, axis=0)
        plt.plot(months, mean_touched, label="Mean " + component + " Touched", color="blue")
        std_above, std_below = calculate_std(mean_touched, data, unit)
        plt.fill_between(months, mean_touched, mean_touched + std_above,
                    color='green', alpha=0.3, label='Above (+1 Std Dev)')

        plt.fill_between(months, mean_touched - std_below, mean_touched,
                    color='red', alpha=0.3, label='Below (-1 Std Dev)')
    plt.xticks(get_x_axis_unit(unit), fontsize=7)
    if y_axis_max > 0:
        step = y_axis_max//10
        if step < 1:
            step = 1
        plt.yticks(np.arange(0, y_axis_max + 1, step))
        plt.ylim(0, y_axis_max)
        
    plt.xlabel(UNIT_FREQUENCY[unit] + "s")
    plt.ylabel(component.capitalize() + " touched")
    plt.tight_layout() 
    file_name = path + get_base_file_name(FILE_NAME) + "." + component + "." + type.lower().replace(" ",".") + "." + UNIT_FREQUENCY[unit].lower() + ".pdf"
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    return file_name

def get_data_and_generate_graph(method, path, component, developers, stage, unit, y_axis_max):
    file_name = method(path + component + "/", component, 
                                  populate_touched_data(developers, 
                                                unit), 
                                                stage,
                                                unit,
                                                y_axis_max)
    return latex_add_sub_graph(file_name, GRAPH_CAPTION.format(num=str(len(developers.keys())), type=stage.capitalize()))


def round_to_x_minus_1_digits_nearest_5(num):
    if num is None or (isinstance(num, float) and (math.isnan(num) or math.isinf(num))):
        return 1
    else:
        x = len(str(abs(int(num)))) if num != 0 else 1  # ensure x≥1 even for 0
        step = 5 * 10**(x - 2)
    return math.ceil(num / step) * step

def get_y_axis_for_a_category(developers, category, unit):
    founder_y_axis_max = get_y_axis_max(developers[category + " " + FOUNDER], unit )
    joiner_y_axis_max = get_y_axis_max(developers[category + " later " + JOINER], unit )
    return max(founder_y_axis_max, joiner_y_axis_max, 1)

def get_y_axis_max_for_categories(developers, unit):
    max_y_axis = {}
    max_y_axis[TRANSIENT] = get_y_axis_for_a_category(developers, TRANSIENT, unit)
    max_y_axis[MODERATE] = get_y_axis_for_a_category(developers, MODERATE, unit )
    max_y_axis[SUSTAINED] = get_y_axis_for_a_category(developers, SUSTAINED, unit )
    return max_y_axis

def get_y_axis_max(developers, unit):
    data = populate_touched_data(developers, unit)
    data_frame = np.array(data)
    mean_touched = np.nanmean(data_frame, axis=0)
    std_above, std_below = calculate_std(mean_touched, data, unit)
    if len(data) > 1:
        max_value = max(mean_touched + std_above)
        return round_to_x_minus_1_digits_nearest_5(max_value)
    else:
        return 1

def generate_latex(repository_id, method, path, component, unit, developers, figure_caption_all, figure_caption):
    
    all_data = developers[TRANSIENT_FOUNDER] | developers[SUSTAINED_FOUNDER] | developers[TRANSIENT_JOINER] | developers[SUSTAINED_JOINER] | developers[MODERATE_FOUNDER] | developers[MODERATE_JOINER]
    y_axis_max = get_y_axis_max(all_data, unit)
    file_name = method(path + component + "/", component, 
                                  populate_touched_data(all_data, 
                                                unit), 
                                                "All",
                                                unit,
                                                y_axis_max,
                                                figure_size=WIDE_FIGURE)
    latex = latex_add_graph(file_name, figure_caption_all.format(repo=repository_id, num=str(len(all_data.keys())), component=component, unit=UNIT_FREQUENCY[unit].lower() + "s"))
    latex += latex_start_graph()
    max_y_axis = get_y_axis_max_for_categories(developers, unit)
    for category in DEVELOPER_CATEGORY:
        stage_developers = developers[category]
        latex += get_data_and_generate_graph(method, path, component, stage_developers, category, unit, max_y_axis[category.split(" ")[0]])
    latex += "\\caption{" + figure_caption.format(component=component, unit=UNIT_FREQUENCY[unit].lower()) + "} \n"
    latex += latex_end_graph()        
    return latex

def default_generate_save(method, base_file_name, file_name, repository_id, component, developers, units=[NUMBER_OF_MONTHS, NUMBER_OF_WEEKS], figure_caption_all=ALL_FIGURE_CAPTION, figure_caption=FIGURE_CAPTION):
    path = "repository/"
    if repository_id > 0:
            path+= str(repository_id) + "/"
            figure_caption_all = FIGURE_CAPTION_START.format(repo=repository_id) + figure_caption_all
            figure_caption = FIGURE_CAPTION_START.format(repo=repository_id) + figure_caption
    read_write_file.create_directory(path)
    latex = ""
    if component == "packages":
        base_latex =  "\\input{" + path + get_base_file_name(file_name)  + "}\n"
        read_write_file.append_to_file(base_file_name, 
                                   base_latex, 
                                    DIRECTORY)
    for unit in units:
        latex += generate_latex(repository_id, method, path, component, unit, developers, figure_caption_all, figure_caption)
    read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", latex, path)

def generate_and_save(repository_id, component, developers, base_file_name):
    path = "repository/" 
    if repository_id > 0:
        path+= str(repository_id) + "/" 
    if component == "packages":
        read_write_file.write_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component, "each period"), path)
    else:
        read_write_file.append_to_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component, "each period"), path)
    default_generate_save(generate_graph, base_file_name, FILE_NAME, repository_id, component, developers, figure_caption=FIGURE_CAPTION, figure_caption_all=ALL_FIGURE_CAPTION, units=[NUMBER_OF_WEEKS])
    read_write_file.append_to_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component, "commit"), path)
    default_generate_save(generate_graph, base_file_name, FILE_NAME, repository_id, component, developers, figure_caption=FIGURE_CAPTION, figure_caption_all=ALL_FIGURE_CAPTION, units=[TIME_SERIES_NUMBER_OF_COMMIT])
