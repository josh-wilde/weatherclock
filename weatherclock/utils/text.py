from matplotlib.axes import Axes
from matplotlib.text import Text


def initialize_text_subplot(self, ax: Axes) -> Axes:
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    return ax
