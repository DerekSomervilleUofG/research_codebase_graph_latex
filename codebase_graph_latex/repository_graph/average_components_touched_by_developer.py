from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
import math

FILE_NAME = __name__
BASE_FILE_NAME = REPOSITORY_SUMMARY_1_FILE
GRAPH_CAPTION = "{period} new {component}. "
FIGURE_CAPTION = "Average number of new components touched per day and per commit (x-axis) for {num} " + SUSTAINED_JOINER + " developers (y-axis) "
FIGURE_CAPTION += "from {number_of_repository_word} ({number_of_repository}) repositories sampled from GitHub."

MAX_Y_AXIS = 140
commit_package_average = []
commit_file_average = []
commit_class_average = []
commit_method_average = []
daily_file_average = []
daily_package_average = []
daily_class_average = []
daily_method_average = []
    
def merge_average(daily, commit, component):
    global daily_package_average, daily_file_average, daily_class_average, daily_method_average
    global commit_package_average, commit_file_average, commit_class_average, commit_method_average
    if component == "packages":
        commit_package_average += commit
        daily_package_average += daily
    elif component == "files":
        commit_file_average += commit
        daily_file_average += daily
    elif component == "classes":
        commit_class_average += commit
        daily_class_average += daily
    elif component == "methods":
        commit_method_average += commit
        daily_method_average += daily

def generate_average(number_of_repository):
    latex_repo = get_section_start(FILE_NAME, "sub") + "By commit and by day} \n"
    latex_repo += latex_start_graph()
    latex_repo += developer_graph(get_base_file_name(FILE_NAME), commit_package_average, "packages", 0, "Commit", "", param_caption=GRAPH_CAPTION.format(period="Commit", component="packages"), max_x_axis=math.ceil(max(commit_package_average)), max_y_axis=MAX_Y_AXIS)
    latex_repo += developer_graph(get_base_file_name(FILE_NAME), daily_package_average, "packages", 0, "Daily", "", param_caption=GRAPH_CAPTION.format(period="Daily", component="packages"), max_x_axis=math.ceil(max(commit_package_average)), max_y_axis=MAX_Y_AXIS, bins=math.ceil(BINS*(max(daily_package_average)/max(commit_package_average))))
    latex_repo += developer_graph(get_base_file_name(FILE_NAME), commit_class_average, "classes", 0, "Commit", "", param_caption=GRAPH_CAPTION.format(period="Commit", component="classes"), max_x_axis=math.ceil(max(commit_class_average)), max_y_axis=MAX_Y_AXIS)
    latex_repo += developer_graph(get_base_file_name(FILE_NAME), daily_class_average, "classes", 0, "Daily", "", param_caption=GRAPH_CAPTION.format(period="Daily", component="classes"), max_x_axis=math.ceil(max(commit_class_average)), max_y_axis=MAX_Y_AXIS, bins=math.ceil(BINS*(max(daily_class_average)/max(commit_class_average))))
    latex_repo += developer_graph(get_base_file_name(FILE_NAME), commit_method_average, "methods", 0, "Commit", "", param_caption=GRAPH_CAPTION.format(period="Commit", component="methods"), max_x_axis=math.ceil(max(commit_method_average)), max_y_axis=MAX_Y_AXIS)
    latex_repo += developer_graph(get_base_file_name(FILE_NAME), daily_method_average, "methods", 0, "Daily", "", param_caption=GRAPH_CAPTION.format(period="Daily", component="methods"), max_x_axis=max(commit_method_average), max_y_axis=MAX_Y_AXIS, bins=math.ceil(BINS*(max(daily_method_average)/max(commit_method_average))))
    latex_repo += "    \\caption{" + FIGURE_CAPTION.format(num=len(commit_method_average), number_of_repository_word=word_engine.number_to_words(number_of_repository), number_of_repository=number_of_repository) +"} \n"
    latex_repo += latex_end_graph()
    read_write_file.write_file(get_file_name(FILE_NAME), latex_repo, DIRECTORY)

def generate_and_save(number_of_repository):
    generate_average(number_of_repository)
    latex = "\\input{repository/" + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY) 