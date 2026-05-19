from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import generate_and_save as scatter_sample_commit_knowledge_generate_and_save
from codebase_graph_latex.repository_graph.average_components_touched_by_developer import generate_and_save as average_components_touched_by_developer_generate_and_save
from codebase_graph_latex.repository_graph.total_commits_by_developer import generate_and_save as developer_commit_generate_and_save
from codebase_graph_latex.repository_graph.histogram_components_touched_by_developer import generate_and_save as repository_histogram_commit_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import generate_and_save as time_series_components_touched_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.anova_generate import generate_and_save  as anova_generate_and_save 
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import generate_and_save  as welch_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import section_sub_heading  as welch_section_sub_heading
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import FILE_NAME  as welch_file_name
from codebase_graph_latex.repository_graph.component_time_series.normality_homoscedasticity import section_sub_heading  as normal_section_sub_heading
from codebase_graph_latex.repository_graph.component_time_series.normality_homoscedasticity import FILE_NAME  as normal_file_name
from codebase_graph_latex.repository_graph.component_time_series.tukey_hsd import generate_and_save  as tukey_hsd_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.tukey_hsd import FILE_NAME  as tukey_hsd_file_name
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import FILE_NAME  as time_series_file_name
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

def generate_welch_t_test(component, filtered_developers, number_of_commits):
    file_name = get_base_file_name(welch_file_name)
    normal_base_file_name = get_base_file_name(normal_file_name)
    sub_file_name = file_name
    latex = welch_section_sub_heading("all commits")
    normal_latex = normal_section_sub_heading("all commits")
    samples = [ [FOUNDER, JOINER], 
                [MODERATE + " " + FOUNDER, MODERATE + " later " + JOINER],
                [SUSTAINED + " " + FOUNDER, SUSTAINED + " later " + JOINER],
                [TRANSIENT, MODERATE],
                [TRANSIENT, SUSTAINED],
                [TRANSIENT, [MODERATE, SUSTAINED]],
                [MODERATE, SUSTAINED]]
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        save_to_latex_file(normal_base_file_name, BASE_FILE_NAME, normal_latex, DIRECTORY)
        save_to_latex_file(file_name, BASE_FILE_NAME, latex, DIRECTORY)
    for sample in samples:
        if sample[0] in [FOUNDER] or sample[1] in [MODERATE]:
            sub_file_name = generate_welch_file_name(file_name, sample)
            normal_sub_file_name = generate_welch_file_name(normal_base_file_name, sample)
        if (sample[0] in [FOUNDER] or sample[1] in [MODERATE]) and component == "packages" and number_of_commits == START_COMMIT_NUMBER:
            save_to_latex_file(sub_file_name, file_name + ".tex", "", DIRECTORY)
            save_to_latex_file(normal_sub_file_name,normal_base_file_name + ".tex", "", DIRECTORY)
        if (sample[0] in [TRANSIENT] and number_of_commits == START_COMMIT_NUMBER) or sample[0] not in [TRANSIENT]:
            welch_generate_and_save(component, filtered_developers, number_of_commits, sample, sub_file_name, normal_sub_file_name)

def generate_tukey_hsd(component, filtered_developers, number_of_commits):
    if component == "packages" and number_of_commits == START_COMMIT_NUMBER:
        base_file_name = get_base_file_name(tukey_hsd_file_name)
        save_to_latex_file(base_file_name, BASE_FILE_NAME, "", DIRECTORY)
    elif component != "packages":
        tukey_hsd_generate_and_save(component, filtered_developers, number_of_commits)

def generate_time_series(component, filtered_developers, number_of_commits):
    file_name = get_base_file_name(time_series_file_name)
    if component == "packages" and number_of_commits == 1:
        save_to_latex_file(file_name, BASE_FILE_NAME, "", DIRECTORY)
    if number_of_commits != 1:
        time_series_components_touched_generate_and_save(0, component, filtered_developers, number_of_commits)

def generate_and_save(number_of_repositories):
    scatter_sample_commit_knowledge_generate_and_save()
    developer_commit_generate_and_save(number_of_repositories)
    repository_histogram_commit_generate_and_save(number_of_repositories)
    for component in COMPONENTS:
        all_developers = {}
        developers = {}
        sustained_developers = {}
        for category in DEVELOPER_CATEGORY:
            all_developers[category] = developer_component_knowledge[category][component]
            if TRANSIENT not in category:
                developers[category] = developer_component_knowledge[category][component]
            if SUSTAINED in category:
                sustained_developers[category] = developer_component_knowledge[category][component]
        for number_of_commits in [1, 5, 10, 20, 0]:
            if number_of_commits == 1:
                filtered_developers = filter_developer_commits(all_developers, number_of_commits)
            elif number_of_commits > 0 and number_of_commits <= 10:
                filtered_developers = filter_developer_commits(developers, number_of_commits)
            elif number_of_commits == 20:
                filtered_developers = filter_developer_commits(sustained_developers, number_of_commits)    
            elif number_of_commits == 0:
                filtered_developers = sustained_developers 

            generate_time_series(component, filtered_developers, number_of_commits)
            if number_of_commits > 0:
                generate_welch_t_test(component, filtered_developers, number_of_commits)
                if number_of_commits <= 10:
                    anova_generate_and_save(component, filtered_developers, number_of_commits)
                generate_tukey_hsd(component, filtered_developers, number_of_commits)
                strategy_generate_and_save(component, filtered_developers, number_of_commits)
