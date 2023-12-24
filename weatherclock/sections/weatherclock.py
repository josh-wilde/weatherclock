from typing import Any
from datetime import datetime
import numpy as np
from numpy import pi
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from weatherclock.utils.clock import get_hour_angle, get_minute_angle, get_second_angle
from weatherclock.settings.weatherclock import AXES_SETTINGS, PLOT_SETTINGS, YVALS


class WeatherClock:
    def __init__(self, axes: Axes, dt: datetime) -> None:
        self.axes: Axes = axes

        # Initialize the clock axes
        self._initialize_axes()

        # Set the plot references
        self._plot_refs: dict[str, Line2D] | None = None

        # Update the clock
        self.update(dt)

    def _initialize_axes(self) -> None:
        # This stuff should not change
        self.axes.set_xticks(np.linspace(0, 2 * pi, 12, endpoint=False))
        self.axes.set_theta_direction(-1)
        self.axes.set_theta_offset(pi / 3.0)
        self.axes.grid(False)
        self.axes.set_ylim(0, 1)
        self.axes.set_yticklabels([])

        # TODO: these will need to come from the weather API, so will move into the update function
        self.axes.set_xticklabels(range(1, 13))

        # Stuff that can be set from AXES_SETTINGS
        if facecolor := AXES_SETTINGS.get("facecolor"):
            self.axes.set_facecolor(facecolor)

    # TODO: change this to take in a Date object
    def update(self, dt: datetime) -> None:
        # Get the current angles
        angles: dict[str, float] = self._get_angles(dt)

        if self._plot_refs is None:
            # Set the plot references
            self._set_plot_refs(angles)
        else:
            self._update_plot_refs(angles)

    def _set_plot_refs(self, angles: dict[str, float]) -> None:
        shared_kwargs: dict[str, Any] = PLOT_SETTINGS["shared"]

        self._plot_refs = {
            hand: self.axes.plot(
                [angles[hand], angles[hand]],
                YVALS[hand],
                **PLOT_SETTINGS[hand],
                **shared_kwargs,
            )[0]
            for hand in ["second", "minute", "hour"]
        }

    def _update_plot_refs(self, angles: dict[str, float]) -> None:
        for hand, plot_ref in self._plot_refs.items():
            plot_ref.set_xdata([angles[hand], angles[hand]])

    def _get_angles(self, dt: datetime) -> dict[str, float]:
        return {
            "hour": get_hour_angle(dt),
            "minute": get_minute_angle(dt),
            "second": get_second_angle(dt),
        }
