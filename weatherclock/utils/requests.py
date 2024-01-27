from typing import Any
import requests


def get_json(url: str | None) -> dict[str, Any]:
    # TODO: need to add headers to the request - differ by weather and trulys endpoint
    if url is None:
        return {}

    response: requests.Response = requests.get(url)
    validate_response(response)
    return response.json()


def validate_response(response: requests.Response) -> None:
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
