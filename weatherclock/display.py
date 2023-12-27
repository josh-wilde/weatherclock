import sys
import matplotlib
from datetime import datetime

matplotlib.use("Qt5Agg")

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec

from weatherclock.sections import WeatherClock, Date, ForecastDescription
from weatherclock.date_time.date_time import DateTime
from weatherclock.forecast.forecast import Forecast


class MplCanvas(FigureCanvas):
    def __init__(self, width=8, height=4.8, dpi=100, **fig_kwargs):
        # Set up figure and add axes
        fig: Figure = Figure(figsize=(width, height), dpi=dpi, **fig_kwargs)
        gs: GridSpec = GridSpec(2, 2, width_ratios=[1.5, 1], figure=fig)
        self.axes: dict[str, Axes] = {
            "weatherclock": WeatherClock(axes=fig.add_subplot(gs[:, 0], polar=True)),
            "date": Date(axes=fig.add_subplot(gs[0, 1])),
            "forecast_description": ForecastDescription(axes=fig.add_subplot(gs[1, 1])),
        }

        super(MplCanvas, self).__init__(fig)

    def update_axes(self, dt: DateTime, forecast: Forecast) -> None:
        self.axes["weatherclock"].update(dt)
        self.axes["date"].update(dt)
        self.axes["forecast_description"].update(forecast)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(layout="constrained", facecolor="lightgray")
        self.setCentralWidget(self.canvas)

        # Create a datetime object to store the current time
        self.now: DateTime = DateTime(datetime.now())

        # Forecast object to store the current weather information
        self.forecast: Forecast = Forecast()

        # Update the plot and draw it
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
        # Get the current time and date
        self.now.update(datetime.now())
        self.forecast.update()
        # TODO: Get the current hourly weather information
        # TODO: get the current forecast information

        # Update the axes of the canvas with the current time and date and forecast
        self.canvas.update_axes(self.now, self.forecast)

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
