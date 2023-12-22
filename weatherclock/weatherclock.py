import sys
from typing import Any
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
from matplotlib.text import Text

from constants import MONTH_NAMES, WEEKDAY_NAMES


class DateTime:
    def __init__(self, dt: datetime):
        self.update(dt)

    def update(self, dt: datetime):
        # Times
        self.hour: int = dt.hour
        self.minute: int = dt.minute
        self.second: int = dt.second

        # Dates
        self.month: int = dt.month
        self.day: int = dt.day
        self.weekday: int = dt.weekday()

        # Convert to string representations
        self._update_strings()

    def _update_strings(self):
        self.hour_str: str = f"{self.hour}"
        self.minute_str: str = f"{self.minute:02}"
        self.second_str: str = f"{self.second:02}"

        self.month_str: str = MONTH_NAMES[self.month]
        self.day_str: str = f"{self.day}"
        self.weekday_str: str = WEEKDAY_NAMES[self.weekday]

    def __repr__(self):
        return f"{self.weekday_str} {self.month_str} {self.day_str} {self.hour_str}:{self.minute_str}:{self.second_str}"


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

        # Store references to the plot elements that will be updated
        self._clock_hand_plot_refs: dict[str, Line2D] | None = None
        self._date_text_refs: dict[str, Text] | None = None
        self._forecast_text_ref: Text | None = None

        # Create a datetime object to store the current time
        self.now: DateTime = DateTime(datetime.now())

        # TODO: Create a weather object to store the current weather information

        # Set the elements of the Axes objects that won't change
        self.initialize_axes()

        self.update_plot()
        self.canvas.draw()

        # self.showFullScreen()
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def initialize_axes(self):
        # Set up the weather clock
        self.initialize_weatherclock()

        # Set up the date and the forecast
        for axes_name in ["date", "forecast"]:
            self.initialize_text_subplot(axes_name)

    def initialize_text_subplot(self, axes_name: str):
        ax: Axes = self.canvas.axes[axes_name]

        ax.axis("off")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

    def initialize_weatherclock(self):
        ax: Axes = self.canvas.axes["weatherclock"]
        ax.set_xticks(np.linspace(0, 2 * pi, 12, endpoint=False))

        # TODO: these will need to come from the weather API, so will move into the update function
        ax.set_xticklabels(range(1, 13))
        ax.set_theta_direction(-1)
        ax.set_theta_offset(pi / 3.0)
        ax.grid(False)
        ax.set_ylim(0, 1)
        ax.set_yticklabels([])

    def update_weatherclock(self):
        weatherclock: Axes = self.canvas.axes["weatherclock"]

        angles: dict[str, float] = {
            "hour": (
                2 * pi * self.now.hour / 12
                + 2 * pi * self.now.minute / (12 * 60)
                + 2 * self.now.second / (12 * 60 * 60)
                - pi / 6.0
            ),
            "minute": (
                2 * pi * self.now.minute / 60
                + 2 * pi * self.now.second / (60 * 60)
                - pi / 6.0
            ),
            "second": 2 * pi * self.now.second / 60 - pi / 6.0,
        }

        if self._clock_hand_plot_refs is None:
            shared_kwargs: dict[str, Any] = {"solid_capstyle": "round"}
            self._clock_hand_plot_refs = {
                "second": weatherclock.plot(
                    [angles["second"], angles["second"]],
                    [0, 0.95],
                    color="red",
                    linewidth=1,
                    **shared_kwargs,
                )[0],
                "minute": weatherclock.plot(
                    [angles["minute"], angles["minute"]],
                    [0, 0.8],
                    color="black",
                    linewidth=2,
                    **shared_kwargs,
                )[0],
                "hour": weatherclock.plot(
                    [angles["hour"], angles["hour"]],
                    [0, 0.5],
                    color="black",
                    linewidth=4,
                    **shared_kwargs,
                )[0],
            }
        else:
            for hand, plot_ref in self._clock_hand_plot_refs.items():
                plot_ref.set_xdata([angles[hand], angles[hand]])

    def update_date(self):
        date_ax: Axes = self.canvas.axes["date"]
        month_day_str: str = f"{self.now.month_str} {self.now.day_str}"

        if self._date_text_refs is None:
            shared_kwargs: dict[str, Any] = {
                "horizontalalignment": "center",
                "verticalalignment": "center",
            }
            self._date_text_refs = {
                "month_day": date_ax.text(
                    5,
                    6.5,
                    f"{self.now.month_str} {self.now.day_str}",
                    fontsize=32,
                    **shared_kwargs,
                ),
                "week_day": date_ax.text(
                    5, 4, self.now.weekday_str, fontsize=24, **shared_kwargs
                ),
            }
        else:
            self._date_text_refs["month_day"].set_text(month_day_str)
            self._date_text_refs["week_day"].set_text(self.now.weekday_str)

    def update_forecast(self):
        # TODO: this will be updated with a call to the weather object
        forecast_str: str = f"Short description of the day's forecast at {self.now.hour_str}:{self.now.hour_str}."

        if self._forecast_text_ref is None:
            self._forecast_text_ref = self.canvas.axes["forecast"].text(
                5,
                7,
                forecast_str,
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=12,
                wrap=True,
            )
            self._forecast_text_ref._get_wrap_line_width = lambda: 300
        else:
            self._forecast_text_ref.set_text(forecast_str)

    def update_plot(self):
        # Get the current time and date
        self.now.update(datetime.now())
        # TODO: Get the current hourly weather information
        # TODO: get the current forecast information

        # Update the weatherclock axes
        self.update_weatherclock()

        # Update the date axes
        self.update_date()

        # Update the forecast axes
        self.update_forecast()

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
