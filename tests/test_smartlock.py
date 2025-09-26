from unittest.mock import patch, call
import pytest

from tests.test_constants import SMARTLOCK_ID


def test_list_smartlocks(nuki_client):
    lst = nuki_client.smartlock.list_smartlocks()
    assert len(lst) > 0


def test_list_smartlocks_with_params(nuki_client):
    # Cover lines where params dict is populated (auth_id and type_)
    with patch.object(nuki_client, "_request") as mock_request:
        mock_request.return_value.json.return_value = [{"smartlockId": 123}]

        result = nuki_client.smartlock.list_smartlocks(auth_id=42, type_=1)

        mock_request.assert_called_once_with(
            "GET", "/smartlock", params={"authId": 42, "type": 1}
        )
        assert result[0]["smartlockId"] == 123


def test_get_smartlock(nuki_client):
    sl_instance = nuki_client.smartlock.get_smartlock(SMARTLOCK_ID)
    assert sl_instance.id == SMARTLOCK_ID


def test_bulk_web_config(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"foo": "bar"}
        result = client.smartlock.bulk_web_config(data)

        mock_request.assert_called_once_with("POST", "/bulk-web-config", json=data)
        assert result["status"] == "success"


def test_update_smartlock(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"foo": "bar"}
        result = client.smartlock.update_smartlock(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123", json=data)
        assert result["status"] == "success"


def test_update_smartlock_with_none(client):
    # Cover 'data or {}' branch
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        result = client.smartlock.update_smartlock(123, data=None)
        mock_request.assert_called_once_with("POST", "/smartlock/123", json={})
        assert result["status"] == "success"


def test_delete_smartlock(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        result = client.smartlock.delete_smartlock(123)

        mock_request.assert_called_once_with("DELETE", "/smartlock/123")
        assert result["status"] == "success"


def test_action(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        action_data = {"action": 2}
        result = client.smartlock.action(123, action_data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/action", json=action_data)
        assert result["status"] == "success"


def test_action_with_none(client):
    # Cover 'data or {}' branch
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        result = client.smartlock.action(123, data=None)
        mock_request.assert_called_once_with("POST", "/smartlock/123/action", json={})
        assert result["status"] == "success"


def test_update_admin_pin(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"pin": "1234"}
        result = client.smartlock.update_admin_pin(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/admin/pin", json=data)
        assert result["status"] == "success"


def test_update_advanced_config(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"a": 1}
        result = client.smartlock.update_advanced_config(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/advanced/config", json=data)
        assert result["status"] == "success"


def test_update_opener_advanced_config(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"o": 2}
        result = client.smartlock.update_opener_advanced_config(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/advanced/openerconfig", json=data)
        assert result["status"] == "success"


def test_update_smartdoor_advanced_config(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"s": 3}
        result = client.smartlock.update_smartdoor_advanced_config(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/advanced/smartdoorconfig", json=data)
        assert result["status"] == "success"


def test_update_config(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"c": 4}
        result = client.smartlock.update_config(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/config", json=data)
        assert result["status"] == "success"


def test_sync_smartlock(nuki_client):
    response = nuki_client.smartlock.sync_smartlock(SMARTLOCK_ID)
    assert response.status_code == 204


def test_update_web_config(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"status": "success"}

        data = {"w": 5}
        result = client.smartlock.update_web_config(123, data)

        mock_request.assert_called_once_with("POST", "/smartlock/123/web/config", json=data)
        assert result["status"] == "success"
