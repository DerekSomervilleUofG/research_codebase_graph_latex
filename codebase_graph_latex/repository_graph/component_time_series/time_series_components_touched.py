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
BASE_FILE_NAME = "repository_summary_1.tex"
GRAPH_CAPTION = "{type} developers (n={num} \& $\mu$={mean})"
FIGURE_CAPTION_START = "Repository {repo} "
FIGURE_CAPTION = "A time series of the average (mean) total {component} touched (y-axis) against the number of {unit} (x-axis) for " + word_engine.number_to_words(len(DEVELOPER_CATEGORY)) + " (" + str(len(DEVELOPER_CATEGORY)) + ") categories of developer. " 
ALL_FIGURE_CAPTION = "A time series of the average (mean) total {component} touched (y-axis) against the number of {unit} (x-axis)  for {all} developers (n={num}). "
FIGURE_SUFFIX = "with \\color{Orange} positive (orange) \\color{Black} and \\color{Red} negative (red) \\color{Black} filled standard deviation. "

def section_sub_heading(repository_id, touched_by):
    latex = get_section_start(FILE_NAME, "sub") 
    if repository_id > 0:
        latex += str(repository_id) + " "
    latex += "For all components touched for " + touched_by + " } \n"
    return latex

def section_sub_sub_heading(repository_id, component, time_series):
    latex = get_section_start(FILE_NAME, "subsub") 
    if repository_id > 0:
        latex += str(repository_id) + " "
    latex += "For " + component + " touched for " + time_series + "} \n"
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

def max_days(developers):
    return len(max(developers.values(), key=lambda dev: len(dev[YEAR_PERIOD]))[YEAR_PERIOD])

def get_step(x_axis_size):
    if x_axis_size >= 500:
        step = 100
    elif x_axis_size > 250:
        step = 50
    elif x_axis_size > 100:
        step = 10
    elif x_axis_size > 30:
        step = 5
    elif x_axis_size >= 20:
        step = 2

    else:
        step = 1
    return step
    
    
def get_x_axis_unit(unit, x_axis_size):
    if unit == NUMBER_OF_MONTHS:
        x_axis = np.arange(1, unit + 1)
    elif unit == NUMBER_OF_WEEKS:
        x_axis = np.arange(0, unit + 1, 5)
    elif unit == TIME_SERIES_NUMBER_OF_COMMIT:
        x_axis = np.arange(0, unit + 1, 100)
    else:
        x_axis = np.arange(0, x_axis_size + 1, get_step(x_axis_size))
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
    plt.close('all')
    x_axis_size = unit
    fig, ax = plt.subplots(figsize=figure_size, dpi=300)
    read_write_file.create_directory(path)
    data_frame = np.array(data)
    months = np.arange(1, unit + 1)
    mean = 0
    if len(data) > 0:
        mean_touched = np.nanmean(data_frame, axis=0)
        mean = round(mean_touched[-1],2)
        x_axis_size = len(mean_touched)
        ax.plot(months, mean_touched, label="Mean " + component + " Touched", color="blue")
        std_above, std_below = calculate_std(mean_touched, data, unit)
        ax.fill_between(months, mean_touched, mean_touched + std_above,
                    color='green', alpha=0.3, label='Above (+1 Std Dev)')

        ax.fill_between(months, mean_touched - std_below, mean_touched,
                    color='red', alpha=0.3, label='Below (-1 Std Dev)')
    ax.set_xticks(get_x_axis_unit(unit, x_axis_size))
    if y_axis_max > 0:
        step = y_axis_max//10
        if step < 1:
            step = 1
        ax.set_yticks(np.arange(0, y_axis_max + 1, step))
        ax.set_ylim(0, y_axis_max)
        
    ax.set_xlabel(UNIT_FREQUENCY.get(unit, "Commits"))
    ax.set_ylabel(component.capitalize() + " touched")
    fig.tight_layout() 
    file_name = path + get_base_file_name(FILE_NAME) + "." + component + "." + type.lower().replace(" ",".") + "." + UNIT_FREQUENCY.get(unit, "Commits").lower() + "_" + str(x_axis_size) + ".pdf"
    fig.savefig(file_name, bbox_inches='tight')
    plt.close()
    return file_name, GRAPH_CAPTION.format(num=str(len(data_frame)), type=type.capitalize(), mean=mean)

