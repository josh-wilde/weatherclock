from typing import Any
import sys

import numpy as np
from numpy import pi
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.artist import Artist
from PIL import Image

from weatherclock.utils.clock import get_hour_angle, get_minute_angle, get_second_angle
from weatherclock.settings.weatherclock import AXES_SETTINGS, PLOT_SETTINGS, YVALS
from weatherclock.date_time.date_time import DateTime
from weatherclock.hour_markers.hour_markers import HourMarkers


class WeatherClock:
    # TODO: this will also take in a Forecast object, eventually, that will get passed to the HourMarkers init
    def __init__(self, axes: Axes, dt: DateTime | None = None) -> None:
        self.axes: Axes = axes
        self.hour_markers: HourMarkers = HourMarkers()
        self.icon_artists: list[Artist] = []

        # Initialize the clock axes
        self._initialize_axes()

        # Set the plot references
        self._plot_refs: dict[str, Line2D] | None = None

        # Update the clock
        if dt is not None:
            self.update(dt)

    def _initialize_axes(self) -> None:
        # This stuff should not change
        self.axes.set_xticks(np.linspace(0, 2 * pi, 12, endpoint=False))
        self.axes.set_theta_direction(-1)
        self.axes.set_theta_offset(pi / 3.0)
        self.axes.grid(False)
        self.axes.set_ylim(0, 1)
        self.axes.set_yticklabels([])
        self.axes.axis("off")

        # TODO: move this all into a method
        # There is a bug that makes the scaling weird if the icons trespass outside the axes
        # Currently I am controlling this by using the y position of the AnnotationBbox
        # Can't figure out how to fix it
        # this might help: https://matplotlib.org/stable/users/explain/animations/blitting.html
        # also this: https://stackoverflow.com/questions/17558096/animated-title-in-matplotlib
        self.axes.set_xticklabels(["" for _ in range(12)])
        xticklabels: list[Text] = self.axes.xaxis.get_ticklabels()
        icons: list[Image.Image] = self.hour_markers.get_icons()
        for i, icon in enumerate(icons):
            icon_oi: OffsetImage = OffsetImage(icon, zoom=1.0)
            icon_oi.image.axes = self.axes
            icon_ab: AnnotationBbox = AnnotationBbox(
                offsetbox=icon_oi,
                xy=(xticklabels[i].get_position()[0], 0.75),
                frameon=False,
            )
            self.icon_artists.append(self.axes.add_artist(icon_ab))

        # Stuff that can be set from AXES_SETTINGS
        if facecolor := AXES_SETTINGS.get("facecolor"):
            self.axes.set_facecolor(facecolor)

    def update(self, dt: DateTime) -> None:
        # TODO: update HourMarkers
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

        # for icon_artist in self.icon_artists:
        #    self.axes.draw_artist(icon_artist)

    def _get_angles(self, dt: DateTime) -> dict[str, float]:
        return {
            "hour": get_hour_angle(dt),
            "minute": get_minute_angle(dt),
            "second": get_second_angle(dt),
        }
