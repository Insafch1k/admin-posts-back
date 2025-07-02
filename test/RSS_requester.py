import pytest
from utils.web_requester.requester import RSS_requester
from pydantic_core import ValidationError
from requests.exceptions import HTTPError, Timeout


def test_successful_request(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        def raise_for_status(self):
            pass

        @property
        def text(self):
            return "<rss><item><title>Test</title></item></rss>"

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    result = RSS_requester("https://example.com/feed")
    assert "<title>Test</title>" in result


def test_invalid_url(monkeypatch):
    def mock_validate_url(url):
        raise ValidationError.from_exception_data("Invalid URL", [])

    monkeypatch.setattr("utils.validators.validate_url", mock_validate_url)

    with pytest.raises(ValueError) as exc_info:
        RSS_requester("invalid-url")

    assert "Invalid URL" in str(exc_info.value)


def test_http_error_404(monkeypatch):
    class MockResponse404:
        def __init__(self):
            self.status_code = 404

        def raise_for_status(self):
            raise HTTPError("404 Not Found")

    def mock_get(*args, **kwargs):
        return MockResponse404()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(ValueError) as exc_info:
        RSS_requester("https://example.com/feed")

    assert "Failed to fetch feed from" in str(exc_info.value)


def test_timeout_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise Timeout("Request timed out")

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(ValueError) as exc_info:
        RSS_requester("https://example.com/feed")

    assert "Failed to fetch feed from" in str(exc_info.value)