from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import *
from codebase_graph_latex.developer_data import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_1.tex"
DEFAULT_COLOURS = [
    "Purple", "Blue", "Green", "Red", "Orange", "Salmon", "Cyan", "Magenta", "Yellow", "Black",
    "Brown", "Pink", "Gray", "Violet", "Olive", "Teal", "Navy", "Maroon", "Lime", "Coral",
    "Gold", "Silver", "Beige", "Turquoise", "Indigo", "Lavender", "Khaki", "Crimson", "Plum", "Tan",
    "Azure", "RosyBrown", "SteelBlue", "Chocolate", "Orchid", "Ivory", "SlateGray", "SeaGreen", "Tomato", "DodgerBlue",
    "FireBrick", "ForestGreen", "HotPink", "LightSkyBlue", "MediumPurple", "DarkOrange", "DarkCyan", "LightCoral", "Sienna", "Maroon"
]

FIGURE_CAPTION = "First {first_developers_word} {first_developers} " + SUSTAINED_JOINER + " "
FIGURE_CAPTION += " developers from this repository. The number of {x_axis} against the number of components touched. "

def section_heading(repository_id, x_axis, first_developer_num):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For developer " + AXIS_NAME[x_axis] + " and components touched.} \n"
    latex += "A scatter plot for the first " + str(first_developer_num)
    latex += " " + SUSTAINED + " late " + JOINER + " developers showing "
    latex += "the number of " + AXIS_NAME[x_axis] + " to components touched. \n"
    return latex

def generate_scatter(path, component, developers, x_axis=NUMBER_OF_COMMIT):
    first_developers = list(developers.items())[:len(DEFAULT_COLOURS)]
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    colours = DEFAULT_COLOURS.copy()
    latex_table = "\\begin{table}[H]\n"
    latex_table += "\\centering\n"
    latex_table += "\\caption{Table of first " + str(len(first_developers)) + " developers in the Scatter Developer graphs."
    latex_table += " } \n"
    latex_table += "\\label{tab:first_developers}\n"
    latex_table += "\\begin{tabular}{rl}\n"
    latex_table += "\\toprule\n"
    latex_table += "\\textbf{Developer ID} & \\textbf{Colour} \\\\ \n"
    latex_table += "\\midrule\n"
    counter = 0
    for key, value in first_developers:
        colour = colours.pop()
        latex_table += str(key) + " & \\color{" + colour + "}" + colour
        latex_table += " \\\\ \n"
        plt.plot(value[x_axis], value[KNOWN_Y_AXIS], color=colour)
        counter += 1
    latex_table += "\\bottomrule\n"
    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{table}\n"
    latex_table += "\\newpage \n"
    file_name = save_graph(path, component, "developer." + AXIS_NAME[x_axis], False, x_axis="Number of " + AXIS_NAME[x_axis])
    return latex_add_sub_graph(file_name, component), latex_table, len(first_developers)

def generate_and_save(repository_id, component, developers, x_axis=NUMBER_OF_COMMIT):
    path = "repository/" + str(repository_id) + "/" 
    latex = ""
    latex_scatter, latex_colour, first_developer_num = generate_scatter(path + component + "/", component, developers, x_axis)
    if component == "packages":
        
        latex += section_heading(repository_id, x_axis, first_developer_num)
        read_write_file.write_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", "", path)
        read_write_file.append_to_file(BASE_FILE_NAME, 
                                       "\\input{" + path + get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + "}\n", 
                                       DIRECTORY)
        if x_axis == NUMBER_OF_COMMIT:
            latex  += latex_colour
        latex += latex_start_graph()
    elif component == "classes":
        latex += latex_new_row()
    latex += latex_scatter
    if component == "methods":
        latex += "\\caption[Short]{"
        latex += "\\begin{minipage}[t]{\\linewidth}" 
        latex += FIGURE_CAPTION.format(x_axis=AXIS_NAME[x_axis], first_developers_word=word_engine.number_to_words(first_developer_num), first_developers=str(first_developer_num)) + "Developers with colours are shown in Table \\ref{tab:first_developers}." 
        latex += "\\end{minipage}"
        latex += "} \n"
        latex += latex_end_graph()
        
    read_write_file.append_to_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", latex, path)
