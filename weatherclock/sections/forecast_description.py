from typing import Any

from matplotlib.axes import Axes
from matplotlib.text import Text

from weatherclock.forecast.forecast import Forecast
from weatherclock.utils.text import initialize_text_subplot
from weatherclock.settings.forecast_description import PLOT_SETTINGS


class ForecastDescription:
    def __init__(self, axes: Axes, forecast: Forecast | None = None) -> None:
        self.axes: Axes = initialize_text_subplot(axes)

        # Set the plot references
        self._plot_refs: dict[str, Text] | None = None

        # Set references to the text strings
        self.text_strings: dict[str, str] = {}

        # Update the axes
        if forecast is not None:
            self.update(forecast.get_daily_detailed())

    def _set_plot_refs(self, daily_detailed: str) -> None:
        shared_kwargs: dict[str, Any] = PLOT_SETTINGS["shared"]

        self._plot_refs = {}
        # Daily detailed forecast
        self._plot_refs["daily_detailed"] = self.axes.text(
            PLOT_SETTINGS["daily_detailed"]["x_position"],
            PLOT_SETTINGS["daily_detailed"]["y_position"],
            daily_detailed,
            horizontalalignment=PLOT_SETTINGS["daily_detailed"]["horizontalalignment"],
            verticalalignment=PLOT_SETTINGS["daily_detailed"]["verticalalignment"],
            fontsize=PLOT_SETTINGS["daily_detailed"]["fontsize"],
            **shared_kwargs,
        )

    def _update_plot_refs(self, daily_detailed: str) -> None:
        self._plot_refs["daily_detailed"].set_text(daily_detailed)

    def update(self, forecast: Forecast) -> None:
        daily_detailed: str = forecast.get_daily_detailed()
        if self._plot_refs is None:
            # Set the plot references
            self._set_plot_refs(daily_detailed)
        else:
            self._update_plot_refs(daily_detailed)
