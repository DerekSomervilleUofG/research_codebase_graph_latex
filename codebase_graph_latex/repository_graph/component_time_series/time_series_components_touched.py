from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.developer_data import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import math

FILE_NAME = __name__
GRAPH_CAPTION = "{type} developers ({num}) showing {component} touched"
FIGURE_CAPTION = "A time series of the number of {unit} (x-axis) against the average (mean) total {component} touched (y-axis) for six categories of developer, " 
ALL_FIGURE_CAPTION = "A time series of the number of {unit} (x-axis) against the average (mean) total {component} touched (y-axis) for all developers {num}, "
FIGURE_SUFFIX = "with \\color{Orange} positive (orange) \\color{Black} and \\color{Red} negative (red) \\color{Black} filled standard deviation. "
BASE_FILE_NAME = "repository_1.tex"




def section_heading(repository_id):
    latex = "\\section{ Repository - "+ str(repository_id) + "} \n"
    return latex

def section_sub_heading(repository_id, component):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For " + component + " touched for each period} \n"
    latex += "A time series of " + component + " touched on average each month. \n"
    return latex

def instansiate_data():
    data = {}
    data[MONTH] = []
    data[TOUCHED] = []
    return data

def add_extra(list, number_extra, value=0):
    for counter in range(0, number_extra):
        list.append(value)

def populate_data(developers, max_days, UNIT=NUMBER_OF_MONTHS):
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
    for id, values in developers.items():        
        data.append(values[find_developer_unit(unit) + 1].copy())
    return data

def max_days(developers):
    return len(max(developers.values(), key=lambda dev: len(dev[YEAR_PERIOD]))[YEAR_PERIOD])

def get_x_axis_unit(unit):
    if unit == NUMBER_OF_MONTHS:
        months = np.arange(1, unit + 1)
    else:
        months = np.arange(1, unit + 1, 9)
    return months

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


def generate_graph(path, component, data, type, unit=NUMBER_OF_MONTHS):
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    data_frame = np.array(data)
    months = np.arange(1, unit + 1)
    mean_touched = np.nanmean(data_frame, axis=0)
    plt.plot(months, mean_touched, label="Mean " + component + " Touched", color="blue")
    std_above, std_below = calculate_std(mean_touched, data, unit)
    plt.fill_between(months, mean_touched, mean_touched + std_above,
                 color='green', alpha=0.3, label='Above (+1 Std Dev)')

    plt.fill_between(months, mean_touched - std_below, mean_touched,
                 color='red', alpha=0.3, label='Below (-1 Std Dev)')
    plt.xticks(get_x_axis_unit(unit), fontsize=7)
    plt.xlabel(UNIT_FREQUENCY[unit] + "s")
    plt.ylabel(component.capitalize() + " touched")
    plt.tight_layout() 
    file_name = path + get_base_file_name(FILE_NAME) + "." + type.lower().replace(" ",".") + "." + UNIT_FREQUENCY[unit].lower() + ".pdf"
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    return file_name

def get_data_and_generate_graph(method, path, component, developers, stage, unit=NUMBER_OF_MONTHS):
    file_name = method(path + component + "/", component, 
                                  populate_touched_data(developers, 
                                                unit), 
                                                stage,
                                                unit)
    return latex_add_sub_graph(file_name, GRAPH_CAPTION.format(num=str(len(developers.keys())), type=stage.capitalize(), component=component))
    
def generate_latex(method, path, component, unit, developers, figure_caption):
    
    all_data = developers[TRANSIENT_FOUNDER] | developers[SUSTAINED_FOUNDER] | developers[TRANSIENT_JOINER] | developers[SUSTAINED_JOINER]
    file_name = method(path + component + "/", component, 
                                  populate_touched_data(all_data, 
                                                unit), 
                                                "All",
                                                unit)
    latex = latex_add_graph(file_name, ALL_FIGURE_CAPTION.format(num=str(len(all_data.keys())), component=component, unit=UNIT_FREQUENCY[unit].lower() + "s"))
    latex += latex_start_graph()
    stage_developers = developers[TRANSIENT_FOUNDER]
    if len(stage_developers.keys()) > 0:
        latex += get_data_and_generate_graph(method, path, component, stage_developers, TRANSIENT_FOUNDER, unit)
    stage_developers = developers[TRANSIENT_JOINER]
    if len(stage_developers.keys()) > 0:
        latex += get_data_and_generate_graph(method, path, component, stage_developers, TRANSIENT_JOINER, unit)
    stage_developers = developers[MODERATE_FOUNDER]
    if len(stage_developers.keys()) > 0:
        latex += get_data_and_generate_graph(method, path, component, stage_developers, MODERATE_FOUNDER, unit)
    stage_developers = developers[MODERATE_JOINER]
    if len(stage_developers.keys()) > 0:
        latex += get_data_and_generate_graph(method, path, component, stage_developers, MODERATE_JOINER, unit)
    stage_developers = developers[SUSTAINED_FOUNDER]
    if len(stage_developers.keys()) > 0:
        latex += get_data_and_generate_graph(method, path, component, stage_developers, SUSTAINED_FOUNDER, unit)
    stage_developers = developers[SUSTAINED_JOINER]
    if len(stage_developers.keys()) > 0:
        latex += get_data_and_generate_graph(method, path, component, stage_developers, SUSTAINED_JOINER, unit)
    latex += "\\caption{" + figure_caption.format(component=component, unit=UNIT_FREQUENCY[unit].lower()) + "} \n"
    latex += latex_end_graph()        
    return latex

def default_generate_save(method, base_file_name, file_name, repository_id, component, developers, units=[NUMBER_OF_MONTHS, NUMBER_OF_WEEKS], figure_caption=FIGURE_CAPTION):
    path = "repository/" + str(repository_id) + "/" 
    latex = ""
    if component == "packages":
        base_latex =  "\\input{" + path + get_base_file_name(file_name)  + "}\n"
        read_write_file.append_to_file(base_file_name, 
                                   base_latex, 
                                    DIRECTORY)
    for unit in units:
        latex += generate_latex(method, path, component, unit, developers, figure_caption)
    read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", latex, path)

def generate_and_save(repository_id, component, developers):
    if component == "packages":
        path = "repository/" + str(repository_id) + "/" 
        read_write_file.write_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component), path)
    default_generate_save(generate_graph, BASE_FILE_NAME, FILE_NAME, repository_id, component, developers, figure_caption=FIGURE_CAPTION)
    