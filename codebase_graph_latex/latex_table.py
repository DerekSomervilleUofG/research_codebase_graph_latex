def generate_latex_heading(headings):
    latex = ""
    for heading in headings:
        if latex != "":
            latex += " & "
        latex += "\\textbf{" + heading + "}"
    return latex + "\\\\ \n"

def start_latex_table(caption, headings):
    section = "\\begin{table}[h!]\n"
    section += "\\centering\n"
    section += f"\\caption{{{caption}}}\n"
    section += "\\begin{tabular}{p{3cm} r r r r r r }\n"
    section += "\\toprule\n"
    section += generate_latex_heading(headings)
    section += "\\midrule\n"
    return section