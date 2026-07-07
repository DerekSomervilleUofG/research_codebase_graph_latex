import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from codebase_graph_latex.repository_graph.master_graph import *
from codebase_graph_latex.latex_graph import *
import os

FILE_NAME = __name__
BASE_FILE_NAME = "repository_summary_1.tex"
CAPTION = "A seaborn strip plot of packages touched (y-axis) against number of developers (x-axis) made by "

CATEGORY_COLORS = {
    "transient founder": TRANSIENT_FOUNDER_COLOUR,
    "moderate founder": MODERATE_FOUNDER_COLOUR,
    "sustained founder": SUSTAINED_FOUNDER_COLOUR,
    "transient later joiner": TRANSIENT_JOINER_COLOUR,
    "moderate later joiner": MODERATE_JOINER_COLOUR,
    "sustained later joiner": SUSTAINED_JOINER_COLOUR
}

def build_stripplot_dataframe(all_categories_data):
    """
    Transforms dictionary-based category data into a long-form DataFrame.
    all_categories_data: dict mapping category names to their respective developer dictionaries
    """
    records = []
    for cat_name, developers in all_categories_data.items():
        for key, developer in developers.items():
           if isinstance(developer, list) and len(developer[KNOWN_Y_AXIS]) > 0:
                records.append({"developer_id": key,
                                "packages_touched":developer[KNOWN_Y_AXIS][-1],
                                "category":cat_name})
                
    df = pd.DataFrame(records)
    
    df.to_csv(
                os.path.join(f"{cat_name}.csv"),
                index=False
            )

    return df

def create_packages_stripplot(path, all_categories_data, threshold=0, file_name_suffix="stripplot"):
    
    df = build_stripplot_dataframe(all_categories_data)
    counts = (df.groupby(["packages_touched", "category"])
            .size()
            .reset_index(name="num_developers")
            )
    plt.figure(figsize=LARGE_FIGURE, dpi=1000)
    sns.set_theme(style="whitegrid")
    

    ax = sns.stripplot(
        data=counts, 
        x="packages_touched", 
        y="num_developers", 
        hue="category",   # one line per category
        palette=CATEGORY_COLORS,
        marker="o"
    )

    ax.set_yscale("log")

    
    ax.axvline(
        x=threshold-1,
        color='red',
        linestyle='--',
        linewidth=2,
        label='Sustained threshold'
    )
    
    # 4. Final adjustments & Save (Integrating with your existing save workflow)
    plt.subplots_adjust(left=0.25) # Give extra breathing room for long category labels
    plt.xlabel("Packages Touched")
    plt.ylabel("Number of Developer (log)")
    
    # Generate file path matching your naming standards
    file_name = f"{path}{get_base_file_name(FILE_NAME)}.packages.{file_name_suffix}.pdf"
    
    plt.savefig(file_name, bbox_inches='tight')
    plt.clf()
    plt.close()
    
    return file_name

def get_category_numbers(all_categories_data):
    numbers = []
    for cat_name in CATEGORY_COLORS.keys():
        if cat_name in all_categories_data.keys():
            numbers.append(len(all_categories_data[cat_name]))
    return numbers

def generate_and_save(developers, threshold):
    numbers = get_category_numbers(developers)
    caption = CAPTION + get_figure_caption_numbers_suffix(FIGURE_CAPTION_NUMBERS, numbers)
    latex = get_section_start(FILE_NAME, "") + "Number of Developers versus Packages Touched} \n" 
    latex += latex_add_graph(create_packages_stripplot(DIRECTORY + "graph/", developers, threshold), caption)
    latex += "\\newpage "
    save_to_latex_file(get_base_file_name(FILE_NAME), BASE_FILE_NAME, latex, DIRECTORY)