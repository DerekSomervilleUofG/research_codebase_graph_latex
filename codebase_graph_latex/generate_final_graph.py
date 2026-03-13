from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import generate_and_save as scatter_sample_commit_knowledge_generate_and_save
from codebase_graph_latex.repository_graph.average_components_touched_by_developer import generate_and_save as average_components_touched_by_developer_generate_and_save
from codebase_graph_latex.repository_graph.total_commits_by_developer import generate_and_save as developer_commit_generate_and_save
from codebase_graph_latex.repository_graph.histogram_components_touched_by_developer import generate_and_save as repository_histogram_commit_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import generate_and_save as time_series_components_touched_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.anova_generate import generate_and_save  as anova_generate_and_save 
from codebase_graph_latex.repository_graph.component_time_series.welch_t_test import generate_and_save  as welch_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.strategy_logistic_regression import generate_and_save  as strategy_generate_and_save
from codebase_graph_latex.constants import *
from codebase_graph_latex.store_developer_data import *
from codebase_graph_latex.developer_data import *

NUMBER_OF_COMMITS = 10

def filter_developer_commits(developers, number_of_commits):
    filtered_developers = {}
    category_developers = {}
    new_developer = []
    for category in DEVELOPER_CATEGORY:
        category_developers = {}
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

def generate_and_save(number_of_repositories):
    scatter_sample_commit_knowledge_generate_and_save()
    developer_commit_generate_and_save(number_of_repositories)
    repository_histogram_commit_generate_and_save(number_of_repositories)
    #average_components_touched_by_developer_generate_and_save(number_of_repositories)
    for component in COMPONENTS:
        developers = {}
        for category in DEVELOPER_CATEGORY:
            developers[category] = developer_component_knowledge[category][component]
        filtered_developers = developers
        for unit in [0, 10, 20, 50]:
            if unit > 0:
                filtered_developers = filter_developer_commits(developers, unit)
            time_series_components_touched_generate_and_save(0, component, filtered_developers, REPOSITORY_SUMMARY_1_FILE, unit)
            welch_generate_and_save(component, filtered_developers, unit)
            anova_generate_and_save(component, filtered_developers, unit)
            strategy_generate_and_save(component, filtered_developers, unit)