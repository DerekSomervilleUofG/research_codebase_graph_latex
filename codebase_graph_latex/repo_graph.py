import matplotlib.pyplot as plt
from codebase_graph_latex.store_developer_data import merge_knowledge as store_developer_data_merge_knowledge
from codebase_graph_latex.repository_summary import generate_and_save as repository_summary_table_generate_and_save
from codebase_graph_latex.generate_final_graph import generate_and_save as generate_final_graph_generate_and_save
from codebase_graph_latex.generate_repo_component_graph import generate_and_save as generate_repo_component_graph_generate_and_save
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.select.select_repository import *
from codebase_graph_latex.glossary import generate_glossary
from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.calculate import *
from codebase_graph_latex.developer_data import get_data_from_database
from utility.ReadWriteFile import ReadWriteFile
from utility.DictUtility import DictUtility

read_write_file = ReadWriteFile()
repo_contribution = {}
CORE_LIMIT = 0.80

def create_repository_directory(repository_id, component):
    path = DIRECTORY + str(repository_id) + "/" + component + "/"
    read_write_file.create_directory(path)

def mark_core_contributors(developers_dict, total_commits):
    sorted_devs = sorted(
        developers_dict.items(), 
        key=lambda item: item[1][3][-1], 
        reverse=True
    )
    
    # 2. Calculate the 80% threshold target
    threshold_target = total_commits * 0.80
    running_commits = 0
    
    # 3. Iterate through the sorted developers and update the original dictionary rows
    for name, row in sorted_devs:
        latest_commits = row[3][-1]
        
        # If we haven't crossed the 80% cumulative threshold yet, they are a core contributor
        if running_commits < threshold_target and latest_commits > 0:
            developers_dict[name][-1] = 1  # Set last column to 1 (Core)
            running_commits += latest_commits
        else:
            developers_dict[name][-1] = 0

def get_developers(repository_id, component):
    global developer_total_commit, max_total_known
    founder_developers, developer_total_commit, max_total_known = get_data_from_database(repository_id, component, FOUNDER)
    founder_total_commits = developer_total_commit
    sustained_founder_developers = filter_developers(founder_developers)
    transient_founder_developers = DictUtility.dict_remove_items(founder_developers, sustained_founder_developers)
    moderate_founder_developers = filter_developers_by_commits(transient_founder_developers, TRANSIENT_COMMITS)
    transient_founder_developers = DictUtility.dict_remove_items(transient_founder_developers, moderate_founder_developers)
    joiner_developers, developer_total_commit, max_total_known  = get_data_from_database(repository_id, component, JOINER)
    mark_core_contributors(founder_developers, founder_total_commits + developer_total_commit )
    mark_core_contributors(joiner_developers, founder_total_commits + developer_total_commit )
    sustained_joiner_developers = filter_developers(joiner_developers)
    transient_joiner_developers = DictUtility.dict_remove_items(joiner_developers, sustained_joiner_developers)
    moderate_joiner = filter_developers_by_commits(transient_joiner_developers, TRANSIENT_COMMITS)
    transient_joiner_developers = DictUtility.dict_remove_items(transient_joiner_developers, moderate_joiner)   
    repo_contribution[repository_id] = {}
    repo_contribution[repository_id][SUSTAINED_JOINER] = len(sustained_joiner_developers.values())
    repo_contribution[repository_id][SUSTAINED_FOUNDER] = len(sustained_founder_developers.values())
    repo_contribution[repository_id][MODERATE_FOUNDER] = len(moderate_founder_developers.values())
    repo_contribution[repository_id][MODERATE_JOINER] = len(moderate_joiner.values())
    repo_contribution[repository_id][TRANSIENT_FOUNDER] = len(transient_founder_developers.values())
    repo_contribution[repository_id][TRANSIENT_JOINER] = len(transient_joiner_developers.values())
    developers = {}
    developers[SUSTAINED_JOINER] = sustained_joiner_developers
    developers[SUSTAINED_FOUNDER] = sustained_founder_developers
    developers[MODERATE_FOUNDER] = moderate_founder_developers
    developers[MODERATE_JOINER] = moderate_joiner
    developers[TRANSIENT_FOUNDER] = transient_founder_developers
    developers[TRANSIENT_JOINER] = transient_joiner_developers
    return developers

def create_repo_latex_file(repository_id, status):
    path = DIRECTORY + str(repository_id) + "/" 
    read_write_file.create_directory(path)
    latex_start_repo = "\\subsection{Repository: " + str(repository_id)  + "} \n"
    read_write_file.append_to_file("repository_1.tex", latex_start_repo, DIRECTORY)
    

def run(repository_id, status):
    print("Run for ", repository_id, status)
    if status == "B":
        create_repo_latex_file(repository_id, status)
    for component in [ "packages", "classes", "methods"]:
        developers = get_developers(repository_id, component)
        store_developer_data_merge_knowledge(component, developers)
        if len(developers[SUSTAINED_JOINER].keys()) >= MINIMUM_NUMBER_OF_COMMTIS:
            if status == "B":
                create_repository_directory(repository_id, component)
            generate_repo_component_graph_generate_and_save(repository_id, status, component, developers)
            

def latex_repository():
    file_suffix = ["_1.tex"]
    base_summary_file_name = "repository_summary"
    base_file_name = "repository"
    appendix_file_name = "appendix"
    for suffix in file_suffix:    
        read_write_file.write_file(base_summary_file_name + suffix, "", DIRECTORY)
        generate_glossary(base_summary_file_name + suffix)
        read_write_file.write_file(base_file_name + suffix, "", DIRECTORY) 
        read_write_file.write_file(appendix_file_name + suffix, "\\begin{appendices}\n%%\\chapter{Supplementary Statistical Results}\n", DIRECTORY) 

def start_generate_repo_latex(control_populate):
    initialise_populate_table(control_populate)
    latex_repository()

def finish_repo_latex():
    number_of_repositories = repository_summary_table_generate_and_save(repo_contribution)
    generate_final_graph_generate_and_save(number_of_repositories)
    read_write_file.append_to_file("appendix_1.tex", "\\end{appendices}\n", DIRECTORY) 

def get_repository(repository_id):
    repositories = []
    if repository_id > 0:
        repositories.append([repository_id, "B"])
    else:
        repositories = get_all_data(query())
    return repositories


def generate_repo_latex(control_populate, repository_id=0):
    start_generate_repo_latex(control_populate)
    repositories = get_repository(repository_id)
    latex_start_repo = "\\section{{Repository}} \n"
    read_write_file.append_to_file("repository_1.tex", latex_start_repo, DIRECTORY)
    for repository in repositories:
        run(repository[REPOSITORY_ID], repository[STATUS])
    finish_repo_latex()