from typing import Any
import requests


def get_json(url: str) -> dict[str, Any]:
    response: requests.Response = requests.get(url)
    validate_response(response)
    return response.json()


def validate_response(response: requests.Response) -> None:
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
