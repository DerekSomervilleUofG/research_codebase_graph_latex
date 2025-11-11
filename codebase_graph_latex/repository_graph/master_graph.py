from utility.ReadWriteFile import ReadWriteFile
from codebase_graph_latex.latex_graph import *
from codebase_graph_latex.constants import *
import matplotlib.pyplot as plt
import inflect

word_engine = inflect.engine()
read_write_file = ReadWriteFile()

TRANSIENT_FOUNDER_COLOUR = 'Blue'
SUSTAINED_FOUNDER_COLOUR = 'Green'
TRANSIENT_JOINER_COLOUR = 'Orange'
SUSTAINED_JOINER_COLOUR = 'Red'

FIGURE_CAPTION_NUMBERS = "Key for the four categories of developer: "
FIGURE_CAPTION_NUMBERS += "\\begin{itemize} "
FIGURE_CAPTION_NUMBERS += "\\item \\color{" + TRANSIENT_FOUNDER_COLOUR + "}" + TRANSIENT_FOUNDER_COLOUR + ": " + TRANSIENT_FOUNDER.title() + " - Sample size NUM1 developers. "
FIGURE_CAPTION_NUMBERS += "\\item \\color{" + SUSTAINED_FOUNDER_COLOUR + "}" + SUSTAINED_FOUNDER_COLOUR + ": " + SUSTAINED_FOUNDER.title() + " - Sample size NUM2 developers. "
FIGURE_CAPTION_NUMBERS += "\\item \\color{" + TRANSIENT_JOINER_COLOUR + "}" + TRANSIENT_JOINER_COLOUR + ": " + TRANSIENT_JOINER.title() + " - Sample size NUM3 developers. "
FIGURE_CAPTION_NUMBERS += "\\item \\color{" + SUSTAINED_JOINER_COLOUR + "}" + SUSTAINED_JOINER_COLOUR + ": " + SUSTAINED_JOINER.title() + " - Sample size NUM4 developers. "
FIGURE_CAPTION_NUMBERS += "\\end{itemize} "
FIGURE_CAPTION_NUMBERS += "\\color{Black}"

def get_figure_caption_numbers_suffix(caption, numbers):
    counter = 1
    for num in numbers:
        if num > 0:
            caption = caption.replace("NUM" + str(counter), str(num))
        counter += 1
    return caption