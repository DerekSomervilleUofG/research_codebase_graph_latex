from codebase_graph_latex.repository_graph.master_graph import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_2.tex"
PERCENTAGE_TOUCHED = 0.8
CAPTION = "{type}"
FIGURE_CAPTION = "A histogram of number of developers that have touched a percentage ({percentage}\%) of {component} each {unit} of a year. "

def section_sub_heading(repository_id, component, percentage_touched):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For component touched for to reach " + str(percentage_touched * 100 ) + " percentage known} \n"
    latex += "A histogram of number of developers that have touched a percentage of " + component + " each period \n"
    return latex

def find_day_at_threshold(touched, threshold):
    counter = len(touched) - 1
    threshold_met = False
    while threshold_met:
        if touched[counter] <= threshold:
            threshold_met = True
        counter -= 1
    return counter 

def populate_data(developers, UNIT, percentage_touched):
    period = []
    for id, values in developers.items():
        counter = find_day_at_threshold(values[KNOWN_Y_AXIS], values[KNOWN_Y_AXIS][-1] * percentage_touched)
        period.append(int((values[YEAR_PERIOD][counter]/ 365) * UNIT))      
    return period

def developer_graph(file_name, developers, table_suffix, repository_id, type, param_x_axis, param_caption, sub_graph=True):
    path = DIRECTORY
    if repository_id > 0:
        path += str(repository_id) + "/"
    else:
        path += "graph/"
    x_axis = "Average number of touched " + table_suffix 
    read_write_file.create_directory(path)
    file_name = path + get_base_file_name(file_name) + "." + table_suffix.lower().replace(" ", ".") 
    if type != "":
        file_name += "." + type.lower().replace(" ", ".")
    file_name += ".pdf"
    months = list(range(1, 13))
    plt.figure(figsize=SMALL_FIGURE)
    plt.hist(developers, BINS)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    if param_x_axis != "":
        x_axis = param_x_axis
    plt.subplots_adjust(left=0.15)
    plt.xlabel(x_axis, fontsize=7)
    plt.xticks(months)
    plt.ylabel('Number of Developers', fontsize=8)
    plt.tight_layout() 
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    if sub_graph:
        latex = latex_add_sub_graph(file_name, param_caption)
    else:
        latex = latex_add_graph(file_name, param_caption)
    return latex

def generate_graph(repository_id, component, period, type, unit, percentage_touched):
    return developer_graph(FILE_NAME, 
                           period, 
                           component + "." + type.lower().replace(" ",".") + "." + UNIT_FREQUENCY[unit].lower(), 
                           repository_id, 
                           type + str(percentage_touched * 100), 
                           UNIT_FREQUENCY[unit], 
                           CAPTION.format(type=type)) 

def generate_latex(repository_id, component, unit, developers, percentage_touched):
    latex  = latex_start_graph()
    all_data = developers[TRANSIENT_FOUNDER] | developers[SUSTAINED_FOUNDER] | developers[TRANSIENT_JOINER] | developers[SUSTAINED_JOINER]
    latex += generate_graph(repository_id, component, 
                                  populate_data(all_data, 
                                                unit, 
                                                percentage_touched), 
                                                "All",
                                                unit,
                                                percentage_touched)
    latex += generate_graph(repository_id, component, 
                                  populate_data(developers[TRANSIENT_FOUNDER], 
                                                unit, 
                                                percentage_touched), 
                                                TRANSIENT_FOUNDER,
                                                unit,
                                                percentage_touched)
    latex += generate_graph(repository_id, component, 
                                  populate_data(developers[SUSTAINED_FOUNDER], 
                                                unit, 
                                                percentage_touched), 
                                                SUSTAINED_FOUNDER,
                                                unit,
                                                percentage_touched)
    latex += generate_graph(repository_id, component, 
                                  populate_data(developers[TRANSIENT_JOINER], 
                                                unit, 
                                                percentage_touched), 
                                                TRANSIENT_JOINER,
                                                unit,
                                                percentage_touched)
    latex += generate_graph(repository_id, component, 
                                  populate_data(developers[SUSTAINED_JOINER], 
                                                unit, 
                                                percentage_touched), 
                                                SUSTAINED_JOINER,
                                                unit,
                                                percentage_touched)
    latex += "\\caption{" + FIGURE_CAPTION.format(component=component, percentage=(percentage_touched * 100), unit=UNIT_FREQUENCY[unit].lower()) + "} \n"
    latex += latex_end_graph()        
    return latex

def generate_and_save(repository_id, component, developers, percentage_touched=PERCENTAGE_TOUCHED, units=[NUMBER_OF_MONTHS]):
    path = "repository/" + str(repository_id) + "/" 
    latex = ""
    if component == "packages":
        read_write_file.write_file(get_base_file_name(FILE_NAME) + "." + str(percentage_touched * 100) + ".tex", 
                               section_sub_heading(repository_id, component, percentage_touched), path)
        base_latex =  "\\input{" + path + get_base_file_name(FILE_NAME) + "." + str(percentage_touched * 100)  + "}\n"
        read_write_file.append_to_file(BASE_FILE_NAME, 
                                   base_latex, 
                                    DIRECTORY)
    for unit in units:
        latex += generate_latex(repository_id, component, unit, developers, percentage_touched)
    read_write_file.append_to_file(get_base_file_name(FILE_NAME) + "." + str(percentage_touched * 100) + ".tex", latex, path)
    