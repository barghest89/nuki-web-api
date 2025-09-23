# tests/conftest.py
import pytest
from unittest.mock import patch
from nukiwebapi.nuki_web_api import NukiWebAPI



def _default_response(method: str, endpoint: str, json = None, **kwargs):
    """Return a safe default response for any endpoint."""
    json_data = kwargs.get("json") or {}

    if isinstance(json, list):
        return {"status": "success", "ids": json}

    return {"status": "success", **(json or {})}

@pytest.fixture
def client():
    """Return a NukiWebAPI client with _request mocked to safe defaults."""
    def fake_request(method, endpoint, **kwargs):
        return _default_response(method, endpoint, **kwargs)

    with patch.object(NukiWebAPI, "_request", side_effect=fake_request) as mock_request:
        client = NukiWebAPI("FAKE_API_KEY")
        client._mock_request = mock_request
        yield client
