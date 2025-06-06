import requests
from pydantic_core import ValidationError
from .validators import validate_url
from typing import Optional


def RSS_requester(url):
    try:
        valid_url = validate_url(url)
    except ValidationError as e:
        raise ValueError(f"Invalid URL {url}", e)
    headers = {
        "User-Agent": "RSSFetcher/1.0 (+https://yourapp.com)" # когда-то здесь будет ссылка на наш сайт
    }
    try:
        response = requests.get(
            url=valid_url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch feed from {url}", e)
