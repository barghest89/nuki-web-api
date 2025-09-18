

from nukiwebapi import NukiWebAPI
from dotenv import load_dotenv
import os

load_dotenv()  # looks for .env in cwd
API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = os.getenv("NUKI_SMARTLOCK_ID")


def test_basic_1():
    # from nuki_web_api.modules import Smartlock
    print("NUKI_API_TOKEN is set:", bool(os.getenv("NUKI_API_TOKEN")))
    print("NUKI_SMARTLOCK_ID is set:", bool(os.getenv("NUKI_SMARTLOCK_ID")))

    wapi = NukiWebAPI(API_TOKEN)
    # print(wapi.fetch_smartlocks())
    locks = wapi.lock_instances
    print(locks)
    for lock in locks.values():
        #	print(lock)
        assert (lock.id == SMARTLOCK_ID)
        print(lock.name)  # "Haustür"
        print(lock.hex_id)

        print(lock.is_locked)  # True/False
        print(lock.battery_charge)  # 98

        # lock.unlock()               # send action
        lock.refresh()
        # update metadata from API
        print(wapi.smartlock_log.list_logs_for_smartlock(lock.id))

    # print(wapi.smartlocks)
    print(wapi.api_key.list_api_keys())
    print(wapi.smartlock_auth.list_auths())


