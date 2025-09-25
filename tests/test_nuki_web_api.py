import pytest
from unittest.mock import patch, Mock
from nukiwebapi.nuki_web_api import NukiWebAPI, SmartlockInstance


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload




def test_fetch_smartlocks_skips_items_without_id():
    """_fetch_smartlocks skips smartlock entries without 'smartlockId'."""
    fake_response = FakeResponse([
        {"smartlockId": 123, "name": "Lock 123"},
        {"name": "No ID"}
    ])
    with patch.object(NukiWebAPI, "_request", return_value=fake_response):
        client = NukiWebAPI("FAKE_API_KEY")
        locks = client._fetch_smartlocks()
        assert 123 in locks
        assert len(locks) == 1
        assert isinstance(locks[123], SmartlockInstance)



def test_request_calls_requests_with_correct_headers():
    """_request sets Authorization and Accept headers correctly."""
    fake_response = Mock()
    fake_response.text = '{"ok": true}'
    fake_response.raise_for_status = Mock()
    fake_response.json.return_value = {"ok": True}

    with patch("requests.request", return_value=fake_response) as mock_req:
        client = NukiWebAPI("FAKE_API_KEY")
        result = client._request("GET", "/test", headers={"X-Custom": "Value"})

        mock_req.assert_called_once()
        args, kwargs = mock_req.call_args
        # Verify headers
        assert kwargs["headers"]["Authorization"] == "Bearer FAKE_API_KEY"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["headers"]["X-Custom"] == "Value"
        # Verify return value
        assert result.json() == {"ok": True}
