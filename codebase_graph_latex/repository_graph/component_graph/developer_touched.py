from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

FILE_NAME = __name__    
BASE_FILE_NAME = "repository_1.tex"
KNOWLEDGE_COLOUR = "Blue"
COMMIT_COLOUR = "Orange"
GRAPH_CAPTION = "Repository: {repo} Developer {id}: Developer touched {comp_number} {component} after {commit} commits. "
FIGURE_CAPTION = "Number of days in the developers first year (x-axis) against {component} touched by " + SUSTAINED_JOINER 
FIGURE_CAPTION += " developers (y-axis). " + SUSTAINED_JOINER_DESC
FIGURE_CAPTION_SUFFIX = "\\begin{itemize} "
FIGURE_CAPTION_SUFFIX += "\\item \\color{" + KNOWLEDGE_COLOUR + "}" + KNOWLEDGE_COLOUR + " - Touched components on left y-axis. "
FIGURE_CAPTION_SUFFIX += "\\item \\color{" + COMMIT_COLOUR + "}" + COMMIT_COLOUR + " - Commits on right y-axis. "
FIGURE_CAPTION_SUFFIX += "\\end{itemize} "

def generate_developer_graph(developers, repository_id, component, y_axis, developer_total_commit, max_total_known):
    path = "repository/" + str(repository_id) + "/" + component + "/"
    path_created = False
    latex_repo =  get_section_start(FILE_NAME, "sub") + "Repository " + str(repository_id) + ": Developer " + component +" knowledge} \n"
    latex_repo += latex_start_graph()
    file_name = path
    for key, developer in developers.items():
        x_points = developer[YEAR_PERIOD]
        y_points = developer[y_axis]
        fig, ax = plt.subplots()
        ax.plot(x_points, y_points, c=KNOWLEDGE_COLOUR)
        ax.set_xlim(1, 365)
        ax.set_ylim(0, max_total_known + 1)
        ax.set_xlabel('Number of days')
        ax.set_ylabel(component + " touched")

        y_points_number_of_commits = developer[NUMBER_OF_COMMIT]
        ax2 = ax.twinx()
        ax2.set_ylim(1, developer_total_commit + 1)
        ax2.plot(x_points, y_points_number_of_commits, c=COMMIT_COLOUR)
        
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax2.set_ylabel('Number of Commits')
        if not path_created:
            read_write_file.create_directory(path)
            path_created = True
        file_name = path + str(key) + "." + get_base_file_name(FILE_NAME)  + ".pdf"
        plt.savefig(file_name)
        plt.close()
        caption = GRAPH_CAPTION.format(repo=repository_id, id=key, component=component, commit=len(y_points_number_of_commits), comp_number=y_points[-1])
        latex_repo += latex_add_sub_graph(file_name, caption)
    plt.close()
    latex_repo += "\\caption[Short]{"
    latex_repo += "\\begin{minipage}[t]{\\linewidth}" 
    latex_repo += FIGURE_CAPTION.format(component=component) + FIGURE_CAPTION_SUFFIX
    latex_repo += "\\end{minipage}"
    latex_repo += "} \n"
    latex_repo += latex_end_graph()
    return latex_repo

def generate_and_save(developers, repository_id, module, y_axis, developer_total_commit, max_total_known):
    path = "repository/" + str(repository_id) + "/" + module + "/"
    latex = generate_developer_graph(developers, repository_id, module, y_axis,  developer_total_commit, max_total_known)
    read_write_file.write_file(get_file_name(FILE_NAME), latex, path)
    latex = "\\input{" + path + get_base_file_name(FILE_NAME) + "}\n"
    read_write_file.append_to_file(BASE_FILE_NAME, latex, DIRECTORY)