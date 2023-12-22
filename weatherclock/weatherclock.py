import sys
import random
import matplotlib
import numpy as np
from numpy import pi
from datetime import datetime

matplotlib.use("Qt5Agg")

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4.8, dpi=100):
        fig: Figure = Figure(figsize=(width, height), dpi=dpi, layout="constrained")
        gs: GridSpec = GridSpec(2, 2, width_ratios=[1.5, 1], figure=fig)
        self.axes: dict[str, Axes] = {
            "weatherclock": fig.add_subplot(gs[:, 0], polar=True),
            "date": fig.add_subplot(gs[0, 1]),
            "forecast": fig.add_subplot(gs[1, 1]),
        }
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas()
        self.setCentralWidget(self.canvas)

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._clock_hand_plot_refs: dict[str, Line2D] | None = None

        # Setup the clock
        self.canvas.axes["weatherclock"].set_xticks(
            np.linspace(0, 2 * pi, 12, endpoint=False)
        )
        self.canvas.axes["weatherclock"].set_xticklabels(range(1, 13))
        self.canvas.axes["weatherclock"].set_theta_direction(-1)
        self.canvas.axes["weatherclock"].set_theta_offset(pi / 3.0)
        self.canvas.axes["weatherclock"].grid(False)
        self.canvas.axes["weatherclock"].set_ylim(0, 1)
        self.canvas.axes["weatherclock"].set_yticklabels([])

        self.update_plot()
        self.canvas.draw()

        # self.showFullScreen()
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        weatherclock: Axes = self.canvas.axes["weatherclock"]
        now: datetime = datetime.now()
        hour: int = now.hour
        minute: int = now.minute
        second: int = now.second

        angles_h = (
            2 * pi * hour / 12
            + 2 * pi * minute / (12 * 60)
            + 2 * second / (12 * 60 * 60)
            - pi / 6.0
        )
        angles_m = 2 * pi * minute / 60 + 2 * pi * second / (60 * 60) - pi / 6.0
        angles_s = 2 * pi * second / 60 - pi / 6.0

        if self._clock_hand_plot_refs is None:
            s_plot_refs: list[Line2D] = weatherclock.plot(
                [angles_s, angles_s],
                [0, 0.95],
                color="red",
                linewidth=1,
                solid_capstyle="round",
            )
            m_plot_refs: list[Line2D] = weatherclock.plot(
                [angles_m, angles_m],
                [0, 0.8],
                color="black",
                linewidth=2,
                solid_capstyle="round",
            )
            h_plot_refs: list[Line2D] = weatherclock.plot(
                [angles_h, angles_h],
                [0, 0.5],
                color="black",
                linewidth=4,
                solid_capstyle="round",
            )

            self._clock_hand_plot_refs = {
                "second": s_plot_refs[0],
                "minute": m_plot_refs[0],
                "hour": h_plot_refs[0],
            }
        else:
            self._clock_hand_plot_refs["second"].set_xdata([angles_s, angles_s])
            self._clock_hand_plot_refs["minute"].set_xdata([angles_m, angles_m])
            self._clock_hand_plot_refs["hour"].set_xdata([angles_h, angles_h])

        # Trigger the canvas to update and redraw.
        self.canvas.draw()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    qapp.exec()
