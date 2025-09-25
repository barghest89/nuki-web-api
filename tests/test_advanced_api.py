import pytest
from unittest.mock import patch, call

# ---- Decentralized Webhooks ----
def test_list_decentral_webhooks(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = [{"id": 1}]
        result = client.advanced_api.list_decentral_webhooks()
        mock_request.assert_called_once_with("GET", "/api/decentralWebhook")
        assert isinstance(result, list)
        assert result[0]["id"] == 1


def test_create_decentral_webhook(client):
    webhook_url = "https://example.com/webhook"
    webhook_features = ["DEVICE_STATUS", "ACCOUNT_USER"]

    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = {"id": 1, "webhookUrl": webhook_url}
        result = client.advanced_api.create_decentral_webhook(webhook_url, webhook_features)

        mock_request.assert_called_once_with(
            "PUT",
            "/api/decentralWebhook",
            json={"webhookUrl": webhook_url, "webhookFeatures": list(set(webhook_features))}
        )
        assert result["webhookUrl"] == webhook_url


def test_create_decentral_webhook_invalid_url(client):
    with pytest.raises(ValueError):
        client.advanced_api.create_decentral_webhook("http://notsecure.com", ["DEVICE_STATUS"])


def test_create_decentral_webhook_invalid_feature(client):
    with pytest.raises(ValueError):
        client.advanced_api.create_decentral_webhook("https://secure.com", ["INVALID_FEATURE"])


def test_delete_decentral_webhook(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = {"status": "deleted"}
        result = client.advanced_api.delete_decentral_webhook(123)
        mock_request.assert_called_once_with("DELETE", "/api/decentralWebhook/123")
        assert result["status"] == "deleted"


def test_get_webhook_logs(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = [{"id": "log1"}]
        result = client.advanced_api.get_webhook_logs(42, limit=50)
        mock_request.assert_called_once_with(
            "GET",
            "/api/key/42/webhook/logs",
            params={"limit": 50}
        )
        assert isinstance(result, list)
        assert result[0]["id"] == "log1"


# ---- Smartlock Advanced Authorizations ----
def test_create_smartlock_auth_advanced(client):
    auth_data = {"name": "Auth1"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = {"requestId": "R1"}
        result = client.advanced_api.create_smartlock_auth_advanced(auth_data)
        mock_request.assert_called_once_with("PUT", "/smartlock/auth/advanced", json=auth_data)
        assert result["requestId"] == "R1"


def test_action_smartlock_advanced(client):
    action_data = {"action": 7}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = {"requestId": "A1"}
        result = client.advanced_api.action_smartlock_advanced("SL1", action_data)
        mock_request.assert_called_once_with("POST", "/smartlock/SL1/action/advanced", json=action_data)
        assert result["requestId"] == "A1"


def test_lock_smartlock_advanced(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = {"requestId": "L1"}
        result = client.advanced_api.lock_smartlock_advanced("SL1")
        mock_request.assert_called_once_with("POST", "/smartlock/SL1/action/lock/advanced", json={})
        assert result["requestId"] == "L1"


def test_unlock_smartlock_advanced(client):
    unlock_data = {"option": "fast"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value.json.return_value = {"requestId": "U1"}
        result = client.advanced_api.unlock_smartlock_advanced("SL1", unlock_data)
        mock_request.assert_called_once_with("POST", "/smartlock/SL1/action/unlock/advanced", json=unlock_data)
        assert result["requestId"] == "U1"
