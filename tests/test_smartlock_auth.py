# tests/test_smartlock_auth_integration.py
import os
import random
from time import sleep

import pytest

from dotenv import load_dotenv

from nukiwebapi import NukiWebAPI

load_dotenv()  # looks for .env in cwd

API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = int(os.getenv("NUKI_SMARTLOCK_ID"))
ACCOUNT_ID = int(os.getenv("NUKI_ACCOUNT_USER_ID") ) # existing account user for tests

@pytest.fixture
def client():
    return NukiWebAPI(API_TOKEN)


def test_list_auths(client):
    """Test listing all authorizations."""
    auths = client.smartlock_auth.list_auths()
    assert auths is not None


def test_create_update_delete_auth(client):
    """Test updating a single auth."""

    teardown(client)
    created = client.account_user.create_account_user("testemail@example.com", "Test User")
    user_id = created.get("accountUserId")
    name = "Test_Auth"
    created = client.smartlock_auth.create_auth_for_smartlocks(smartlock_ids=[SMARTLOCK_ID], name=name,
                                                     allowed_from_date="2025-09-21T21:50:33.306Z",
                                                     allowed_until_date="2026-09-21T21:50:33.306Z", allowed_week_days=127,
                                                     allowed_from_time=0,
                                                     allowed_until_time=0, account_user_id=user_id, remote_allowed=True,
                                                     smart_actions_enabled=True, type=0)


    sleep(7)
    auths = client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
    auth_id=None
    for auth_instance in auths:
        if auth_instance["name"] == name:
            # we found our just created id
            auth_id = auth_instance["id"]
    assert auth_id is not None
    new_name = f"updated_{random.randint(1000,9999)}"

    auth_instance = client.smartlock_auth.get_smartlock_auth(smartlock_id=SMARTLOCK_ID, auth_id=auth_id)
    assert auth_instance is not None
    client.smartlock_auth.update_auth(smartlockId=SMARTLOCK_ID,
            id=auth_id,
            name=new_name,
            remote_allowed=False
    )
    sleep(7)

    new_auth_instance = client.smartlock_auth.get_smartlock_auth(smartlock_id=SMARTLOCK_ID, auth_id=auth_id)

    assert new_auth_instance["name"] == new_name and new_auth_instance["remoteAllowed"] == False
    teardown(client)


def test_bulk_update_auth(client):
    """Test bulk updating auths."""
    teardown(client)

    name = "HelloWorld234"
    client.smartlock_auth.create_auth_for_smartlocks(smartlock_ids=[SMARTLOCK_ID], name=name,
                                                     allowed_from_date="2025-09-21T21:50:33.306Z",
                                                     allowed_until_date="2026-09-21T21:50:33.306Z", allowed_week_days=127,
                                                     allowed_from_time=0,
                                                     allowed_until_time=0, account_user_id=707629236, remote_allowed=True,
                                                     smart_actions_enabled=True, type=0)

    name = "HelloWorld456"
    client.smartlock_auth.create_auth_for_smartlocks(smartlock_ids=[SMARTLOCK_ID], name=name,
                                                     allowed_from_date="2025-09-21T21:50:33.306Z",
                                                     allowed_until_date="2026-09-21T21:50:33.306Z", allowed_week_days=127,
                                                     allowed_from_time=0,
                                                     allowed_until_time=0, remote_allowed=True,
                                                     smart_actions_enabled=True, type=13, code=245869)

    sleep(5)
    auths = client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
    auth_list = []
    i = 1
    for auth_instance in auths:
        if auth_instance["name"].startswith("HelloWorld"):
            # we found our just created id
            auth_list.append(
            {
                "id": auth_instance["id"],  # existing auth ID
                "name": f"Updated Bulk Name {i}",
                "enabled": True,
                "remoteAllowed": True,
                "allowedFromDate": "2025-09-21T12:00:00Z",
                "allowedUntilDate": "2025-09-30T12:00:00Z",
            })
        i += 1

    assert len(auth_list) > 0

    client.smartlock_auth.update_auth_bulk(auth_list)
    sleep(5)
    auths = client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
    for auth_instance in auths:
        assert not auth_instance["name"].startswith("HelloWorld")

    teardown(client)

def teardown(client):
    prefixes = ("HelloWorld", "updated_", "Updated Bulk", "Test_Auth")

    auths = client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
    for auth_instance in auths:
        if auth_instance["name"].startswith(prefixes):
            # we found our just created id
            auth_id = auth_instance["id"]
            client.smartlock_auth.delete_auth(auth_id)
            print(f"deleted auth_instance {auth_instance['name']} with id {auth_id}.")


"""
Not testable at the moment
def test_generate_shared_key_auth(client):
    #Test creating a shared key auth.
    
    name = f"shared_key_{random.randint(1000,9999)}"
    auth = client.smartlock_auth.generate_shared_key_auth(
        smartlock_id=SMARTLOCK_ID,
        name=name
    )
    auth_id = auth.get("id")
    assert auth_id
    # cleanup
    client.smartlock_auth.delete_smartlock_auth(SMARTLOCK_ID, auth_id)
"""
