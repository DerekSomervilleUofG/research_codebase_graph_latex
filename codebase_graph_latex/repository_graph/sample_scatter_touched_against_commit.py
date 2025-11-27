from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.store_developer_data import *
import numpy

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"

X_AXIS = "X_AXIS"
Y_AXIS = "Y_AXIS"

GRAPH_CAPTION = "{component}"
FIGURE_CAPTION = "Scatter plots of the log total number of components touched (y-axis) " \
                "against the number of commits (x-axis) made by "

def section_heading(file_name, sub_section="", title="", x_axis="commits"):
    latex =  get_section_start(file_name, sub_section) + title 
    latex += "} \n"
    latex += "A scatter plot of touched components by number of " + x_axis + ". \n "
    latex += DEVELOPER_IGNORE + " \n"
    return latex    

def get_developer_knowledge(developers):
    commit_number = []
    developer_knowledge = []
    for key, developer in developers.items():
        if developer[KNOWN_Y_AXIS][-1] > 0:
            commit_number.append(developer[NUMBER_OF_COMMIT][-1])
            developer_knowledge.append(developer[KNOWN_Y_AXIS][-1])
    return commit_number, developer_knowledge

def get_total_sample_numbers(component):
    founder_transient_num = len(get_transient_founder_component(component))
    founder_moderate_num = len(get_moderate_founder_component(component))
    founder_sustained_num = len(get_sustained_founder_component(component))
    joiner_transient_num = len(get_transient_joiner_component(component))
    joiner_moderate_num = len(get_moderate_joiner_component(component))
    joiner_sustained_num = len(get_sustained_joiner_component(component))
    return get_sample_numbers(founder_transient_num, founder_moderate_num, founder_sustained_num, joiner_transient_num, joiner_moderate_num, joiner_sustained_num)

def get_figure_caption(num1, num2, num3, num4, num5=0, num6=0):
    return FIGURE_CAPTION.format(number=num4) + get_figure_caption_numbers_suffix(FIGURE_CAPTION_NUMBERS, [num1, num2, num3, num4, num5, num6])

def get_figure_caption_with_numbers(component):
    founder_transient, founder_moderate, founder_sustained, joiner_transient, joiner_moderate, joiner_sustained = get_total_sample_numbers(component)
    return get_figure_caption(founder_transient, founder_moderate, founder_sustained, joiner_transient, joiner_moderate, joiner_sustained)

def get_sample_numbers(founder_transient_num, founder_moderate_num,founder_sustained_num, joiner_transient_num, joiner_moderate_num, joiner_sustained_num):
    if founder_transient_num > joiner_sustained_num:
        founder_transient_num = joiner_sustained_num
    if founder_moderate_num > joiner_sustained_num:
        founder_moderate_num = joiner_sustained_num
    if founder_sustained_num > joiner_sustained_num:
        founder_sustained_num = joiner_sustained_num
    if joiner_moderate_num > joiner_sustained_num: 
        joiner_moderate_num = joiner_sustained_num
    if joiner_transient_num > joiner_sustained_num:
        joiner_transient_num = joiner_sustained_num
    return founder_transient_num, founder_moderate_num, founder_sustained_num, joiner_transient_num, joiner_moderate_num, joiner_sustained_num

def get_sample_first_or_last(transient_developers, sustained_developers, colour, sample_of_developers):
    number_of_records = -1
    if len(transient_developers[X_AXIS]) > sample_of_developers:
        number_of_records = sample_of_developers
    plt.scatter(transient_developers[X_AXIS][0:number_of_records], 
                transient_developers[Y_AXIS][0:number_of_records], 
                color=colour, 
                alpha=1.0, 
                s=1.0)
    number_of_records = -1
    if len(sustained_developers[X_AXIS]) > sample_of_developers:
        number_of_records = sample_of_developers
    return_developers= {}
    return_developers[X_AXIS] = sustained_developers[X_AXIS][0:number_of_records]
    return_developers[Y_AXIS] = sustained_developers[Y_AXIS][0:number_of_records] 
    return return_developers

def compare_developers(path, component, 
                       transient_founder_developers, 
                       moderate_founder_developers,
                       sustained_founder_developers, 
                       transient_joiner_developers, 
                       moderate_joiner_developers,
                       sustained_joiner_developers, 
                       file_name_suffix, sample_of_developers, x_axis="Number of commits"):
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    knowledge = get_sample_first_or_last(moderate_founder_developers, 
                                         sustained_joiner_developers, 
                                         MODERATE_FOUNDER_COLOUR, 
                                         sample_of_developers)    
    knowledge = get_sample_first_or_last(moderate_joiner_developers, 
                                         sustained_joiner_developers, 
                                         MODERATE_JOINER_COLOUR, 
                                         sample_of_developers)    
    knowledge = get_sample_first_or_last(transient_joiner_developers, 
                                         sustained_joiner_developers, 
                                         TRANSIENT_JOINER_COLOUR, 
                                         sample_of_developers)    
    plt.scatter(knowledge[X_AXIS], knowledge[Y_AXIS], color=SUSTAINED_JOINER_COLOUR, alpha=1.0, s=1.0)
    knowledge = get_sample_first_or_last(transient_founder_developers, 
                                         sustained_founder_developers, 
                                         TRANSIENT_FOUNDER_COLOUR, 
                                         sample_of_developers)    
    plt.scatter(knowledge[X_AXIS], knowledge[Y_AXIS], color=SUSTAINED_FOUNDER_COLOUR, alpha=1.0, s=1.0)
    file_name = save_graph(path, component, file_name_suffix, x_axis=x_axis)
    return file_name

