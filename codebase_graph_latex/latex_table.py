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

def get_number_match(headings, heading_index, match_word):
    num_headings = len(headings)
    match_count = 1
    while (heading_index + match_count < num_headings and 
            match_count < 4 and 
            headings[heading_index + match_count][0:len(match_word)] == match_word):
        match_count += 1
    return match_count

def generate_latex_heading_parts(headings):
    row1_cells = []
    row2_cells = []
    cmidrules = []
    
    heading_index = 0
    num_headings = len(headings)
    
    # Track the real, absolute data column index (1-based for LaTeX)
    actual_col_idx = 1
    
    while heading_index < num_headings:
        current_heading = headings[heading_index]
        first_word = current_heading.split(" ")[0]
        
        match_count = get_number_match(headings, heading_index, first_word)
            
        if match_count > 1:
            # Row 1 gets the top level multi-column master cell span
            row1_cells.append(r"\multicolumn{" + str(match_count) + r"}{c}{\textbf{" + first_word + "}}")
            
            # Row 2 gets the distinct trailing text for each sub-column
            for offset in range(match_count):
                h_words = headings[heading_index + offset].split(" ")
                sub_text = " ".join(h_words[1:]) if len(h_words) > 1 else headings[heading_index + offset]
                
                # FIX: Explicitly pass sub-column fields through format_cell_text 
                # using configuration parameters that trigger bold text tags ("t" or equivalent)
                row2_cells.append(format_cell_text(sub_text, "t"))
            
            col_start = actual_col_idx
            col_end = actual_col_idx + match_count - 1
            cmidrules.append(f"\\cmidrule(lr){{{col_start}-{col_end}}}")
            
            heading_index += match_count
            actual_col_idx += match_count
        else:
            # Standalone single-column cell layout block
            row1_cells.append(format_cell_text(current_heading, "t"))
            
            # Row 2 gets a blank cell placeholder to balance the column layout vector
            row2_cells.append("")
            
            heading_index += 1
            actual_col_idx += 1
    return row1_cells, row2_cells, cmidrules

def generate_latex_heading(headings):
    
    row1_cells, row2_cells, cmidrules = generate_latex_heading_parts(headings)

    total_data_columns = len(row2_cells)
    
    # We need to find out how many columns our multicolumn cells 'ate'
    columns_in_row1 = 0
    for cell in row1_cells:
        if r"\multicolumn" in cell:
            # Extract the integer number inside the first curly brace: \multicolumn{X}{...}
            # e.g., \multicolumn{4}{c}{...} -> extracts 4
            span_size = int(cell.split("{")[1].split("}")[0])
            columns_in_row1 += span_size
        else:
            columns_in_row1 += 1
            
    missing_padding_cells = total_data_columns - columns_in_row1
    
    # 3. Construct Row 1 and append trailing empty cells if any columns are missing
    latex_output = " & ".join(row1_cells)
    if missing_padding_cells > 0:
        latex_output += " & " * missing_padding_cells
    latex_output += r" \\ " + "\n"
    
    # 4. Construct alignment rules cleanly
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

def table_end(file_path):
    table = "\\bottomrule\n"
    table += "\\end{tabular}%\n"
    table += "} \n"
    table += "\\label{tab:" + file_path.replace(".", "_")
    table += "} \n"
    table += "\\end{table}\n"    
    table += "\\newpage \n"
    return table