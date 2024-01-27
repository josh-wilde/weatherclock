from typing import Any
import requests

from weatherclock.utils.requests import get_json
from weatherclock.date_time.date_time import DateTime


class Forecast:
    def __init__(self, latitude: float, longitude: float, date_time: DateTime) -> None:
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.forecast_as_of_time: DateTime = date_time
        self._endpoints: dict[str, str | None] = {}
        self._forecast_attributes: dict[str, Any] = {
            "forecast": {},
            "forecast_hourly": {},
            "forecast_grid_data": {},
        }

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
        self._endpoints["forecast"] = points_properties.get("forecast", None)
        self._endpoints["forecast_hourly"] = points_properties.get(
            "forecastHourly", None
        )
        self._endpoints["forecast_grid_data"] = points_properties.get(
            "forecastGridData", None
        )

    def _update_forecast_endpoint_attributes(self) -> None:
        # Pull the short forecast [properties][periods][num][shortForecast], could also use detailedForecast
        # Pull tomorrow's forecast after 6pm, today's forecast before 6pm
        forecast: dict = get_json(self._endpoints["forecast"])
        forecast_periods: list[dict[str, Any]] = forecast.get("properties", {}).get(
            "periods", {}
        )
        first_period_name: str = forecast_periods[0]["name"]

        if self.forecast_as_of_time.hour >= 18 and "night" in first_period_name.lower():
            forecast_period = 1
        else:
            forecast_period = 0

        self._forecast_attributes["forecast"]["short_forecast"] = (
            f"{forecast_periods[forecast_period]['name']}: "
            f"{forecast_periods[forecast_period]['shortForecast']}"
        )

    def _update_forecast_hourly_endpoint_attributes(self) -> None:
        # Temperature
        # Prob of precip
        # icon url
        forecast_hourly: dict = get_json(self._endpoints["forecast_hourly"])
        forecast_hourly_periods: list[dict[str, Any]] = forecast_hourly.get(
            "properties", {}
        ).get("periods", {})

        for period in forecast_hourly_periods[:12]:
            hour: int = ...  # parse startTime
            self._forecast_attributes["forecast_hourly"][hour] = {
                "temperature": period["temperature"],
                "probability_of_precipitation": period["probabilityOfPrecipitation"][
                    "value"
                ],
                "icon_url": period["icon"],
            }

    def _update_forecast_grid_data_endpoint_attributes(self) -> None:
        pass
