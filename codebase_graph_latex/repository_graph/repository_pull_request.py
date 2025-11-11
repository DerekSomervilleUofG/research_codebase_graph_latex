from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.select.select_repositpory_pull_request import *
import matplotlib.pyplot as plt

FILE_NAME = __name__
BASE_FILE_NAME = "appendix_2.tex"
GRAPH_CAPTION = "Average number of pull request for {number} developers."

pull_requests = {}
    
def get_pull_requests(repository_id):
    global pull_requests
    local_pull_requests = {}
    for exp in get_all_data(query(repository_id)):
        local_pull_requests[exp[DEVELOPER_ID]] = exp[COUNT]
    pull_requests.update(local_pull_requests)
    return pull_requests

def generate_pull_request_graph(repository_id):
    sub_level = ""
    if repository_id > 0:
        sub_level = "sub"
    latex_repo = get_section_start(FILE_NAME, sub_level)
    if repository_id > 0:
        local_pull_requests = get_pull_requests(repository_id)
        latex_repo +=  "Repository " + str(repository_id) + " "
    else:
        local_pull_requests = pull_requests
    latex_repo += "Pull requests " + "} \n"
    latex_repo += developer_graph(FILE_NAME, local_pull_requests.values(), "pull requests", repository_id, "", "", GRAPH_CAPTION.format(number=len(local_pull_requests.values())), sub_graph=False) 
    return latex_repo, pull_requests

def generate_and_save(repository_id):
    path = DIRECTORY + "appendix/"
    read_write_file.create_directory(path)
    latex, pull_requests = generate_pull_request_graph(repository_id)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)
    return pull_requests