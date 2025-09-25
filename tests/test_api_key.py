from unittest.mock import patch, call

# ---- API Keys ----
def test_list_api_keys(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = [{"apiKeyId": 1}, {"apiKeyId": 2}]
        result = client.api_key.list_api_keys()

        mock_request.assert_called_once_with("GET", "/api/key")
        assert isinstance(result, list)
        assert len(result) == 2

def test_create_api_key(client):
    key_data = {"description": "Test", "redirectUris": ["https://example.com"]}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"apiKeyId": 1, "description": "Test"}
        result = client.api_key.create_api_key(key_data)

        mock_request.assert_called_once_with("PUT", "/api/key", json=key_data)
        assert result["description"] == "Test"

def test_update_api_key(client):
    key_data = {"description": "Updated"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.update_api_key(1, key_data)

        mock_request.assert_called_once_with("POST", "/api/key/1", json=key_data)
        assert isinstance(result, dict)

def test_delete_api_key(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.delete_api_key(1)

        mock_request.assert_called_once_with("DELETE", "/api/key/1")
        assert isinstance(result, dict)

# ---- Advanced API Keys ----
def test_get_advanced_api_key(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"name": "AdvancedKey"}
        result = client.api_key.get_advanced_api_key(1)

        mock_request.assert_called_once_with("GET", "/api/key/1/advanced")
        assert result["name"] == "AdvancedKey"

def test_create_advanced_api_key(client):
    key_data = {"name": "AdvKey"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.create_advanced_api_key(1, key_data)

        mock_request.assert_called_once_with("PUT", "/api/key/1/advanced", json=key_data)
        assert isinstance(result, dict)

def test_update_advanced_api_key(client):
    key_data = {"webhookUrl": "https://example.com"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.update_advanced_api_key(1, key_data)

        mock_request.assert_called_once_with("POST", "/api/key/1/advanced", json=key_data)
        assert isinstance(result, dict)

def test_delete_advanced_api_key(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.delete_advanced_api_key(1)

        mock_request.assert_called_once_with("DELETE", "/api/key/1/advanced")
        assert isinstance(result, dict)

def test_reactivate_advanced_api_key(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.reactivate_advanced_api_key(1)

        mock_request.assert_called_once_with("POST", "/api/key/1/advanced/reactivate")
        assert isinstance(result, dict)

# ---- API Key Tokens ----
def test_list_api_key_tokens(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = [{"id": "T1"}, {"id": "T2"}]
        result = client.api_key.list_api_key_tokens(1)

        mock_request.assert_called_once_with("GET", "/api/key/1/token")
        assert isinstance(result, list)
        assert len(result) == 2

def test_create_api_key_token(client):
    token_data = {"description": "Token1", "scopes": ["read"]}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"id": "T1"}
        result = client.api_key.create_api_key_token(1, token_data)

        mock_request.assert_called_once_with("PUT", "/api/key/1/token", json=token_data)
        assert result["id"] == "T1"

def test_update_api_key_token(client):
    token_data = {"description": "UpdatedToken"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.update_api_key_token(1, "T1", token_data)

        mock_request.assert_called_once_with("POST", "/api/key/1/token/T1", json=token_data)
        assert isinstance(result, dict)

def test_delete_api_key_token(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {}
        result = client.api_key.delete_api_key_token(1, "T1")

        mock_request.assert_called_once_with("DELETE", "/api/key/1/token/T1")
        assert isinstance(result, dict)
