import requests
from weatherclock.settings.location import LAT_LONG
from PIL import Image
import os

# Information needed:
# - Next 12 hours of icons, temperatures, precip percentage, maybe wind speed and direction
# - detailed description of forecast for today and tomorrow

# Request demo
# 1. Get the forecast, forecastHourly, and forecastGridData URLs:
# points_request: Response = requests.get(f"https://api.weather.gov/points/{','.join(map(str, LAT_LONG))}")
# Check to make sure that the request was successful: points_request.status_code == 200
# points_request_json: dict = points_request.json()
# forecast_url: str = points_request_json.get("properties").get("forecast")
# forecast_hourly_url: str = points_request_json.get("properties").get("forecastHourly")
# forecast_grid_data_url: str = points_request_json.get("properties").get("forecastGridData")


class Forecast:
    def __init__(self) -> None:
        pass

    def update(self) -> None:
        pass

    def get_daily_detailed(self) -> str:
        return "Daily detailed forecast"
