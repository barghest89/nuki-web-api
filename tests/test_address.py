from time import sleep

from tests.test_constants import SMARTLOCK_ID

def test_list_addresses(client):
    """Test listing addresses."""
    addresses = client.address.list_addresses()
    assert isinstance(addresses, list)


def test_create_address(client):
    """Test creating an address."""
    result = client.address.create_address("Test_Address", [SMARTLOCK_ID])
    assert len(result) > 0


def test_update_address(client):
    """Test updating an address."""
    result = client.address.update_address(123, name="Updated", smartlock_ids=[123], settings={"tz": "UTC"})
    assert result["status"] == "success"
    assert result.get("name") == "Updated"
    assert result.get("smartlockIds") == [123]
    assert result.get("settings") == {"tz": "UTC"}


def test_delete_address(client):
    """Test deleting an address."""
    result = client.address.delete_address(123)
    assert len(result) > 0


def test_list_address_units(client):
    """Test listing units."""
    units = client.address.list_address_units(123)
    assert units["status"] == "success"


def test_create_address_unit(client):
    """Test creating a unit."""
    unit = client.address.create_address_unit(123, "Unit1")
    assert unit["status"] == "success"
    assert unit.get("name") == "Unit1"


def test_delete_address_units(client):
    """Test deleting multiple units."""
    result = client.address.delete_address_units(123, ["u1", "u2"])
    assert result["status"] == "success"


def test_delete_address_unit(client):
    """Test deleting a single unit."""
    result = client.address.delete_address_unit(123, "u1")
    assert result["status"] == "success"