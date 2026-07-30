from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import generate_and_save as scatter_sample_commit_knowledge_generate_and_save
from codebase_graph_latex.repository_graph.average_components_touched_by_developer import generate_and_save as average_components_touched_by_developer_generate_and_save
from codebase_graph_latex.repository_graph.total_commits_by_developer import generate_and_save as developer_commit_generate_and_save
from codebase_graph_latex.repository_graph.histogram_components_touched_by_developer import generate_and_save as repository_histogram_commit_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import generate_and_save as time_series_components_touched_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import FILE_NAME  as time_series_file_name
from codebase_graph_latex.repository_graph.component_time_series.ART_anova import generate_and_save  as art_anova_generate_and_save 
from codebase_graph_latex.repository_graph.component_time_series.ART_anova import FILE_NAME  as art_anova_file_name
from codebase_graph_latex.repository_graph.component_time_series.standard_anova import generate_and_save  as standard_anova_generate_and_save 
from codebase_graph_latex.repository_graph.component_time_series.standard_anova import FILE_NAME  as standard_anova_file_name
from codebase_graph_latex.repository_graph.component_time_series.statistical_significance_test import generate_and_save  as statistical_significance_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.statistical_significance_test import section_heading  as statistical_significance_section_sub_heading
from codebase_graph_latex.repository_graph.component_time_series.statistical_significance_test import FILE_NAME  as statistical_significance_file_name
from codebase_graph_latex.repository_graph.component_time_series.statistical_significance_test import set_previous
from codebase_graph_latex.repository_graph.component_time_series.normality_and_variance import section_sub_heading  as normal_section_sub_heading
from codebase_graph_latex.repository_graph.component_time_series.normality_and_variance import FILE_NAME  as normal_file_name
from codebase_graph_latex.repository_graph.component_time_series.tukey_hsd import generate_and_save  as tukey_hsd_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.tukey_hsd import FILE_NAME  as tukey_hsd_file_name
from codebase_graph_latex.repository_graph.component_time_series.holm_bonferroni import generate_and_save  as holm_bonferroni_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.holm_bonferroni import FILE_NAME  as holm_bonferroni_file_name
from codebase_graph_latex.repository_graph.component_time_series.strategy_logistic_regression import generate_and_save  as strategy_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.breadth_or_depth import generate_and_save_ratio_analysis
from codebase_graph_latex.constants import *
from codebase_graph_latex.store_developer_data import *
from codebase_graph_latex.developer_data import *
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.latex_table import *

NUMBER_OF_COMMITS = 10
BASE_FILE_NAME = "repository_summary_1.tex"
APPENDIX = "appendix_1.tex"

def filter_developer_commits(developers, number_of_commits):
    filtered_developers = {}
    category_developers = {}
    new_developer = []
    for category in DEVELOPER_CATEGORY:
        category_developers = {}
        if category in developers.keys():
            for key, developer in developers[category].items():
                if len(developer[KNOWN_Y_AXIS]) >= number_of_commits:
                    new_developer = []
                    for item in developer:
                        if isinstance(item, list) and len(item) >= number_of_commits:
                            new_developer.append(item[:number_of_commits].copy())
                        else:
                            new_developer.append(item)
                    if len(new_developer) > 0:
                        category_developers[key] = new_developer
            filtered_developers[category] = category_developers
    return filtered_developers

def generate_statistical_significance_file_name(file_name, sample_a_b):
    return file_name + "_" + sample_a_b[0] + "_" + sample_a_b[1]

def generate_statistical_significance_test(component, filtered_developers, number_of_commits):
    file_name = get_base_file_name(statistical_significance_file_name)
    normal_base_file_name = get_base_file_name(normal_file_name)
    graph_file_name = normal_base_file_name + "_graph"
    samples = [ [FOUNDER, JOINER] 
                ,[MODERATE + " " + FOUNDER, MODERATE + " later " + JOINER]
                ,[SUSTAINED + " " + FOUNDER, SUSTAINED + " later " + JOINER]
                ,[TRANSIENT, MODERATE]
                ,[TRANSIENT, SUSTAINED]
                ,[TRANSIENT, [MODERATE, SUSTAINED]]
                ,[MODERATE, SUSTAINED]
                ,["Core", "Non Core"]
                ]

    for sample in samples:
        if sample[0] in [FOUNDER] or sample[1] in [MODERATE]:
            sub_file_name = generate_statistical_significance_file_name(file_name, sample) + "_" + component
            sub_graph_file_name = generate_statistical_significance_file_name(graph_file_name, sample)
            normal_sub_file_name = generate_statistical_significance_file_name(normal_base_file_name, sample) + "_" + component
        if (sample[0] in [FOUNDER] or sample[1] in [MODERATE]) and number_of_commits == START_COMMIT_NUMBER:
            set_previous()
            set_graph_number(0)
            save_to_latex_file(sub_file_name, file_name + ".tex", "", DIRECTORY)
            save_to_latex_file(normal_sub_file_name, normal_base_file_name + ".tex", "", DIRECTORY)
            read_write_file.write_file(sub_graph_file_name + ".tex", latex_start_graph(), DIRECTORY)
        if (sample[0] in [TRANSIENT] and number_of_commits == START_COMMIT_NUMBER) or sample[0] not in [TRANSIENT]:
            statistical_significance_generate_and_save(component, filtered_developers, number_of_commits, sample, sub_file_name, sub_graph_file_name, normal_sub_file_name)

