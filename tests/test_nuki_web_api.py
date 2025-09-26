from unittest.mock import Mock, patch, MagicMock

import pytest
import requests
from requests import Response, Request

from nukiwebapi import NukiWebAPI


def test_fetch_smartlocks_skips_invalid_entries(client):
    """_fetch_smartlocks should skip entries missing 'smartlockId'."""

    # Mock _request to return a Response-like object with .json() method
    fake_response = Mock()
    fake_response.json.return_value = [
        {"name": "valid_lock", "smartlockId": 123},
        {"name": "invalid_lock"}  # missing smartlockId
    ]

    with patch.object(client, "_request", return_value=fake_response):
        smartlocks = client._fetch_smartlocks()
        assert 123 in smartlocks
        # Ensure the invalid entry was skipped
        assert all(lock.id != None for lock in smartlocks.values())

def test_request_value_error_captured():
    """_request should handle ValueError when response.json() fails."""
    client = NukiWebAPI("FAKE_TOKEN")

    # Create a real Response object
    fake_response = requests.Response()
    fake_response.status_code = 400
    fake_response._content = b"Not JSON content"  # raw bytes
    fake_response.url = "https://api.nuki.io/endpoint"

    # Patch requests.request to return this response
    with patch("requests.request", return_value=fake_response):
        with pytest.raises(requests.HTTPError) as excinfo:
            res = client._request("GET", "/endpoint")
            print(res)
    # Check that the fallback text from .text is in the exception
    assert "Not JSON content" in str(excinfo.value)