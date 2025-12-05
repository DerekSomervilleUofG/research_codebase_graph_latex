from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import *
from codebase_graph_latex.developer_data import *

FILE_NAME = __name__
BASE_FILE_NAME = REPOSITORY_1_FILE
DEFAULT_COLOURS = [
    "Purple", "Blue", "Green", "Red", "Orange", "Salmon", "Cyan", "Magenta", "Yellow", "Black",
    "Brown", "Pink", "Gray", "Violet", "Olive", "Teal", "Navy", "Maroon", "Lime", "Coral",
    "Gold", "Silver", "Beige", "Turquoise", "Indigo", "Lavender", "Khaki", "Crimson", "Plum", "Tan",
    "Azure", "RosyBrown", "SteelBlue", "Chocolate", "Orchid", "Ivory", "SlateGray", "SeaGreen", "Tomato", "DodgerBlue",
    "FireBrick", "ForestGreen", "HotPink", "LightSkyBlue", "MediumPurple", "DarkOrange", "DarkCyan", "LightCoral", "Sienna", "Maroon"
]
COMPONENT_Y_AXIS_MAX = {"packages": 250, "classes": 3000, "methods": 10000}

FIGURE_CAPTION = "Repo: {repo}. First {first_founder_developers_word} ({first_founder_developers}) " + SUSTAINED_FOUNDER + " and first {first_joiner_developers_word} ({first_joiner_developers}) " + SUSTAINED_JOINER 
FIGURE_CAPTION += " developers. The number of components touched (y-axis) against the number of {x_axis} (x-axis). "

def section_heading(repository_id, x_axis):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For developer " + AXIS_NAME[x_axis] + " and components touched.} \n"
    return latex

def generate_scatter(repository_id, path, component, developers, x_axis, y_axis_max, category):
    first_developers = list(developers.items())[:len(DEFAULT_COLOURS)]
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    colours = DEFAULT_COLOURS.copy()
    latex_table = "\\begin{table}[H]\n"
    latex_table += "\\centering\n"
    latex_table += "\\caption{Table of first " + str(len(first_developers)) + " " + category + " developers in the Scatter Developer graphs."
    latex_table += " } \n"
    latex_table += "\\label{tab:" + str(repository_id) + "first_developers" + category.replace(" ", "_") + "}\n"
    latex_table += "\\begin{tabular}{rl}\n"
    latex_table += "\\toprule\n"
    latex_table += "\\textbf{Developer ID} & \\textbf{Colour} \\\\ \n"
    latex_table += "\\midrule\n"
    counter = 0
    plt.yticks(np.arange(0, y_axis_max + 1, step=y_axis_max // 10))
    plt.ylim(0, y_axis_max)
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
    file_name = save_graph(path, component, "developer." + AXIS_NAME[x_axis] + "." + category, False, x_axis="Number of " + AXIS_NAME[x_axis])
    return latex_add_sub_graph(file_name, component.capitalize() + " for " + category), latex_table, len(first_developers)

def generate_and_save(repository_id, component, sustained_founder_developers, sustained_joiner_developers, x_axis=NUMBER_OF_COMMIT):
    path = "repository/" + str(repository_id) + "/" 
    latex = ""
    latex_scatter_founder, latex_founder_colour, first_founder_developer_num = generate_scatter(repository_id, path + component + "/", component, sustained_founder_developers, x_axis, COMPONENT_Y_AXIS_MAX[component], SUSTAINED_FOUNDER)
    latex_scatter_joiner, latex_joiner_colour, first_joiner_developer_num = generate_scatter(repository_id, path + component + "/", component, sustained_joiner_developers, x_axis, COMPONENT_Y_AXIS_MAX[component], SUSTAINED_JOINER)
    if component == "packages":
        
        latex += section_heading(repository_id, x_axis)
        read_write_file.write_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", "", path)
        read_write_file.append_to_file(BASE_FILE_NAME, 
                                       "\\input{" + path + get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + "}\n", 
                                       DIRECTORY)
        if x_axis == NUMBER_OF_COMMIT:
            latex += latex_founder_colour
            latex += latex_joiner_colour
        latex += latex_start_graph()
    elif component == "classes":
        latex += latex_new_row()
    latex += latex_scatter_founder
    latex += latex_scatter_joiner
    if component == "methods":
        latex += "\\caption{"
        latex += FIGURE_CAPTION.format(repo=repository_id, x_axis=AXIS_NAME[x_axis], first_founder_developers_word=word_engine.number_to_words(first_founder_developer_num), first_founder_developers=str(first_founder_developer_num), first_joiner_developers_word=word_engine.number_to_words(first_joiner_developer_num), first_joiner_developers=str(first_joiner_developer_num)) 
        latex += SUSTAINED_FOUNDER.capitalize() + " developers with colours are shown in Table \\ref{tab:" + str(repository_id) + "first_developers" + SUSTAINED_FOUNDER.replace(" ", "_") + "}. " 
        latex += SUSTAINED_JOINER.capitalize() + " developers with colours are shown in Table \\ref{tab:" + str(repository_id) + "first_developers" + SUSTAINED_JOINER.replace(" ", "_") + "}." 
        latex += "} \n"
        latex += latex_end_graph()
        
    read_write_file.append_to_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", latex, path)
