import unittest
from codebase_graph_latex.latex_table import *

class TestGetNumberMatch(unittest.TestCase):

    def test_no_matches_ahead(self):
        """Should return 1 if the subsequent headers do not share the match_word prefix."""
        headings = ["OLS df", "ART df", "Factor", "Component"]
        
        expected = 1
        actual = get_number_match(headings, heading_index=0, match_word="OLS")
        
        self.assertEqual(expected, actual)

    def test_single_match_ahead(self):
        """Should return 2 if exactly one subsequent header matches (total group of 2)."""
        headings = ["OLS df", "OLS F-Stat", "Factor", "Component"]
        
        expected = 2
        actual = get_number_match(headings, heading_index=0, match_word="OLS")
        
        self.assertEqual(expected, actual)

    def test_double_match_ahead_hitting_cap(self):
        """Should return 3 if two subsequent headers match (total group of 3, hitting the cap)."""
        headings = ["OLS df", "OLS F-Stat", "OLS $P$ Value", "OLS $\eta^2$"]
        
        expected = 4
        actual = get_number_match(headings, heading_index=0, match_word="OLS")
        
        self.assertEqual(expected, actual)

    def test_array_boundary_termination(self):
        """Should handle running out of headers gracefully without throwing an IndexError."""
        headings = ["Factor", "ART df", "ART F-Stat"]
        
        expected = 2
        actual = get_number_match(headings, heading_index=1, match_word="ART")
        
        self.assertEqual(expected, actual)

    def test_exact_word_matching(self):
        """Verifies that the method accurately tracks whole words instead of sliding character prefixes."""
        headings = ["Component", "First *n* commits", "First week commits"]
        
        expected = 2
        actual = get_number_match(headings, heading_index=1, match_word="First")
        
        self.assertEqual(expected, actual)

    def test_starting_at_last_element(self):
        """Should immediately return 1 if the heading_index points to the absolute last element."""
        headings = ["Component", "First *n* commits", "Number of Developers"]
        
        expected = 1
        actual = get_number_match(headings, heading_index=2, match_word="Number")
        
        self.assertEqual(expected, actual)

    def test_all_standalone_columns(self):
        """No headings share a first word. Row 2 should contain only empty placeholder cells."""
        headings = ["Component", "Factor"]
        
        expected = (
            r"\textbf{Component} & \textbf{Factor} \\ " + "\n"
            r" &  \\ " + "\n"
        )
        actual = generate_latex_heading(headings)
        self.assertEqual(expected, actual)

    def test_triple_prefix_merge(self):
        """Three headings share a first word. Row 1 creates a multicolumn, Row 2 holds sub-words."""
        headings = ["OLS df", "OLS F-Stat", "OLS $P$ Value"]
        
        expected = (
            r"\multicolumn{3}{c}{\textbf{OLS}} \\ " + "\n"
            r"\cmidrule(lr){1-3}" + "\n"
            r"df & F-Stat & $P$ Value \\ " + "\n"
        )
        actual = generate_latex_heading(headings)
        self.assertEqual(expected, actual)

    def test_window_cap_at_four_columns(self):
        """Four items share a prefix. It should merge the first 3, then treat the 4th as standalone."""
        headings = ["OLS df", "OLS F-Stat", "OLS $P$ Value", "OLS $\eta^2$"]
        
        expected = (
            r"\multicolumn{4}{c}{\textbf{OLS}} \\ " + "\n"
            r"\cmidrule(lr){1-4}" + "\n"
            r"\textbf{df} & \textbf{F-Stat} & \textbf{$P$ Value} & \textbf{$\eta^2$} \\ " + "\n"
        )
        actual = generate_latex_heading(headings)
        self.assertEqual(expected, actual)

    def test_mixed_table_dissertation_matrix(self):
        """Simulates your actual 12-column paired layout parameters."""
        headings = [
            "Component", "Factor", 
            "OLS df", "OLS F-Stat", "OLS $P$ Value", 
            "ART df", "ART F-Stat", "ART $P$ Value"
        ]
        
        expected = (
            r"\textbf{Component} & \textbf{Factor} & "
            r"\multicolumn{3}{c}{\textbf{OLS}} & "
            r"\multicolumn{3}{c}{\textbf{ART}} \\ " + "\n"
            r"\cmidrule(lr){3-5} \cmidrule(lr){6-8}" + "\n"
            r" &  & \textbf{df} & \textbf{F-Stat} & \textbf{$P$ Value} & \textbf{df} & \textbf{F-Stat} & \textbf{$P$ Value} \\ " + "\n"
        )
        actual = generate_latex_heading(headings)
        self.assertEqual(expected, actual)

    def test_single_word_repeats(self):
        """If repeating columns have no sub-words, Row 2 should gracefully fall back to the full token."""
        headings = ["Data", "Data"]
        
        expected = (
            r"\multicolumn{2}{c}{\textbf{Data}} \\ " + "\n"
            r"\cmidrule(lr){1-2}" + "\n"
            r"\textbf{Data} & \textbf{Data} \\ " + "\n"
        )
        actual = generate_latex_heading(headings)
        self.assertEqual(expected, actual)
    
    def test_all_standalone_columns(self):
        """Standalone items shouldn't trigger multicolumn spans or cmidrules."""
        headings = ["Component", "Factor"]
        
        expected_row1 = ["\\textbf{Component}", "\\textbf{Factor}"]
        expected_row2 = ["", ""]
        expected_rules = []
        
        act_row1, act_row2, act_rules = generate_latex_heading_parts(headings)
        
        self.assertEqual(expected_row1, act_row1)
        self.assertEqual(expected_row2, act_row2)
        self.assertEqual(expected_rules, act_rules)

    def test_triple_prefix_merge(self):
        """Verifies correct structural grouping and rule indexing across 3 items."""
        headings = ["DOLS df", "DOLS F-Stat", "DOLS $P$ Value"]
        
        expected_row1 = [r"\multicolumn{3}{c}{\textbf{DOLS}}"]
        expected_row2 = ["\\textbf{df}", "\\textbf{F-Stat}", "\\textbf{$P$ Value}"]
        expected_rules = ["\\cmidrule(lr){1-3}"]
        
        act_row1, act_row2, act_rules = generate_latex_heading_parts(headings)
        
        self.assertEqual(expected_row1, act_row1)
        self.assertEqual(expected_row2, act_row2)
        self.assertEqual(expected_rules, act_rules)

    def test_window_cap_at_four_columns_with_makecell(self):
        """Confirms that a 4th matching item is safely processed by the standalone logic."""
        headings = ["DOLS df", "DOLS F-Stat", "DOLS $P$ Value", "DOLS $\eta^2$"]
        
        expected_row1 = [
            r"\multicolumn{4}{c}{\textbf{DOLS}}"
        ]
        expected_row2 = ["\\textbf{df}", "\\textbf{F-Stat}", "\\textbf{$P$ Value}", "\\textbf{$\eta^2$}"]
        expected_rules = ["\\cmidrule(lr){1-4}"]
        
        act_row1, act_row2, act_rules = generate_latex_heading_parts(headings)
        
        self.assertEqual(expected_row1, act_row1)
        self.assertEqual(expected_row2, act_row2)
        self.assertEqual(expected_rules, act_rules)

    def test_mixed_dissertation_table_matrix(self):
        """Validates that absolute indices for cmidrules are tracked correctly across gaps."""
        headings = [
            "Component", "Factor", 
            "OLS df", "OLS F-Stat", "OLS $P$ Value", 
            "ART df", "ART F-Stat", "ART $P$ Value"
        ]
        
        expected_row1 = [
            "\\textbf{Component}", 
            "\\textbf{Factor}", 
            r"\multicolumn{3}{c}{\textbf{OLS}}", 
            r"\multicolumn{3}{c}{\textbf{ART}}"
        ]
        expected_row2 = [
            "", "", 
            "\\textbf{df}", "\\textbf{F-Stat}", "\\textbf{$P$ Value}", 
            "\\textbf{df}", "\\textbf{F-Stat}", "\\textbf{$P$ Value}"
        ]
        expected_rules = ["\\cmidrule(lr){3-5}", "\\cmidrule(lr){6-8}"]
        
        act_row1, act_row2, act_rules = generate_latex_heading_parts(headings)
        
        self.assertEqual(expected_row1, act_row1)
        self.assertEqual(expected_row2, act_row2)
        self.assertEqual(expected_rules, act_rules)

    def test_single_word_repeats_fallback(self):
        """Verifies that items with no trailing words safely default to bolding the full token."""
        headings = ["Data", "Data"]
        
        expected_row1 = [r"\multicolumn{2}{c}{\textbf{Data}}"]
        expected_row2 = ["\\textbf{Data}", "\\textbf{Data}"]
        expected_rules = ["\\cmidrule(lr){1-2}"]
        
        act_row1, act_row2, act_rules = generate_latex_heading_parts(headings)
        
        self.assertEqual(expected_row1, act_row1)
        self.assertEqual(expected_row2, act_row2)
        self.assertEqual(expected_rules, act_rules)

if __name__ == "__main__":
    unittest.main()