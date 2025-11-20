from codebase_graph_latex.repository_graph.component_time_series.time_series_components_touched import *
from sklearn.cluster import KMeans
from scipy.stats import pearsonr


FILE_NAME = __name__
FIGURE_CAPTION = "A statistical process control chart for additonal {component} touched each month. "
THRESHOLD = 500

BASE_FILE_NAME = "appendix_2.tex"

def section_sub_heading(repository_id, component):
    latex = get_section_start(FILE_NAME, "sub") + str(repository_id) 
    latex += " For " + component + " touched for each month of a year} \n"
    latex += "A statistical process control chart for " + component + " touched \n"
    return latex


def generate_graph(path, component, data, type, unit=NUMBER_OF_MONTHS):
    plt.figure(figsize=SMALL_FIGURE, dpi=1000)
    data_frame = pd.DataFrame(data)
    df_monthly = data_frame.groupby(MONTH)[TOUCHED].sum().reset_index()
    # Assuming the count of files touched cannot be negative, we ensure it's at least 0 after differencing
    df_monthly[TOUCHED] = df_monthly[TOUCHED].clip(lower=0)
    df_monthly[TOUCHED] = df_monthly[TOUCHED].astype(int)

    # --- 3. Implement C-Chart Logic ---

    # C-Chart Center Line (CL): Average number of "Additional Files Touched"
    CL = df_monthly[TOUCHED].mean()

    # C-Chart Control Limits (UCL and LCL) based on 3-sigma (p-value equivalent)
    # Standard deviation for a C-Chart (Poisson distribution) is sqrt(CL)
    sigma = np.sqrt(CL)
    UCL = CL + 3 * sigma
    LCL = max(0, CL - 3 * sigma) # LCL cannot be negative


    # Plot the monthly counts
    plt.plot(df_monthly[MONTH], df_monthly[TOUCHED], marker='o', linestyle='-', color='b', label='Monthly $\\Delta$ Files Touched')

    # Plot the Center Line
    plt.axhline(CL, color='g', linestyle='-', linewidth=2, label=f'Center Line (CL): {CL:.2f}')

    # Plot the Upper Control Limit (UCL)
    plt.axhline(UCL, color='r', linestyle='--', linewidth=2, label=f'UCL (3$\\sigma$): {UCL:.2f}')

    # Plot the Lower Control Limit (LCL)
    plt.axhline(LCL, color='r', linestyle='--', linewidth=2, label=f'LCL (3$\\sigma$): {LCL:.2f}')

    # Highlight out-of-control points (the 'clusters' or anomalies)
    out_of_control = df_monthly[(df_monthly[TOUCHED] > UCL) | (df_monthly[TOUCHED] < LCL)]
    plt.plot(out_of_control[MONTH], out_of_control[TOUCHED], 'o', color='red', markersize=8)


    plt.xlabel(UNIT_FREQUENCY[unit])
    plt.ylabel('Total Additional Files Touched')


    file_name = path + get_base_file_name(FILE_NAME) + "." + type.lower().replace(" ",".") + "." + str(unit) + ".pdf"
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    return file_name

def generate_and_save(repository_id, component, developers):
    if component == "packages":
        path = "repository/" + str(repository_id) + "/" 
        read_write_file.write_file(get_base_file_name(FILE_NAME) + ".tex", 
                               section_sub_heading(repository_id, component), path)
    default_generate_save(generate_graph, BASE_FILE_NAME, FILE_NAME, repository_id, component, developers, figure_caption=FIGURE_CAPTION)
