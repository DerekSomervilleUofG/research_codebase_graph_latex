from codebase_graph_latex.constants import *
from codebase_graph_latex.developer_data import get_data_from_database
from codebase_graph_latex.repo_graph import get_repository
from codebase_graph_latex.repo_graph import get_developers
from codebase_graph_latex.repo_graph import start_generate_repo_latex
from codebase_graph_latex.select.select_repository import *
from utility.ReadWriteFile import ReadWriteFile
from utility.DictUtility import DictUtility

read_write_file = ReadWriteFile()

def run(repository_id):
    print("Run for ", repository_id)
    for component in [ "packages", "classes", "methods"]:
        developers = get_developers(repository_id, component)
        read_write_file.write_file("data_" + str(repository_id) + "_" + TRANSIENT_FOUNDER + "_" + component + ".csv", DictUtility.dict_format(developers[TRANSIENT_FOUNDER]), DIRECTORY)           
        read_write_file.write_file("data_" + str(repository_id) + "_" + SUSTAINED_FOUNDER + "_" + component + ".csv", DictUtility.dict_format(developers[SUSTAINED_FOUNDER]), DIRECTORY)        
        read_write_file.write_file("data_" + str(repository_id) + "_" + TRANSIENT_JOINER + "_" + component + ".csv", DictUtility.dict_format(developers[TRANSIENT_JOINER]), DIRECTORY)        
        read_write_file.write_file("data_" + str(repository_id) + "_" + SUSTAINED_JOINER + "_" + component + ".csv", DictUtility.dict_format(developers[SUSTAINED_JOINER]), DIRECTORY)   

def main(control_populate, repository_id):   
    start_generate_repo_latex(control_populate)
    repositories = get_repository(repository_id)
    for repository in repositories:
        run(repository[REPOSITORY_ID])