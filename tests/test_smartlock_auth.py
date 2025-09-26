import os
import random
import time
from time import sleep

import pytest
from dotenv import load_dotenv

from nukiwebapi import NukiWebAPI

load_dotenv()  # looks for .env in cwd

API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = int(os.getenv("NUKI_SMARTLOCK_ID"))
ACCOUNT_ID = int(os.getenv("NUKI_ACCOUNT_USER_ID"))  # existing account user for tests

# --- Helper for retry loops ---
def retry_until(func, timeout=10, interval=1, fail_message="Condition not met within timeout"):
    start = time.time()
    while time.time() - start < timeout:
        result = func()
        if result:
            return result
        time.sleep(interval)
    raise RuntimeError(fail_message)

@pytest.fixture
def client():
    return NukiWebAPI(API_TOKEN)


def teardown(client):
    prefixes = ("HelloWorld", "updated_", "Updated Bulk", "Test_Auth")
    try:
        auths = client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
    except Exception:
        return  # skip if API temporarily unreachable
    for auth_instance in auths:
        name = auth_instance.get("name", "")
        if any(name.startswith(p) for p in prefixes):
            auth_id = auth_instance.get("id")
            if auth_id:
                try:
                    client.smartlock_auth.delete_auth(SMARTLOCK_ID, auth_id)
                    print(f"deleted auth_instance {name} with id {auth_id}.")
                except Exception:
                    continue


def test_create_update_delete_auth(client):
    """Test creating, updating, and deleting a single smartlock auth."""

    teardown(client)

    # Step 1: Create account user
    created_user = client.account_user.create_account_user("testemail@example.com", "Test User")
    user_id = created_user.get("accountUserId")
    assert user_id is not None, "Failed to create account user"

    # Step 2: Create auth
    name = "Test_Auth"
    client.smartlock_auth.create_auth_for_smartlocks(
        smartlock_ids=[SMARTLOCK_ID],
        name=name,
        allowed_from_date="2025-09-21T21:50:33.306Z",
        allowed_until_date="2026-09-21T21:50:33.306Z",
        allowed_week_days=127,
        allowed_from_time=0,
        allowed_until_time=0,
        account_user_id=user_id,
        remote_allowed=True,
        smart_actions_enabled=True,
        type=0,
    )

    # Step 3: Wait for auth to appear
    auth_instance = retry_until(
        lambda: next(
            (a for a in client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID) if a.get("name") == name),
            None,
        ),
        timeout=20,
        interval=2,
        fail_message=f"Auth '{name}' did not appear within timeout",
    )
    auth_id = auth_instance["id"]
    assert auth_id is not None

    # Step 4: Update auth
    new_name = f"updated_{random.randint(1000,9999)}"
    client.smartlock_auth.update_auth(
        smartlock_id=SMARTLOCK_ID,
        auth_id=auth_id,
        name=new_name,
        remote_allowed=False
    )

    # Step 5: Wait for update to propagate
    updated_auth = retry_until(
        lambda: next(
            (
                a for a in client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
                if a.get("id") == auth_id and a.get("name") == new_name
            ),
            None,
        ),
        timeout=20,
        interval=2,
        fail_message=f"Auth '{auth_id}' update did not propagate"
    )

    assert updated_auth["remoteAllowed"] is False

    # Step 6: Cleanup
    teardown(client)


def test_bulk_update_auth(client):
    """Test bulk updating multiple auths."""

    teardown(client)

    # Step 1: Create multiple auths
    names = ["HelloWorld234", "HelloWorld456"]
    for i, name in enumerate(names):
        client.smartlock_auth.create_auth_for_smartlocks(
            smartlock_ids=[SMARTLOCK_ID],
            name=name,
            allowed_from_date="2025-09-21T21:50:33.306Z",
            allowed_until_date="2026-09-21T21:50:33.306Z",
            allowed_week_days=127,
            allowed_from_time=0,
            allowed_until_time=0,
            account_user_id=ACCOUNT_ID if i == 0 else None,
            remote_allowed=True,
            smart_actions_enabled=True,
            type=0 if i == 0 else 13,
            code=None if i == 0 else 245869
        )

    # Step 2: Wait for auths to appear
    auths_to_update = retry_until(
        lambda: [
            a for a in client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
            if a.get("name", "").startswith("HelloWorld")
        ],
        timeout=20,
        interval=2,
        fail_message="Bulk auths did not appear within timeout",
    )



    # Step 3: Prepare bulk update payload
    auth_list = []
    for i, auth_instance in enumerate(auths_to_update, start=1):
        auth_list.append({
            "id": auth_instance["id"],
            "name": f"Updated Bulk Name {i}",
            "enabled": True,
            "remoteAllowed": True,
            "allowedFromDate": "2025-09-21T12:00:00Z",
            "allowedUntilDate": "2025-09-30T12:00:00Z",
        })

    # Step 4: Bulk update
    client.smartlock_auth.update_auths_bulk(auth_list)

    # Step 5: Wait for updates to propagate
    updated_auths = retry_until(
        lambda: [
            a for a in client.smartlock_auth.list_auths_for_smartlock(SMARTLOCK_ID)
            if not a.get("name", "").startswith("HelloWorld")
        ],
        timeout=20,
        interval=2,
        fail_message="Bulk auth updates did not propagate",
    )

    assert len(updated_auths) >= len(auth_list)

    teardown(client)