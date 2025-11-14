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

FIGURE_CAPTION_NUMBERS = "samples of developers capped at NUM4 from four categories: "
FIGURE_CAPTION_NUMBERS += "\\color{" + TRANSIENT_FOUNDER_COLOUR + "}" + TRANSIENT_FOUNDER.title() + " (" + TRANSIENT_FOUNDER_COLOUR + ", NUM1), "
FIGURE_CAPTION_NUMBERS += "\\color{" + SUSTAINED_FOUNDER_COLOUR + "}" ": " + SUSTAINED_FOUNDER.title() + " (" + SUSTAINED_FOUNDER_COLOUR + ", NUM2), "
FIGURE_CAPTION_NUMBERS += "\\color{" + TRANSIENT_JOINER_COLOUR + "}" ": " + TRANSIENT_JOINER.title() + " (" + TRANSIENT_JOINER_COLOUR + ", NUM3), "
FIGURE_CAPTION_NUMBERS += "\\color{" + SUSTAINED_JOINER_COLOUR + "}" ": " + SUSTAINED_JOINER.title() + " (" + SUSTAINED_JOINER_COLOUR + ", NUM4). "
FIGURE_CAPTION_NUMBERS += "\\color{Black}"

def get_figure_caption_numbers_suffix(caption, numbers):
    counter = 1
    for num in numbers:
        if num > 0:
            caption = caption.replace("NUM" + str(counter), str(num))
        counter += 1
    return caption