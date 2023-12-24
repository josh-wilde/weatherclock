from datetime import datetime
from matplotlib.axes import Axes
from matplotlib.text import Text

from weatherclock.utils.text import initialize_text_subplot


# TODO: change datetime to Date object
class Date:
    def __init__(self, axes: Axes, dt: datetime) -> None:
        self.axes: Axes = initialize_text_subplot(axes)

        # Set the plot references
        self._date_text_refs: dict[str, Text] | None = None

        # Update the axes
        self.update(dt)

    # TODO: finish pull stuff out in the settings file and transition over to the Date object
    def update(self, dt: datetime) -> None:
        month_day_str: str = f"{dt.month_str} {dt.day_str}"

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
