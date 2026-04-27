from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import generate_and_save as scatter_sample_commit_knowledge_generate_and_save
from codebase_graph_latex.repository_graph.average_components_touched_by_developer import generate_and_save as average_components_touched_by_developer_generate_and_save
from codebase_graph_latex.repository_graph.total_commits_by_developer import generate_and_save as developer_commit_generate_and_save
from codebase_graph_latex.repository_graph.histogram_components_touched_by_developer import generate_and_save as repository_histogram_commit_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import generate_and_save as time_series_components_touched_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.anova_generate import generate_and_save  as anova_generate_and_save 
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import generate_and_save  as welch_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import section_sub_heading  as welch_section_sub_heading
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import FILE_NAME  as welch_file_name
from codebase_graph_latex.repository_graph.component_time_series.tukey_hsd import generate_and_save  as tukey_hsd_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.strategy_logistic_regression import generate_and_save  as strategy_generate_and_save
from codebase_graph_latex.constants import *
from codebase_graph_latex.store_developer_data import *
from codebase_graph_latex.developer_data import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

NUMBER_OF_COMMITS = 10
BASE_FILE_NAME = "repository_summary_1.tex"

def filter_developer_commits(developers, number_of_commits):
    filtered_developers = {}
    category_developers = {}
    new_developer = []
    for category in DEVELOPER_CATEGORY:
        category_developers = {}
        if category in developers.keys():
            for key, developer in developers[category].items():
                new_developer = []
                for item in developer:
                    if isinstance(item, list):
                        item = item.copy()
                        new_developer.append(item[:number_of_commits])
                    else:
                        new_developer.append(item)
                category_developers[key] = new_developer
            filtered_developers[category] = category_developers
    return filtered_developers

def generate_welch_file_name(file_name, sample_a_b):
    return file_name + "_" + sample_a_b[0] + "_" + sample_a_b[1]

def welch_end_table(base_file_name, samples):
    for sample in samples:
        file_name = generate_welch_file_name(base_file_name, sample)
        read_write_file.append_to_file(file_name + ".tex", table_end(), DIRECTORY)

def generate_welch_t_test(component, filtered_developers, number_of_commits):
    file_name = get_base_file_name(welch_file_name)
    latex = welch_section_sub_heading("all commits")
    samples = [[FOUNDER, JOINER], 
               [MODERATE, SUSTAINED],
               [MODERATE + " " + FOUNDER, MODERATE + " later " + JOINER],
               [SUSTAINED + " " + FOUNDER, SUSTAINED + " later " + JOINER]]
    if len(filtered_developers.keys()) == 2:
        if component == "methods":
            samples.pop()
            welch_end_table(file_name, samples)
        samples = [[SUSTAINED + " " + FOUNDER, SUSTAINED + " later " + JOINER]]
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        save_to_latex_file(file_name, BASE_FILE_NAME, latex, DIRECTORY)
        for sample in samples:
            save_to_latex_file(generate_welch_file_name(file_name, sample),file_name + ".tex", "", DIRECTORY)
    for sample in samples:
        welch_generate_and_save(component, filtered_developers, number_of_commits, sample, generate_welch_file_name(file_name, sample))

def generate_and_save(number_of_repositories):
    scatter_sample_commit_knowledge_generate_and_save()
    developer_commit_generate_and_save(number_of_repositories)
    repository_histogram_commit_generate_and_save(number_of_repositories)
    #average_components_touched_by_developer_generate_and_save(number_of_repositories)
    for component in COMPONENTS:
        developers = {}
        sustained_developers = {}
        for category in DEVELOPER_CATEGORY:
            if TRANSIENT not in category:
                developers[category] = developer_component_knowledge[category][component]
            if SUSTAINED in category:
                sustained_developers[category] = developer_component_knowledge[category][component]
        for number_of_commits in [5, 10, 20, 0]:
            if number_of_commits > 0 and number_of_commits <= 10:
                filtered_developers = filter_developer_commits(developers, number_of_commits)
            elif number_of_commits == 20:
                filtered_developers = filter_developer_commits(sustained_developers, number_of_commits)    
            elif number_of_commits == 0:
                filtered_developers = sustained_developers 
            time_series_components_touched_generate_and_save(0, component, filtered_developers, number_of_commits)
            if number_of_commits > 0:
                generate_welch_t_test(component, filtered_developers, number_of_commits)
                if number_of_commits <= 10:
                    anova_generate_and_save(component, filtered_developers, number_of_commits)
                if component != "packages":
                    tukey_hsd_generate_and_save(component, filtered_developers, number_of_commits)
                strategy_generate_and_save(component, filtered_developers, number_of_commits)