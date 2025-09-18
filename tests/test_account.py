# tests/test_account.py
import pytest
from unittest.mock import patch, call
from nukiwebapi import NukiWebAPI
from dotenv import load_dotenv
import os

load_dotenv()  # looks for .env in cwd
API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = os.getenv("NUKI_SMARTLOCK_ID")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

def test_account():
    client = NukiWebAPI(API_TOKEN)
    acc = client.account.get()
    assert acc is not None
    assert str(acc["accountId"]) == ACCOUNT_ID


def test_delete_account():

    # Patch _request on this client instance
    with patch.object(NukiWebAPI, "_request") as mock_request:
        mock_request.return_value = []
        client = NukiWebAPI("FAKE")

        mock_request.return_value = {"status": "success"}

        result = client.account.delete()

        mock_request.assert_has_calls([
            call("GET", "/smartlock"),
            call("DELETE", "/account")
        ])
        assert result["status"] == "success"

def test_update_account():

    # Patch _request on this client instance
    with patch.object(NukiWebAPI, "_request") as mock_request:
        mock_request.return_value = []
        client = NukiWebAPI("FAKE")

        mock_request.return_value = {"status": "success"}

        result = client.account.update({"accountId":"FAKE"})

        mock_request.assert_has_calls([
            call("GET", "/smartlock"),
            call('POST', '/account', json={'accountId': 'FAKE'})
        ])
        assert result["status"] == "success"

def test_change_email():

    # Patch _request on this client instance
    with patch.object(NukiWebAPI, "_request") as mock_request:
        mock_request.return_value = []
        client = NukiWebAPI("FAKE")

        mock_request.return_value = {"status": "success"}

        result = client.account.change_email("fake_email")

        mock_request.assert_has_calls([
            call("GET", "/smartlock"),
            call('POST', '/account/email/change', json={'email': 'fake_email'})
        ])
        assert result["status"] == "success"

def test_send_verification_email():

    # Patch _request on this client instance
    with patch.object(NukiWebAPI, "_request") as mock_request:
        mock_request.return_value = []
        client = NukiWebAPI("FAKE")

        mock_request.return_value = {"status": "success"}

        result = client.account.verify_email()

        mock_request.assert_has_calls([
            call("GET", "/smartlock"),
            call('POST', '/account/email/verify')
        ])
        assert result["status"] == "success"

def test_list_integrations():
    print()
    client = NukiWebAPI(API_TOKEN)
    acc = client.account.list_integrations()
    print(acc)

def test_delete_integration():

    # Patch _request on this client instance
    with patch.object(NukiWebAPI, "_request") as mock_request:
        mock_request.return_value = []
        client = NukiWebAPI("FAKE")

        mock_request.return_value = {"status": "success"}
        apiKeyId = "abc123"
        tokenId= "deadbeef"
        data = {"apiKeyId": apiKeyId, "tokenId": tokenId}
        result = client.account.delete_integration(apiKeyId, tokenId)

        mock_request.assert_has_calls([
            call("GET", "/smartlock"),
            call("DELETE", "/account/integration", json=data)
        ])
        assert result["status"] == "success"


@pytest.fixture
def client():
    # Patch _request on NukiWebAPI so init calls don't make real HTTP requests
    with patch.object(NukiWebAPI, "_request") as mock_request:
        mock_request.side_effect = [
            [],  # GET /smartlock during init
            {"status": "success"}  # POST /account/otp
        ]

        yield NukiWebAPI("FAKE")

def test_enable_otp(client):

    result = client.account.enable_otp()
    client._request.assert_called_with("POST", "/account/otp")
    assert result["status"] == "success"

def test_create_otp(client):
    data = {"method": "totp"}
    result = client.account.create_otp(data)
    client._request.assert_called_with("PUT", "/account/otp", json=data)
    assert result["status"] == "success"

def test_disable_otp(client):
    result = client.account.disable_otp()
    client._request.assert_called_with("DELETE", "/account/otp")
    assert result["status"] == "success"

def test_reset_password(client):
    email = "user@example.com"
    delete_tokens = True

    result = client.account.reset_password(email=email, deleteApiTokens=delete_tokens)

    client._request.assert_called_with(
        "POST",
        "/account/password/reset",
        json={"email": email, "deleteApiTokens": delete_tokens}
    )
    assert result["status"] == "success"

def test_get_setting(client):
    result = client.account.get_setting()
    client._request.assert_called_with("GET", "/account/setting")
    assert result["status"] == "success"

def test_update_setting(client):
    data = {"theme": "dark"}
    result = client.account.update_setting(data)
    client._request.assert_called_with("PUT", "/account/setting", json=data)
    assert result["status"] == "success"

def test_delete_setting(client):
    key = "theme"
    result = client.account.delete_setting(key)
    client._request.assert_called_with("DELETE", "/account/setting", json={"key": key})
    assert result["status"] == "success"

def test_list_sub_accounts(client):
    result = client.account.list_sub_accounts()
    client._request.assert_called_with("GET", "/account/sub")
    assert result["status"] == "success"

def test_create_sub_account(client):
    data = {"name": "SubUser"}
    result = client.account.create_sub_account(data)
    client._request.assert_called_with("PUT", "/account/sub", json=data)
    assert result["status"] == "success"

def test_get_sub_account(client):
    account_id = "abc123"
    result = client.account.get_sub_account(account_id)
    client._request.assert_called_with("GET", f"/account/sub/{account_id}")
    assert result["status"] == "success"

def test_update_sub_account(client):
    account_id = "abc123"
    data = {"name": "Updated"}
    result = client.account.update_sub_account(account_id, data)
    client._request.assert_called_with("POST", f"/account/sub/{account_id}", json=data)
    assert result["status"] == "success"

def test_delete_sub_account(client):
    account_id = "abc123"
    result = client.account.delete_sub_account(account_id)
    client._request.assert_called_with("DELETE", f"/account/sub/{account_id}")
    assert result["status"] == "success"