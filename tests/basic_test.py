

from nukiwebapi import NukiWebAPI
from dotenv import load_dotenv
import os

load_dotenv()  # looks for .env in cwd
API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = os.getenv("NUKI_SMARTLOCK_ID")


def test_basic_1():
    # from nuki_web_api.modules import Smartlock
    print()
    print("NUKI_API_TOKEN is set:", bool(os.getenv("NUKI_API_TOKEN")))
    print("NUKI_SMARTLOCK_ID is set:", bool(os.getenv("NUKI_SMARTLOCK_ID")))
    wapi = NukiWebAPI(API_TOKEN)

    assert wapi.api_key.list_api_keys() is not None
    assert wapi.smartlock_auth.list_auths() is not None
    assert wapi.smartlock_log.list_logs() is not None

    # print(wapi.fetch_smartlocks())
    locks = wapi.lock_instances
    print(locks)
    for lock in locks.values():
        #	print(lock)
        assert (lock.id == SMARTLOCK_ID)
        assert wapi.smartlock_log.list_logs_for_smartlock(lock.id) is not None


        assert lock.name is not None
        assert lock.hex_id is not None
        assert lock.battery_charge is not None

        lock.refresh()
       
        # Minimal auth creation for type 13 (keypad)
        auth = client.smartlock_auth.create_auth(
            name="KeypadAuthTest",
            remote_allowed=True,
            type=13
        )

        print("Created auth:", auth)

        auth_id = auth.get("id")
        if auth_id:
        # Delete the auth
            deleted = client.smartlock_auth.delete_smartlock_auth(SMARTLOCK_ID, auth_id)
            print("Deleted auth:", deleted)
        else:
            print("No auth ID returned; cannot delete.")


