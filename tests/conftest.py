# tests/conftest.py
import os

import pytest
from unittest.mock import patch

from dotenv import load_dotenv

from nukiwebapi.nuki_web_api import NukiWebAPI

load_dotenv()  # looks for .env in cwd

API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = int(os.getenv("NUKI_SMARTLOCK_ID"))
ACCOUNT_ID = int(os.getenv("NUKI_ACCOUNT_USER_ID") ) # existing account user for tests


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

@pytest.fixture
def nuki_client():
    return NukiWebAPI(API_TOKEN)
