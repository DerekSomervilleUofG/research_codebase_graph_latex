def generate_latex_heading(headings):
    latex = ""
    for heading in headings:
        if latex != "":
            latex += " & "
        latex += "\\textbf{" + heading + "}"
    return latex + "\\\\ \n"

def start_latex_table(caption, headings):
    num_r_columns = len(headings) - 1
    column_setup = "p{3cm} " + "r " * num_r_columns
    section = "\\begin{table}[h!]\n"
    section += "\\centering\n"
    section += f"\\caption{{{caption}}}\n"
    section += f"\\begin{{tabular}}{{{column_setup.strip()}}}\n"
    section += "\\toprule\n"
    section += generate_latex_heading(headings)
    section += "\\midrule\n"
    return section

def table_end():
    table = "\\bottomrule\n"
    table += "\\end{tabular}\n"
    table += "\\end{table}\n"
    table += "\\end{landscape}\n"
    table += "\\newpage \n"
    return table