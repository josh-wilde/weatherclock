from bs4 import BeautifulSoup
import requests

headers: dict = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url: str = "https://trulys.com/flavor-of-the-day-calendar/"

response: requests.Response = requests.get(url, headers=headers)

soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

# TODO: need to figure out how to effectively search and extract from the HTML
