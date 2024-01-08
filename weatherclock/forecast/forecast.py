from typing import Any
import requests

from weatherclock.utils.requests import get_json
from weatherclock.date_time.date_time import DateTime


class Forecast:
    def __init__(self, latitude: float, longitude: float, date_time: DateTime) -> None:
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.forecast_as_of_time: DateTime = date_time
        self._endpoints: dict[str, str] = {}
        # The first level of this dict should indicate which endpoint the data came from (forecast, forecasut_hourly, forecast_grid_data)
        self._forecast_attributes: dict[str, Any] = {}

        self.update()

    def update(self, date_time: DateTime) -> None:
        # Should call update_forecast_endpoints() monthly or if self.endpoints is empty
        # Update forecast if the as of time is stale by calling updates on each endpoint
        pass

    def get(self, forecast_attribute: str | None = None) -> Any:
        if forecast_attribute is None:
            return self._forecast_attributes

        attribute: Any | None = self._forecast_attributes.get(forecast_attribute)
        if attribute is None:
            raise AttributeError(
                f"Forecast object has no attribute {forecast_attribute}"
            )

        return attribute

    def _update_forecast_endpoints(self) -> None:
        points_url: str = (
            f"https://api.weather.gov/points/{self.latitude},{self.longitude}"
        )
        points_json: dict[str, Any] = get_json(points_url)

        points_properties: dict[str, str] | None = points_json.get("properties")
        if points_properties is None:
            raise ValueError("No properties found in points request")

        # Update endpoints
        self._endpoints["forecast"]: dict = points_properties.get("forecast", {})
        self._endpoints["forecast_hourly"]: dict = points_properties.get(
            "forecastHourly", {}
        )
        self._endpoints["forecast_grid_data"]: dict = points_properties.get(
            "forecastGridData", {}
        )

    def _update_forecast_endpoint_attributes(self) -> None:
        pass

    def _update_forecast_hourly_endpoint_attributes(self) -> None:
        pass

    def _update_forecast_grid_data_endpoint_attributes(self) -> None:
        pass
