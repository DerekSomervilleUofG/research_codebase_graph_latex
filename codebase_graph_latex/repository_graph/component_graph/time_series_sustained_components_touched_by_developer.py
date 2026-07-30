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
Y_AXIS = {0: "touched", 1: "methods div packages ratio"}
COMPONENT_Y_AXIS_MAX = {COMPONENT_TOUCHED: {"packages": 250, "classes": 1800, "methods": 8000}, COMPONENT_RATIO: {"packages": 10, "classes": 10, "methods": 250}}

FIGURE_CAPTION = "Repo: {repo}. First {first_founder_developers_word} ({first_founder_developers}) " + SUSTAINED_FOUNDER + " and first {first_joiner_developers_word} ({first_joiner_developers}) " + SUSTAINED_JOINER 
FIGURE_CAPTION += " developers. The number of components {y_axis} (y-axis) against the number of {x_axis} (x-axis). "
RATIO_NUMBER_OF_COMMITS = 20
founder_package_touched = []
late_joiner_package_touched = []
founder_ratio = []
late_joiner_ratio = []

def calculate_ratio(package_touched, method_touched):
    ratio = []
    counter = 0
    for touched in package_touched:
        ratio.append(list(map(lambda pair: pair[1] / pair[0], zip(touched, method_touched[counter]))))
        counter += 1
    return ratio

def generate_scatter(repository_id, path, component, developers, x_axis, y_axis_max, category, y_axis, ratio):
    first_developers = list(developers.items())[:len(DEFAULT_COLOURS)]
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    colours = DEFAULT_COLOURS.copy()
    latex_table = "\\begin{table}[H]\n"
    latex_table += "\\centering\n"
    latex_table += "\\caption{Table of first " + str(len(first_developers)) + " " + category + " developers in the Scatter Developer graphs."
    latex_table += " } \n"
    latex_table += "\\label{tab:first_developers_" + str(repository_id) + category.replace(" ", "_") + "}\n"
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
        if y_axis == COMPONENT_TOUCHED:
            plt.plot(value[x_axis], value[KNOWN_Y_AXIS], color=colour)
        elif y_axis == COMPONENT_RATIO and component == "methods":
            plt.plot(value[x_axis][:RATIO_NUMBER_OF_COMMITS], ratio[counter][:RATIO_NUMBER_OF_COMMITS], color=colour)
        counter += 1
    latex_table += "\\bottomrule\n"
    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{table}\n"
    latex_table += "\\newpage \n"
    file_name = save_graph(path, component, "developer." + AXIS_NAME[x_axis] + "." + category + "." + Y_AXIS[y_axis].replace(" ", "_"), False, x_axis="Number of " + AXIS_NAME[x_axis], y_axis_param=Y_AXIS[y_axis])
    return latex_add_sub_graph(file_name, component.capitalize() + " for " + category), latex_table, len(first_developers)

def get_component_touched(developers):
    package_touched = []
    first_developers = list(developers.items())[:len(DEFAULT_COLOURS)]
    for key, value in first_developers:
        package_touched.append(value[KNOWN_Y_AXIS])
    return package_touched

def generate_and_save(repository_id, component, sustained_founder_developers, sustained_joiner_developers, x_axis=NUMBER_OF_COMMIT, y_axis=TOUCHED):
    global founder_package_touched, late_joiner_package_touched
    path = DIRECTORY + str(repository_id) + "/" 
    founder_ratio = []
    late_joiner_ratio = []
    if y_axis == COMPONENT_RATIO and component == "methods":
        founder_ratio = calculate_ratio(founder_package_touched, get_component_touched(sustained_founder_developers))
        late_joiner_ratio = calculate_ratio(late_joiner_package_touched, get_component_touched(sustained_joiner_developers))
    latex = ""

    latex_scatter_founder, latex_founder_colour, first_founder_developer_num = generate_scatter(repository_id, path + component + "/", component, sustained_founder_developers, x_axis, COMPONENT_Y_AXIS_MAX[y_axis][component], SUSTAINED_FOUNDER, y_axis, founder_ratio)
    latex_scatter_joiner, latex_joiner_colour, first_joiner_developer_num = generate_scatter(repository_id, path + component + "/", component, sustained_joiner_developers, x_axis, COMPONENT_Y_AXIS_MAX[y_axis][component], SUSTAINED_JOINER, y_axis, late_joiner_ratio)
    if component == "packages" and y_axis == COMPONENT_TOUCHED:
        read_write_file.write_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", "", path)
        read_write_file.append_to_file(BASE_FILE_NAME, 
                                       "\\input{" + path + get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + "}\n", 
                                       DIRECTORY)
        if x_axis == NUMBER_OF_COMMIT:
            latex += latex_founder_colour
            latex += latex_joiner_colour
        if y_axis == COMPONENT_TOUCHED:
            latex += latex_start_graph()
    if y_axis == COMPONENT_RATIO and component == "packages":
        founder_package_touched = get_component_touched(sustained_founder_developers)
        late_joiner_package_touched = get_component_touched(sustained_joiner_developers)
    elif component == "classes" and y_axis == COMPONENT_TOUCHED:
        latex += latex_new_row()
    if y_axis == COMPONENT_TOUCHED:
        latex += latex_scatter_founder
        latex += latex_scatter_joiner
    elif y_axis == COMPONENT_RATIO and component == "methods":
        latex += latex_start_graph()
        latex += latex_scatter_founder
        latex += latex_scatter_joiner
    if component == "methods":
        latex += "\\caption[Time series of sustained components touched for repository:" + str(repository_id) + " x-axis:" + AXIS_NAME[x_axis] + "]{"
        latex += FIGURE_CAPTION.format(repo=repository_id, x_axis=AXIS_NAME[x_axis], y_axis=Y_AXIS[y_axis], first_founder_developers_word=word_engine.number_to_words(first_founder_developer_num), first_founder_developers=str(first_founder_developer_num), first_joiner_developers_word=word_engine.number_to_words(first_joiner_developer_num), first_joiner_developers=str(first_joiner_developer_num)) 
        latex += SUSTAINED_FOUNDER.capitalize() + " developers with colours are shown in Table \\ref{tab:first_developers_" + str(repository_id) + SUSTAINED_FOUNDER.replace(" ", "_") + "}. " 
        latex += SUSTAINED_JOINER.capitalize() + " developers with colours are shown in Table \\ref{tab:first_developers_" + str(repository_id) + SUSTAINED_JOINER.replace(" ", "_") + "}." 
        latex += "} \n"
        latex += latex_end_graph(FILE_NAME + "_" + str(repository_id) + "_" + str(x_axis) + "_" + str(y_axis))
        
    read_write_file.append_to_file(get_base_file_name(FILE_NAME) + "." + AXIS_NAME[x_axis] + ".tex", latex, path)
