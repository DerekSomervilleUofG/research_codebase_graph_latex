from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import *
import seaborn as sns

FILE_NAME = __name__
FIGURE_CAPTION = "Repository: {repo}. A box plot of total {component} touched on mean each month, with quartile shading. "

BASE_FILE_NAME = "repository_2.tex"

def section_sub_heading(repository_id, component):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) + " For " + component + " touched for each period} \n"
    latex += "A box plot of " + component + " touched on average each period "
    latex += "the number of commits to components touched. \n"
    return latex


def developer_mean_data(data, unit):
    median_data = [0] * unit
    for developer_data in data:
        for i in range(unit):
            median_data[i] += developer_data[i]
    for i in range(unit):
        median_data[i] = median_data[i] / len(data)
    return median_data


def generate_graph(path, component, data, type, unit, y_axis_max):
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    period = list(range(1, unit + 1))
    period_list = period * len(data)
    touched = [val for dev in data for val in dev   ]
    data_frame = {
        'Period': period_list,
        'Touched': touched
    }
    data_frame = pd.DataFrame(data_frame)
    p1 = sns.boxplot(x='Period', y='Touched', data=data_frame, showfliers=False, patch_artist=True)

    plt.xticks(get_x_axis_unit(unit))
    plt.yticks(np.arange(0, y_axis_max + 1))
    plt.xlabel(UNIT_FREQUENCY[unit])
    plt.ylabel(component.capitalize() + " touched")
    plt.tight_layout() 
    file_name = path + get_base_file_name(FILE_NAME) + "." + type.lower().replace(" ",".") + "." + component + "." + str(unit) + ".pdf"
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    return file_name

def generate_and_save(repository_id, component, developers):
    if component == "packages":
        path = "repository/" + str(repository_id) + "/" 
        read_write_file.write_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component), path)
    default_generate_save(generate_graph, BASE_FILE_NAME, FILE_NAME, repository_id, component, developers, units=[NUMBER_OF_WEEKS], figure_caption=FIGURE_CAPTION)