def save_graph(path, component, file_suffix="", log_switch=False, x_axis="Number of commits"):
    read_write_file.create_directory(path)
    plt.subplots_adjust(left=0.15)
    if log_switch:
        plt.yscale('log')
    plt.xlabel(x_axis)
    y_axis = component.capitalize() + " touched "
    if log_switch:
        y_axis += "(log)"
    plt.ylabel(y_axis)
    plt.grid(True)
    file_name = path + get_base_file_name(FILE_NAME) + "." + component 
    if file_suffix != "":
        file_name += "." + file_suffix
    file_name += ".pdf"
    plt.savefig(file_name, bbox_inches='tight')
    plt.clf()
    plt.close()
    return file_name

def generate_x_axis_and_y_axis(developers, method, param=""):
    if param == "":
        x_axis, y_axis = method(developers)
    else:
        x_axis, y_axis = method(developers, param)
    axis = {}
    axis[X_AXIS] = x_axis
    axis[Y_AXIS] = numpy.round(numpy.log10(y_axis), 3)
    return axis

def generate_compare_for_component(path):
    latex = latex_start_graph()
    for component in COMPONENTS:
        latex += latex_add_sub_graph(compare_developers(path, component, 
                                                        generate_x_axis_and_y_axis(get_transient_founder_component(component), 
                                                                                   get_developer_knowledge), 
                                                        generate_x_axis_and_y_axis(get_moderate_founder_component(component), 
                                                                                   get_developer_knowledge),
                                                        generate_x_axis_and_y_axis(get_sustained_founder_component(component), 
                                                                                   get_developer_knowledge),
                                                        generate_x_axis_and_y_axis(get_transient_joiner_component(component), 
                                                                                   get_developer_knowledge),
                                                        generate_x_axis_and_y_axis(get_moderate_joiner_component(component), 
                                                                                   get_developer_knowledge),
                                                        generate_x_axis_and_y_axis(get_sustained_joiner_component(component), 
                                                                                   get_developer_knowledge),
                                                        "sample.first",
                                                        len(get_sustained_joiner_component(component).values())
                                                        ), 
                                                        GRAPH_CAPTION.format(component=component).capitalize())
    latex += "\\caption{"
    founder_transient, founder_moderate, founder_sustained, joiner_transient, joiner_moderate, joiner_sustained = get_total_sample_numbers(component)
    latex += FIGURE_CAPTION
    latex += get_figure_caption_numbers_suffix(FIGURE_CAPTION_NUMBERS, [founder_transient, founder_moderate, founder_sustained, joiner_transient, joiner_moderate, joiner_sustained]) 
    latex += "} \n"
    latex += latex_end_graph()
    return latex

def generate_and_save():
    latex = get_section_start(FILE_NAME, "sub") + "} \n" 
    latex += generate_compare_for_component(DIRECTORY + "graph/")
    read_write_file.write_file(get_file_name(FILE_NAME), latex, DIRECTORY) 
    latex = "\\input{repository/" + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY) 

def repository_generate_and_save(repository_id, component, 
                                 developers):
    path = "repository/" + str(repository_id) + "/" 
    base_file_name = str(repository_id) + ".tex"
    latex_repo = ""
    if component == "packages":
        latex_repo += section_heading(FILE_NAME, "sub", "Repository: " + str(repository_id)) 
        latex_repo += latex_start_graph()
    elif component == "classes":
        latex_repo += latex_new_row()
    latex_repo += latex_add_sub_graph(compare_developers(path + component + "/", component, 
                                                         generate_x_axis_and_y_axis(developers[TRANSIENT_JOINER], 
                                                                                    get_developer_knowledge),
                                                         generate_x_axis_and_y_axis(developers[MODERATE_FOUNDER], 
                                                                                    get_developer_knowledge),
                                                         generate_x_axis_and_y_axis(developers[SUSTAINED_FOUNDER], 
                                                                                    get_developer_knowledge),
                                                         generate_x_axis_and_y_axis(developers[TRANSIENT_JOINER], 
                                                                                    get_developer_knowledge),
                                                         generate_x_axis_and_y_axis(developers[MODERATE_JOINER], 
                                                                                    get_developer_knowledge),
                                                         generate_x_axis_and_y_axis(developers[SUSTAINED_JOINER], 
                                                                                    get_developer_knowledge),
                                                         "sample.first",
                                                         len(developers[SUSTAINED_FOUNDER].values())),
                                                        GRAPH_CAPTION.format(component=component))
    if component == "methods":
        founder_transient_no, founder_moderate_no, founder_sustained_no, joiner_transient_no, joiner_moderate_no, joiner_sustained_no = get_sample_numbers(len(developers[TRANSIENT_FOUNDER].values()), 
                                                                                                                  len(developers[MODERATE_FOUNDER].values()), 
                                                                                                                    len(developers[SUSTAINED_FOUNDER].values()),
                                                                                                                    len(developers[TRANSIENT_JOINER].values()),
                                                                                                                    len(developers[MODERATE_JOINER].values()),
                                                                                                                    len(developers[SUSTAINED_JOINER].values()))
        latex_repo += "\\caption[Short]{"
        latex_repo += "\\begin{minipage}[t]{\\linewidth}" 
        latex_repo += FIGURE_CAPTION
        latex_repo += get_figure_caption_numbers_suffix(FIGURE_CAPTION_NUMBERS, [founder_transient_no, 
                                                        founder_moderate_no,
                                                        founder_sustained_no, 
                                                        joiner_transient_no,
                                                        joiner_moderate_no, 
                                                        joiner_sustained_no])
        latex_repo += "\\end{minipage}"
        latex_repo += "} \n"
        latex_repo += latex_end_graph()
    read_write_file.append_to_file(base_file_name, latex_repo, path)
