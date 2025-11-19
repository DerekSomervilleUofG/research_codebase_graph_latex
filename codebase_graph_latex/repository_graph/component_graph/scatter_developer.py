from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import *
from codebase_graph_latex.developer_data import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_1.tex"
MINIMUM_NUMBER_OF_COMMTIS = 20
DEFAULT_COLOURS = ["Purple", "Blue", "Green", "Red", "Orange", "Salmon", "Cyan", 
                   "Magenta", "Yellow", "Black", "Brown", "Pink", "Gray", "Violet",
                   "Olive", "Teal", "Navy", "Maroon", "Lime", "Coral"]

FIGURE_CAPTION = "First " + word_engine.number_to_words(MINIMUM_NUMBER_OF_COMMTIS) + " " + SUSTAINED_JOINER + " "
FIGURE_CAPTION += " developers from this repository. The number of {x_axis} against the number of components touched. " 

def section_heading(repository_id, x_axis):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For developer " + AXIS_NAME[x_axis] + " and components touched.} \n"
    latex += "A scatter plot for the first " + str(MINIMUM_NUMBER_OF_COMMTIS) 
    latex += " " + SUSTAINED + " late " + JOINER + " developers showing "
    latex += "the number of " + AXIS_NAME[x_axis] + " to components touched. \n"
    return latex

def generate_scatter(path, component, developers, x_axis=NUMBER_OF_COMMIT):
    first_developers = list(developers.items())[:MINIMUM_NUMBER_OF_COMMTIS]
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    colours = DEFAULT_COLOURS.copy()
    latex = ""
    counter = 0
    for key, value in first_developers:
        colour = colours.pop()
        latex += "\\color{" + colour + "}Developer: " + str(key) + " in colour " + colour + ". "
        plt.plot(value[x_axis], value[KNOWN_Y_AXIS], color=colour)
        counter += 1
    file_name = save_graph(path, component, "developer." + AXIS_NAME[x_axis], False, x_axis="Number of " + AXIS_NAME[x_axis])
    return latex_add_sub_graph(file_name, component), latex

def generate_and_save(repository_id, component, developers, x_axis=NUMBER_OF_COMMIT):
    path = "repository/" + str(repository_id) + "/" 
    latex = ""
    if component == "packages":
        latex += section_heading(repository_id, x_axis)
        read_write_file.write_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", "", path)
        latex  += latex_start_graph()
        read_write_file.append_to_file(BASE_FILE_NAME, 
                                       "\\input{" + path + get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + "}\n", 
                                       DIRECTORY)
    elif component == "classes":
        latex += latex_new_row()
    latex_scatter, latex_colour = generate_scatter(path + component + "/", component, developers, x_axis)
    latex += latex_scatter
    if component == "methods":
        latex += "\\caption[Short]{"
        latex += "\\begin{minipage}[t]{\\linewidth}" 
        latex += FIGURE_CAPTION.format(x_axis=AXIS_NAME[x_axis])
        latex += latex_colour 
        latex += "\\end{minipage}"
        latex += "} \n"
        latex += latex_end_graph()    
    read_write_file.append_to_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", latex, path)
