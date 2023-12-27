from typing import Any
from matplotlib.axes import Axes
from matplotlib.text import Text

from weatherclock.date_time.date_time import DateTime
from weatherclock.utils.text import initialize_text_subplot
from weatherclock.settings.date import PLOT_SETTINGS


class Date:
    def __init__(self, axes: Axes, dt: DateTime | None = None) -> None:
        self.axes: Axes = initialize_text_subplot(axes)

        # Set the plot references
        self._plot_refs: dict[str, Text] | None = None

        # Set references to the text strings
        self.text_strings: dict[str, str] = {}

        # Update the axes
        if dt is not None:
            self.update(dt)

    def _set_plot_refs(self) -> None:
        shared_kwargs: dict[str, Any] = PLOT_SETTINGS["shared"]
        self._plot_refs = {
            subplot_name: self.axes.text(
                subplot_settings["x_position"],
                subplot_settings["y_position"],
                self.text_strings[subplot_name],
                fontsize=subplot_settings["fontsize"],
                **shared_kwargs,
            )
            for subplot_name, subplot_settings in PLOT_SETTINGS.items()
            if subplot_name != "shared"
        }

    def _update_plot_refs(self) -> None:
        for subplot_name, text_string in self.text_strings.items():
            self._plot_refs[subplot_name].set_text(text_string)

    def update(self, dt: DateTime) -> None:
        self.text_strings = {
            "month_day": f"{dt.month_str} {dt.day_str}",
            "weekday": dt.weekday_str,
        }

        if self._plot_refs is None:
            # Set the plot references
            self._set_plot_refs()
        else:
            self._update_plot_refs()
