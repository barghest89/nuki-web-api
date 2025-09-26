# tests/conftest.py
import os

import pytest
from unittest.mock import patch

from tests.test_constants import API_TOKEN

from nukiwebapi.nuki_web_api import NukiWebAPI

from requests.models import Response
import json as pyjson


from requests.models import Response
import json as json_module


def _default_response(method: str, endpoint: str, json=None, **kwargs) -> Response:
    """Return a fake Response object for testing."""

    resp = Response()
    resp.status_code = 200
    resp.headers["Content-Type"] = "application/json"

    # Determine response content based on endpoint
    if endpoint == "/address":
        # Return a list of addresses
        content = [
            {"id": 1, "name": "Fake Address", "smartlockIds": [123]}
        ]
    elif endpoint.startswith("/smartlock/") and "/log" in endpoint:
        # Return fake logs
        content = [
            {"id": "log1", "smartlockId": 123, "action": 1}
        ]
    elif endpoint.startswith("/smartlock/") and "/auth" in endpoint:
        # Return fake auths
        content = [
            {"id": "auth1", "smartlockId": 123, "name": "Test Auth"}
        ]
    elif isinstance(json, list):
        content = {"status": "success", "ids": json}
    elif isinstance(json, dict):
        content = {"status": "success", **json}
    else:
        content = {"status": "success"}

    # Serialize content into the response object
    resp._content = json_module.dumps(content).encode("utf-8")
    resp.encoding = "utf-8"

    return resp

@pytest.fixture
def client():
    """Return a NukiWebAPI client with _request mocked to safe defaults."""
    def fake_request(method, endpoint, **kwargs):
        return _default_response(method, endpoint, **kwargs)

    with patch.object(NukiWebAPI, "_request", side_effect=fake_request) as mock_request:
        client = NukiWebAPI("FAKE_API_KEY")
        client._mock_request = mock_request
        yield client

@pytest.fixture
def nuki_client():
    return NukiWebAPI(API_TOKEN)
