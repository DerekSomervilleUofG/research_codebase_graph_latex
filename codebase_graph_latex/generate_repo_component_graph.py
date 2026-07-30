from codebase_graph_latex.repository_graph.sample_scatter_touched_against_commit import repository_generate_and_save as scatter_sample_commit_knowledge_repository_generate_and_save
from codebase_graph_latex.repository_graph.average_components_touched_by_developer import merge_average as repository_average_knowledge_merge_average
from codebase_graph_latex.repository_graph.component_graph.time_series_sustained_components_touched_by_developer import generate_and_save as timeseries_components_touched_by_developer_generate_and_save
from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import generate_and_save as time_series_components_touched_generate_and_save
from codebase_graph_latex.repository_graph.histogram_components_touched_by_developer import get_commit_and_daily
from codebase_graph_latex.constants import *

def generate_and_save(repository_id, status, component, developers):
    daily_data = get_commit_and_daily(developers[SUSTAINED_JOINER], "daily")
    commit_data = get_commit_and_daily(developers[SUSTAINED_JOINER], "commit")
    repository_average_knowledge_merge_average(daily_data, commit_data, component)
    if status == "B":
        #time_series_components_touched_generate_and_save(repository_id, component, developers)
        scatter_sample_commit_knowledge_repository_generate_and_save(repository_id, component, developers)        
        timeseries_components_touched_by_developer_generate_and_save(repository_id, component, developers[SUSTAINED_FOUNDER], developers[SUSTAINED_JOINER], NUMBER_OF_COMMIT, COMPONENT_TOUCHED)
        timeseries_components_touched_by_developer_generate_and_save(repository_id, component, developers[SUSTAINED_FOUNDER], developers[SUSTAINED_JOINER], YEAR_PERIOD, COMPONENT_TOUCHED)
        timeseries_components_touched_by_developer_generate_and_save(repository_id, component, developers[SUSTAINED_FOUNDER], developers[SUSTAINED_JOINER], NUMBER_OF_COMMIT, COMPONENT_RATIO)
        timeseries_components_touched_by_developer_generate_and_save(repository_id, component, developers[SUSTAINED_FOUNDER], developers[SUSTAINED_JOINER], YEAR_PERIOD, COMPONENT_RATIO)
