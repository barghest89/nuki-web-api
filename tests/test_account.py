# tests/test_account.py
import os
import random
import string
from time import sleep, time

import pytest
from unittest.mock import patch, call

import requests
from dotenv import load_dotenv
import pyotp

from nukiwebapi import NukiWebAPI

load_dotenv()  # looks for .env in cwd
API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = os.getenv("NUKI_SMARTLOCK_ID")
TEST_EMAIL_PREFIX = os.getenv("TEST_EMAIL_PREFIX")
ORIGINAL_EMAIL_PREFIX = os.getenv("ORIGINAL_EMAIL_PREFIX")


def test_account_update(nuki_client):
    nuki_client.account.update(language="en", email=f"{TEST_EMAIL_PREFIX}@gmail.com")
    nuki_client.account.update(language="de", email=f"{ORIGINAL_EMAIL_PREFIX}@gmail.com")
    account_data = nuki_client.account.get()
    assert account_data["email"] == f"{ORIGINAL_EMAIL_PREFIX}@gmail.com"
    assert account_data["language"] == "de"



# ---- OTP tests ----
def test_otp_lifecycle_integration(nuki_client):
    acc = nuki_client.account.get()
    config = acc.get("config", {})
    if acc.get("config", {}).get("otpEnabledDate") is not None:
        nuki_client.account.disable_otp()  # Disable first to ensure test status is always the same

    # Step 1: Create OTP secret
    secret = nuki_client.account.create_otp()
    assert isinstance(secret, str)
    assert len(secret) > 10

    # Step 2: Generate TOTP from secret (done only in the test!)
    totp = pyotp.TOTP(secret)

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        code = totp.now()


    # Step 3: Enable OTP using generated code
        try:
            response = nuki_client.account.enable_otp(code)
            if response.status_code == 204:
                return True  # success
            elif response.status_code == 401:
                # Wrong OTP → maybe timing issue
                if attempt < max_retries:
                    time.sleep(1)  # wait a second and retry
                    continue
                else:
                    raise RuntimeError("OTP rejected after max retries")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            if attempt == max_retries:
                raise

    acc = nuki_client.account.get()
    # Step 4: Disable OTP
    assert acc.get("config", {}).get("otpEnabledDate") is not None
    disabled = nuki_client.account.disable_otp()
    acc = nuki_client.account.get()
    assert acc.get("config", {}).get("otpEnabledDate") is None
    return None


# ---- Password reset ----
def test_reset_password(client):
    email = "user@example.com"
    delete_tokens = True

    result = client.account.reset_password(email=email, deleteApiTokens=delete_tokens)
    client._mock_request.assert_called_with(
        "POST",
        "/account/password/reset",
        json={"email": email, "deleteApiTokens": delete_tokens}
    )
    assert result["status"] == "success"


# ---- Account settings ----

def test_update_delete_account_setting_nuki_banner(nuki_client):


    setting = True
    """Test updating account setting: Nuki Club banner dismissed flag."""
    # Prepare payload
    payload = {
        "web": {
            "nukiClubDismissed": setting
        }
    }

    # Update/create the setting
    result = nuki_client.account.update_setting(payload)
    assert isinstance(result, dict)
    # Nuki API usually echoes the updated structure back
    assert "web" in result
    assert result["web"].get("nukiClubDismissed") is setting

    # Fetch to verify persistence
    fetched = nuki_client.account.get_setting()
    assert isinstance(fetched, dict)
    assert "web" in fetched
    assert fetched["web"].get("nukiClubDismissed") is setting
    nuki_client.account.delete_setting()


# ---- Sub-account management ----
def test_create_update_delete_list_sub_accounts(nuki_client):

    email = f"test{str(random.randint(1, 999))}@gmail.com"

    profile_data = {
        "firstName": "Alice",
        "lastName": "Tester",
        "address": "42 Integration Road",
        "zip": "12345",
        "city": "Testville",
        "country": "DE"
    }

    response = nuki_client.account.create_sub_account(
        email=email,
        password="securePass123",
        name="Integration Test Sub",
        rights=31,
        language="de",
        profile=profile_data
    )

    # Assertions based on expected structure
    assert "accountId" in response
    account_id = response["accountId"]

    data = {"name": "Updated"}

    nuki_client.account.update_sub_account(account_id, data)

    account = nuki_client.account.get_sub_account(account_id)

    assert account["name"] == "Updated"

    nuki_client.account.delete_sub_account(account_id)

    # Teardown
    subs = nuki_client.account.list_sub_accounts()
    for sub in subs:
        account_id = sub["accountId"]
        nuki_client.account.delete_sub_account(account_id)


def test_list_integrations(nuki_client):
    response = nuki_client.account.list_integrations()
    assert response is not None

def test_change_email(client):
    result = client.account.change_email("fake_email")
    client._mock_request.assert_called_with("POST", "/account/email/change", json={"email": "fake_email"})
    assert result["status"] == "success"


def test_send_verification_email(client):
    result = client.account.verify_email()
    client._mock_request.assert_called_with("POST", "/account/email/verify")
    assert result["status"] == "success"


# ---- Account integrations ----
def test_delete_integration(client):
    apiKeyId = "abc123"
    tokenId = "deadbeef"
    result = client.account.delete_integration(apiKeyId, tokenId)
    client._mock_request.assert_called_with(
        "DELETE",
        "/account/integration",
        json={"apiKeyId": apiKeyId, "tokenId": tokenId}
    )
    assert result["status"] == "success"
