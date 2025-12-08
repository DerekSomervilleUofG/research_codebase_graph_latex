import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from codebase_graph_latex.FigureCounter import FigureCounter
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.constants import *


figure_counter = FigureCounter()
BINS = 50
NUMBER_GRAPHS_TO_PAGE = 6
NUMBER_GRAPHS_TO_ROW = 2
MAX_Y_AXIS = 40
graph_number = None
read_write_file = ReadWriteFile()

def set_graph_number(number):
    global graph_number
    graph_number = number
def get_graph_number():
    return graph_number

def latex_start_graph():
    latex = "\\begin{figure}[!htbp]\n"
    latex += "  \\centering \n"
    global graph_number, figure_counter
    graph_number = 0
    figure_counter.increment_graph()
    return latex

def latex_end_graph():
    latex = "  \\hfill \n"
    latex += "\\end{figure}\n"
    latex += "\\newpage \n"
    global graph_number
    graph_number = None
    return  latex

def latex_new_row():
    return "  \\vspace{0.5cm}\n"

def get_section_start(file_name, sub_type=""):
    return "\\" + sub_type + "section{" + file_name.split(".")[-1].replace("_", " ").capitalize() + " - "


def __add_graph_latex(file_path, caption, figure="subfigure", size=0.48, placement="b"):
    global figure_counter
    label = "figure." + str(figure_counter.get_counter())
    latex = "  \\hfill \n"
    latex += "  \\begin{" + figure + "}["+ placement + "] \n"
    if size > 0:
        latex += "{" + str(size) + "\\textwidth}\n"
    latex += "    \\includegraphics{" + file_path + "}\n"
    latex += "    \\caption{" + caption.replace("_", " ") + "}\n"
    latex += "    \\label{" + label + "}\n"
    latex += "  \\end{" + figure + "}\n"
    return latex

def latex_add_graph(file_path, caption):
    return __add_graph_latex(file_path, caption, "figure", 0, "h!") + "\n \\newpage \n"

def latex_add_sub_graph(file_path, caption):
    global graph_number, figure_counter
    figure_counter.increment_sub_graph()
    latex = ""
    if graph_number is not None and graph_number > 0 and graph_number % NUMBER_GRAPHS_TO_PAGE == 0:
        latex += "\\caption{Part " + str(graph_number// NUMBER_GRAPHS_TO_PAGE) + " continued on next page.}\n"
        local_graph_number = graph_number
        latex += latex_end_graph()
        latex += latex_start_graph()
        set_graph_number(local_graph_number)
    elif graph_number is not None and graph_number > 0 and graph_number % NUMBER_GRAPHS_TO_ROW == 0:
        latex += latex_new_row()
    latex += __add_graph_latex(file_path, caption)
    if graph_number is not None:
        graph_number += 1
    return latex

def developer_graph(file_name, developers, table_suffix, repository_id, 
                    type, param_x_axis="", param_caption="", 
                    sub_graph=True, 
                    max_x_axis=0, 
                    max_y_axis=0, 
                    bins=BINS,
                    figure_size=SMALL_FIGURE):
    path = DIRECTORY
    if repository_id > 0:
        path += str(repository_id) + "/"
    else:
        path += "graph/"
    x_axis = "Average number of "
    if table_suffix in ["packages", "files", "classes", "methods"]:
        x_axis += "touched "
    x_axis += table_suffix
    read_write_file.create_directory(path)
    file_name = path + get_base_file_name(file_name) + "." + table_suffix.lower().replace(" ", ".") 
    if type != "":
        file_name += "." + type.lower().replace(" ", ".")
    file_name += ".pdf"
    plt.figure(figsize=figure_size)
    plt.hist(developers, bins=bins)
    max_height = max([patch.get_height() for patch in plt.gca().patches])
    if max_x_axis > 0:
        plt.xlim(0, max_x_axis)
    if max_y_axis > 0:
        plt.ylim(0, max_y_axis)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    if param_x_axis != "":
        x_axis = param_x_axis
    plt.subplots_adjust(left=0.15)
    plt.xlabel(x_axis, fontsize=7)
    plt.ylabel('Number of Developers', fontsize=8)
    plt.tight_layout() 
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    #param_caption += "The maximum number of developers is " + str(int(max_height)) + "."
    if sub_graph:
        latex = latex_add_sub_graph(file_name, param_caption)
    else:
        latex = latex_add_graph(file_name, param_caption)
    return latex

def developer_percentage_graph(file_name, developers, weights, table_suffix, repository_id, 
                    type, param_x_axis="", param_caption="", 
                    sub_graph=True, 
                    max_x_axis=0, 
                    bins=BINS,
                    figure_size=SMALL_FIGURE):
    path = DIRECTORY
    if repository_id > 0:
        path += str(repository_id) + "/"
    else:
        path += "graph/"
    x_axis = "Average number of "
    if table_suffix in ["packages", "files", "classes", "methods"]:
        x_axis += "touched "
    x_axis += table_suffix
    read_write_file.create_directory(path)
    file_name = path + get_base_file_name(file_name) + "." + table_suffix.lower().replace(" ", ".") 
    if type != "":
        file_name += "." + type.lower().replace(" ", ".")
    file_name += ".pdf"
    plt.figure(figsize=figure_size)
    plt.hist(developers, bins=bins, weights=weights)
    if max_x_axis > 0:
        plt.xlim(0, max_x_axis)
    plt.ylim(0, MAX_Y_AXIS)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    if param_x_axis != "":
        x_axis = param_x_axis
    plt.subplots_adjust(left=0.15)
    plt.xlabel(x_axis, fontsize=7)
    plt.ylabel('Percentage of Developers', fontsize=8)
    plt.tight_layout() 
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    if sub_graph:
        latex = latex_add_sub_graph(file_name, param_caption)
    else:
        latex = latex_add_graph(file_name, param_caption)
    return latex

def get_base_file_name(file_name):
    return file_name.split(".")[-1]

def get_file_name(file_name):
    return get_base_file_name(file_name) + ".tex"