def get_data_and_generate_graph(method, path, component, developers, stage, unit, y_axis_max):
    file_name, graph_caption = method(path + component + "/", component, 
                                  populate_touched_data(developers, 
                                                unit), 
                                                stage,
                                                unit,
                                                y_axis_max)
    return latex_add_sub_graph(file_name, graph_caption)


def round_to_x_minus_1_digits_nearest_5(num):
    if num is None or (isinstance(num, float) and (math.isnan(num) or math.isinf(num))):
        return 1
    else:
        x = len(str(abs(int(num)))) if num != 0 else 1  # ensure x≥1 even for 0
        step = 5 * 10**(x - 2)
    return (math.ceil(num / step) * step) + step

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

def generate_repo_graph(repository_id, method, path, component, unit, developers, figure_caption_all, figure_caption):
    all_data = developers[TRANSIENT_FOUNDER] | developers[SUSTAINED_FOUNDER] | developers[TRANSIENT_JOINER] | developers[SUSTAINED_JOINER] | developers[MODERATE_FOUNDER] | developers[MODERATE_JOINER]
    y_axis_max = get_y_axis_max(all_data, unit)
    file_name, graph_caption = method(path + component + "/", component, 
                                  populate_touched_data(all_data, 
                                                unit), 
                                                "All",
                                                unit,
                                                y_axis_max,
                                                figure_size=WIDE_FIGURE)
    latex = latex_add_graph(file_name, figure_caption_all.format(repo=repository_id, num=str(len(all_data.keys())), component=component, unit=UNIT_FREQUENCY.get(unit, "Commits").lower() + "s", all="All"))
    all_data = developers[TRANSIENT_FOUNDER] | developers[SUSTAINED_FOUNDER] | developers[MODERATE_FOUNDER] 
    file_name, graph_caption = method(path + component + "/", component, 
                                  populate_touched_data(all_data, 
                                                unit), 
                                                "All Founders",
                                                unit,
                                                y_axis_max,
                                                figure_size=WIDE_FIGURE)
    latex += latex_add_graph(file_name, figure_caption_all.format(repo=repository_id, num=str(len(all_data.keys())), component=component, unit=UNIT_FREQUENCY.get(unit, "Commits").lower() + "s", all="All Founders"))
    all_data = developers[TRANSIENT_JOINER] | developers[SUSTAINED_JOINER] | developers[MODERATE_JOINER] 
    file_name, graph_caption = method(path + component + "/", component, 
                                  populate_touched_data(all_data, 
                                                unit), 
                                                "All Joiners",
                                                unit,
                                                y_axis_max,
                                                figure_size=WIDE_FIGURE)
    latex += latex_add_graph(file_name, figure_caption_all.format(repo=repository_id, num=str(len(all_data.keys())), component=component, unit=UNIT_FREQUENCY.get(unit, "Commits").lower() + "s", all="All Joiners"))
    latex += "\\newpage \n"
    return latex

def generate_component_latex(repository_id, method, path, component, unit, developers, figure_caption_all, figure_caption, commit_prefix):
    latex = latex_start_graph()
    max_y_axis = get_y_axis_max_for_categories(developers, unit)
    for category in DEVELOPER_CATEGORY:
        stage_developers = developers[category]
        latex += get_data_and_generate_graph(method, path, component, stage_developers, category, unit, max_y_axis[category.split(" ")[0]])
    latex += "\\caption{" + figure_caption.format(component=component, unit=UNIT_FREQUENCY.get(unit, "Commits").lower()) + "} \n"
    latex += latex_end_graph()        
    return latex

