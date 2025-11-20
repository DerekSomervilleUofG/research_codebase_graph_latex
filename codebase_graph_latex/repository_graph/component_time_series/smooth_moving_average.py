from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import *
import seaborn as sns
import plotly.express as px

FILE_NAME = __name__
FIGURE_CAPTION = "A smooth moving of total {component} touched on average each {unit} of a year. "

BASE_FILE_NAME = "appendix_2.tex"

def section_sub_heading(repository_id, component):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For " + component + " touched for each unit} \n"
    latex += "A smooth moving average " + component + " touched on average each period "
    latex += "the number of commits to components touched. \n"
    return latex

def generate_graph(path, component, data, type, unit=NUMBER_OF_MONTHS):
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)

    mean_touched = np.mean(data, axis=0)
    data_frame = pd.DataFrame({'month': np.arange(1, unit + 1), 'mean': mean_touched})
    
    data_frame['smoothed'] = data_frame['mean'].rolling(window=3, center=True).mean()
    

    plt.plot(data_frame['month'], data_frame['mean'], color='blue', label='Mean')
    plt.plot(data_frame['month'], data_frame['smoothed'], color='orange', linestyle='--', label='Smoothed (Moving Avg)')

    
    file_name = path + get_base_file_name(FILE_NAME) + "." + type.lower().replace(" ",".") + "." + UNIT_FREQUENCY[unit].lower() + ".pdf"
    plt.savefig(file_name, bbox_inches='tight')
    return file_name

def generate_and_save(repository_id, component, developers):
    if component == "packages":
        path = "repository/" + str(repository_id) + "/" 
        read_write_file.write_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component), path)
    default_generate_save(generate_graph, BASE_FILE_NAME, FILE_NAME, repository_id, component, developers, figure_caption=FIGURE_CAPTION)