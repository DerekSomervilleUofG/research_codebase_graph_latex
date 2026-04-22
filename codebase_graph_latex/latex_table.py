COLUMN_MAX_WIDTH = 10

def generate_latex_heading(headings):
    processed_cells = []
    
    for heading in headings:
        # If it's short, just bold it
        if len(heading) <= COLUMN_MAX_WIDTH:
            processed_cells.append(r"\textbf{" + heading + "}")
        else:
            # It's long, so we build ONE makecell with internal line breaks
            words = heading.split(" ")
            lines = []
            current_line = ""
            
            for word in words:
                # Check if adding the next word exceeds width
                if len(current_line + word) <= COLUMN_MAX_WIDTH:
                    current_line += (word + " ")
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            
            # Add the last remaining bit
            if current_line:
                lines.append(current_line.strip())
            
            # Join lines with LaTeX line breaks \\
            # Use [b] to keep all headers aligned at the bottom
            inner_text = r"\\".join([r"\textbf{" + l + "}" for l in lines])
            processed_cells.append(r"\makecell[b]{" + inner_text + "}")         
    return " & ".join(processed_cells) + r" \\ " + "\n"

def start_latex_table(caption, headings, column_setup=""):
    num_r_columns = len(headings)
    latex_column_setup = "" 
    if column_setup == "":
        column_setup = "r " * num_r_columns
    latex_column_setup += column_setup
    section = "\\begin{table}[!h]\n"
    section += "\\centering\n"
    section += "\\setlength{\\tabcolsep}{2pt}\n"
    section += f"\\caption{{{caption}}}\n"
    section += f"\\begin{{tabular}}{{{latex_column_setup.strip()}}}\n"
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