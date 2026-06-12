COLUMN_MAX_WIDTH = 10

def format_cell_text(text, vertical_align="t"):
        if len(text) <= COLUMN_MAX_WIDTH:
            return r"\textbf{" + text + "}"
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + word) <= COLUMN_MAX_WIDTH:
                current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        inner_text = r"\\".join([r"\textbf{" + l + "}" for l in lines])
        return r"\makecell[" + vertical_align + "]{" + inner_text + "}"

def generate_latex_heading(headings):
    row1_cells = []
    row2_cells = []
    cmidrules = []
    
    i = 0
    num_headings = len(headings)
    
    while i < num_headings:
        current_heading = headings[i]
        words = current_heading.split(" ")
        first_word = words[0]
        
        # Check if the next heading shares the exact same first word (and we aren't at the last element)
        if i + 1 < num_headings and headings[i + 1].split(" ")[0] == first_word:
            # We found a pair! Extract the sub-words for row 2
            sub_word1 = " ".join(words[1:]) if len(words) > 1 else first_word
            sub_word2 = " ".join(headings[i + 1].split(" ")[1:]) if len(headings[i + 1].split(" ")) > 1 else first_word
            
            # Row 1 gets the shared multi-column master span
            row1_cells.append(r"\multicolumn{2}{c}{\textbf{" + first_word + "}}")
            
            # Row 2 gets the distinct individual metrics underneath
            row2_cells.append(format_cell_text(sub_word1, "c"))
            row2_cells.append(format_cell_text(sub_word2, "c"))
            
            # Add 1-based index rules for LaTeX tracking (Col index = standard array index + 1)
            col_start = i + 1
            cmidrules.append(f"\\cmidrule(lr){{{col_start}-{col_start + 1}}}")
            
            # Skip the next element in the loop since it's merged
            i += 2
        else:
            # Standalone single column header block
            row1_cells.append(format_cell_text(current_heading, "t"))
            
            # Row 2 gets a completely blank cell placeholder in this column position
            row2_cells.append("")
            i += 1

    # Construct the final 2-row table layout block
    latex_output = " & ".join(row1_cells) + r" \\ " + "\n"
    
    if cmidrules:
        latex_output += " ".join(cmidrules) + "\n"
        
    latex_output += " & ".join(row2_cells) + r" \\ " + "\n"
    return latex_output

def start_latex_table(caption, headings, column_setup=""):
    num_r_columns = len(headings)
    latex_column_setup = "" 
    if column_setup == "":
        column_setup = "r " * num_r_columns
    latex_column_setup += column_setup
    section = "\\begin{table}[H]\n"
    section += "\\centering\n"
    section += "\\setlength{\\tabcolsep}{2pt}\n"
    section += f"\\caption{{{caption}}}\n"
    section += "\\resizebox{\\textwidth}{!}{% \n"
    section += f"\\begin{{tabular}}{{{latex_column_setup.strip()}}}\n"
    section += "\\toprule\n"
    section += generate_latex_heading(headings)
    section += "\\midrule\n"
    return section

def table_end():
    table = "\\bottomrule\n"
    table += "\\end{tabular}%\n"
    table += "} \n"
    table += "\\end{table}\n"
    table += "\\newpage \n"
    return table