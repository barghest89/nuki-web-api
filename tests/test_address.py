import os
import random
import pytest
from nukiwebapi import NukiWebAPI

API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = int(os.getenv("NUKI_SMARTLOCK_ID", "0"))  # required for address create


@pytest.fixture
def client():
    return NukiWebAPI(API_TOKEN)


@pytest.fixture
def test_address(client):
    """Create an address for testing and tear it down after."""
    name = f"pytest_address_{random.randint(100, 999)}"
    addr = client.address.create_address(name=name, smartlock_ids=[SMARTLOCK_ID])
    addr_id = addr.get("addressId")
    assert addr_id, f"Failed to create test address: {addr}"

    yield addr

    # cleanup
    try:
        client.address.delete_address(addr_id)
    except Exception as e:
        print(f"[WARN] Cleanup failed for address {addr_id}: {e}")


def test_create_and_get_address(client, test_address):
    """Create address and fetch it via list."""
    addr_id = test_address["addressId"]

    addresses = client.address.list_addresses()
    assert any(a["addressId"] == addr_id for a in addresses)


def test_update_address(client, test_address):
    """Update address with new name and settings."""
    addr_id = test_address["addressId"]
    new_name = f"updated_{random.randint(100,999)}"
    settings = {"timezone": "UTC"}

    updated = client.address.update_address(
        addr_id, name=new_name, smartlock_ids=[SMARTLOCK_ID], settings=settings
    )

    assert updated["name"] == new_name
    assert "settings" in updated


def test_create_and_delete_address_unit(client, test_address):
    """Create, list and delete a unit for the address."""
    addr_id = test_address["addressId"]
    unit_name = f"unit_{random.randint(100,999)}"

    created = client.address.create_address_unit(addr_id, name=unit_name)
    unit_id = created.get("id")
    assert unit_id, f"Failed to create unit: {created}"

    # list should contain it
    units = client.address.list_address_units(addr_id)
    assert any(u["id"] == unit_id for u in units)

    # delete single
    client.address.delete_address_unit(addr_id, unit_id)
    units_after = client.address.list_address_units(addr_id)
    assert all(u["id"] != unit_id for u in units_after)


def test_delete_address_units_bulk(client, test_address):
    """Create multiple units and delete them in bulk."""
    addr_id = test_address["addressId"]

    ids = []
    for i in range(2):
        created = client.address.create_address_unit(addr_id, name=f"bulk_unit_{i}")
        ids.append(created["id"])

    assert len(ids) == 2

    client.address.delete_address_units(addr_id, ids)

    remaining = client.address.list_address_units(addr_id)
    for uid in ids:
        assert all(u["id"] != uid for u in remaining)


# --- Invalid input tests ---

def test_create_address_invalid_input(client):
    with pytest.raises(ValueError):
        client.address.create_address("", [SMARTLOCK_ID])
    with pytest.raises(ValueError):
        client.address.create_address("bad", ["not-an-int"])


def test_update_address_invalid_input(client, test_address):
    addr_id = test_address["addressId"]
    with pytest.raises(ValueError):
        client.address.update_address("not-an-int", name="bad")
    with pytest.raises(ValueError):
        client.address.update_address(addr_id, smartlock_ids=["bad"])
    with pytest.raises(ValueError):
        client.address.update_address(addr_id, settings="not-a-dict")


def test_create_address_unit_invalid_input(client, test_address):
    addr_id = test_address["addressId"]
    with pytest.raises(ValueError):
        client.address.create_address_unit("not-an-int", "name")
    with pytest.raises(ValueError):
        client.address.create_address_unit(addr_id, "")


def test_delete_address_units_invalid_input(client, test_address):
    addr_id = test_address["addressId"]
    with pytest.raises(ValueError):
        client.address.delete_address_units("bad", ["id"])
    with pytest.raises(ValueError):
        client.address.delete_address_units(addr_id, [123])  # must be str IDs


def test_delete_address_unit_invalid_input(client, test_address):
    addr_id = test_address["addressId"]
    with pytest.raises(ValueError):
        client.address.delete_address_unit("bad", "id")
    with pytest.raises(ValueError):
        client.address.delete_address_unit(addr_id, 123)
