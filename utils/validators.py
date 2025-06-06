from pydantic_core import Url, ValidationError

def validate_url(url: str) -> Url:
    try:
        return Url(url).unicode_string()
    except ValidationError as e:
        raise ValueError("Invalid URL", e)
