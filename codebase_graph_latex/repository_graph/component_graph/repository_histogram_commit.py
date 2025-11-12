from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *

FILE_NAME = __name__
BASE_FILE_NAME = "repository_1.tex"
GRAPH_CAPTION = "By {freq}."

FIGURE_CAPTION = "Histogram of new {component} touched (x-axis) against number of developers (y-axis)." \
    " Graphs for {number} {group}" 


def generate_summary_histogram(commit_data, daily_data, repository_id, path, component):
    latex_repo = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For " + component + " with total } \n"
    latex_repo += "\n"
    read_write_file.create_directory(path)
    latex_repo += latex_start_graph()
    latex_repo += developer_graph(FILE_NAME, daily_data, component, repository_id, "Day", "", GRAPH_CAPTION.format(freq="Day")) 
    latex_repo += developer_graph(FILE_NAME, commit_data, component, repository_id, "Commit", "", GRAPH_CAPTION.format(freq="Commit")) 
    latex_repo += "  \\caption{" + FIGURE_CAPTION.format(component=component, group=SUSTAINED_JOINER_DESC.lower(), number=str(len(daily_data))) + "} \n"
    latex_repo += latex_end_graph()
    return latex_repo

def generate_and_save(commit_data, daily_data, repository_id, component):
    path = "repository/" + str(repository_id) + "/" + component + "/"
    latex = generate_summary_histogram(commit_data, daily_data, repository_id, path, component)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
