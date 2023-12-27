from datetime import datetime
from weatherclock.constants import MONTH_NAMES, WEEKDAY_NAMES


class DateTime:
    def __init__(self, dt: datetime):
        self.update(dt)

    def update(self, dt: datetime):
        # Times
        self.hour: int = dt.hour
        self.minute: int = dt.minute
        self.second: int = dt.second

        # Dates
        self.year: int = dt.year
        self.month: int = dt.month
        self.day: int = dt.day
        self.weekday: int = dt.weekday()

        # Convert to string representations
        self._update_strings()

    def _update_strings(self):
        twelve_hour: int = self.hour % 12 if self.hour % 12 != 0 else 12
        self.hour_str: str = f"{twelve_hour}"
        self.minute_str: str = f"{self.minute:02}"
        self.second_str: str = f"{self.second:02}"

        self.year_str: str = f"{self.year}"
        self.month_str: str = MONTH_NAMES[self.month]
        self.day_str: str = f"{self.day}"
        self.weekday_str: str = WEEKDAY_NAMES[self.weekday]

    def __repr__(self):
        return f"{self.weekday_str} {self.year_str} {self.month_str} {self.day_str} {self.hour_str}:{self.minute_str}:{self.second_str}"