def default_generate_save(method, base_file_name, file_name, repository_id, component, developers, unit=NUMBER_OF_WEEKS, figure_caption_all=ALL_FIGURE_CAPTION, figure_caption=FIGURE_CAPTION, commit_prefix="commit"):
    path = "repository/"
    if repository_id > 0:
            path+= str(repository_id) + "/"
            figure_caption_all = FIGURE_CAPTION_START.format(repo=repository_id) + figure_caption_all
            figure_caption = FIGURE_CAPTION_START.format(repo=repository_id) + figure_caption
    read_write_file.create_directory(path)
    latex = ""
    latex_component = ""
    latex += generate_repo_graph(repository_id, method, path, component, unit, developers, figure_caption_all, figure_caption)
    latex_component += generate_component_latex(repository_id, method, path, component, unit, developers, figure_caption_all, figure_caption, commit_prefix)
    read_write_file.append_to_file(get_base_file_name(file_name) + "_" + UNIT_FREQUENCY.get(unit, "commit") + ".tex", latex, path)
    read_write_file.append_to_file(get_base_file_name(file_name) + "_" + UNIT_FREQUENCY.get(unit, "commit") + "_component.tex", latex_component, path)

def generate_and_save(repository_id, component, developers, number_of_commits=0):
    path = "repository/" 
    file_name = FILE_NAME
    base_file_name = FILE_NAME
    commit_prefix = "commit"
    time_series_commits = TIME_SERIES_NUMBER_OF_COMMIT
    if repository_id > 0:
        path+= str(repository_id) + "/" 
    file_name += "_" + str(number_of_commits)
    if number_of_commits > 0:        
        commit_prefix = "first " + word_engine.number_to_words(number_of_commits) + " commits"
        time_series_commits = number_of_commits
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        latex = section_sub_heading(repository_id, commit_prefix + " and for each period")
        save_to_latex_file(get_base_file_name(base_file_name), BASE_FILE_NAME, latex, path)

    if component == "packages":
        latex = section_sub_sub_heading(repository_id, component, commit_prefix)
        save_to_latex_file(get_base_file_name(file_name) + "_" + UNIT_FREQUENCY.get(time_series_commits, "commit"), 
                           get_base_file_name(base_file_name) + ".tex",
                           latex, path)
        
        latex = section_sub_sub_heading(repository_id, component, " each week")
        save_to_latex_file(get_base_file_name(file_name) + "_" + UNIT_FREQUENCY.get(NUMBER_OF_WEEKS, "commit"), 
                           get_base_file_name(base_file_name) + ".tex",
                           latex, path)
        save_to_latex_file(get_base_file_name(file_name) + "_" + UNIT_FREQUENCY.get(time_series_commits, "commit") + "_componet", 
                           get_base_file_name(base_file_name) + ".tex",
                           latex, path)
        save_to_latex_file(get_base_file_name(file_name) + "_" + UNIT_FREQUENCY.get(NUMBER_OF_WEEKS, "commit") + "_componet", 
                           get_base_file_name(base_file_name) + ".tex",
                           latex, path)
    else:
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", 
                               section_sub_sub_heading(repository_id, component, commit_prefix), path)

    
       
    default_generate_save(generate_graph, base_file_name, file_name, repository_id, component, developers, figure_caption=FIGURE_CAPTION, figure_caption_all=ALL_FIGURE_CAPTION, unit=time_series_commits, commit_prefix=commit_prefix)
    if number_of_commits == 0:
        read_write_file.append_to_file(get_base_file_name(file_name) + ".tex", 
                                section_sub_sub_heading(repository_id, component, "each period"), path)
        default_generate_save(generate_graph, base_file_name, file_name, repository_id, component, developers, figure_caption=FIGURE_CAPTION, figure_caption_all=ALL_FIGURE_CAPTION, unit=NUMBER_OF_WEEKS, commit_prefix=commit_prefix)
