from matplotlib.axes import Axes


def initialize_text_subplot(ax: Axes) -> Axes:
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    return ax