def generate_tukey_hsd(component, filtered_developers, number_of_commits):
    if component != "packages":
        tukey_hsd_generate_and_save(component, filtered_developers, number_of_commits)

def generate_holm_bonferroni(component, filtered_developers, number_of_commits):
    holm_bonferroni_generate_and_save(component, filtered_developers, number_of_commits)

def generate_time_series(component, filtered_developers, number_of_commits):
    if number_of_commits != 1:
        time_series_components_touched_generate_and_save(0, component, filtered_developers, number_of_commits)

def create_files():
    file_name = get_base_file_name(time_series_file_name)
    save_to_latex_file(file_name, APPENDIX, "", DIRECTORY)
    
    normal_latex = normal_section_sub_heading("all commits")
    normal_base_file_name = get_base_file_name(normal_file_name)
    save_to_latex_file(normal_base_file_name, BASE_FILE_NAME, normal_latex, DIRECTORY)
    latex = statistical_significance_section_sub_heading("all commits")
    stat_file_name = get_base_file_name(statistical_significance_file_name)
    save_to_latex_file(stat_file_name, APPENDIX, latex, DIRECTORY)
    anova_file_name = get_base_file_name(standard_anova_file_name)
    save_to_latex_file(anova_file_name, APPENDIX, "", DIRECTORY)
    tukey_file_name = get_base_file_name(tukey_hsd_file_name)
    save_to_latex_file(tukey_file_name, APPENDIX, "", DIRECTORY)
    file_name = get_base_file_name(art_anova_file_name)
    save_to_latex_file(file_name, BASE_FILE_NAME, "", DIRECTORY)
    holm_bon_file_name = get_base_file_name(holm_bonferroni_file_name)
    save_to_latex_file(holm_bon_file_name, BASE_FILE_NAME, "", DIRECTORY)


def generate_and_save(number_of_repositories):
    developer_commit_generate_and_save(number_of_repositories)
    repository_histogram_commit_generate_and_save(number_of_repositories)
    scatter_sample_commit_knowledge_generate_and_save()
    create_files()
    for component in COMPONENTS:
        all_developers = {}
        five_developers = {}
        developers = {}
        sustained_developers = {}
        for category in DEVELOPER_CATEGORY:
            all_developers[category] = developer_component_knowledge[category][component]
            if TRANSIENT not in category:
                developers[category] = developer_component_knowledge[category][component]
            if SUSTAINED in category:
                sustained_developers[category] = developer_component_knowledge[category][component]
        for number_of_commits in [1, 2, 5, 10, 20, 0]:
            if number_of_commits == 1:
                filtered_developers = filter_developer_commits(all_developers, number_of_commits)
            elif number_of_commits in (2,5):
                filtered_developers = filter_developer_commits(all_developers, number_of_commits)
            elif number_of_commits == 10:
                filtered_developers = filter_developer_commits(developers, number_of_commits)
            elif number_of_commits == 20:
                filtered_developers = filter_developer_commits(sustained_developers, number_of_commits)    
            elif number_of_commits == 0:
                filtered_developers = sustained_developers 
            if number_of_commits in [1, 5, 10, 20, 0]:
                generate_time_series(component, filtered_developers, number_of_commits)
            if number_of_commits > 0:
                generate_statistical_significance_test(component, filtered_developers, number_of_commits)
                if number_of_commits <= 10:
                    standard_anova_generate_and_save(component, filtered_developers, number_of_commits)
                    art_anova_generate_and_save(component, filtered_developers, number_of_commits)
                generate_tukey_hsd(component, filtered_developers, number_of_commits)
                generate_holm_bonferroni(component, filtered_developers, number_of_commits)
                strategy_generate_and_save(component, filtered_developers, number_of_commits, True)
                strategy_generate_and_save(component, filtered_developers, number_of_commits, False)
                if component in ["packages", "methods"]:
                    generate_and_save_ratio_analysis(component, filtered_developers, number_of_commits)
