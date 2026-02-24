from unittest.mock import patch, call, Mock
import pytest

from nukiwebapi.smartlock_instance import SmartlockInstance


def test_metadata_properties():
    data = {
        "name": "Front Door",
        "state": {"state": 1, "batteryCharge": 85},
        "config": {"name": "Config Name"}
    }
    instance = SmartlockInstance(client=None, smartlock_id=12345, data=data)

    # name property
    assert instance.name == "Front Door"

    # state property
    assert instance.state == data["state"]

    # battery_charge property
    assert instance.battery_charge == 85

    # is_locked property
    assert instance.is_locked is True


def test_hex_id_calculation():
    instance = SmartlockInstance(client=None, smartlock_id=0x51A2B3C4D)
    # Hex representation skips first digit
    assert instance.hex_id == "1A2B3C4D"



def test_refresh_calls_request(client):
    instance = SmartlockInstance(client, smartlock_id=123)

    mock_response = Mock()
    mock_response.json.return_value = {"id": 123, "state": {"state": 0}}

    with patch.object(client, "_request", return_value=mock_response) as mock_request:
        result = instance.refresh()

        mock_request.assert_called_once_with("GET", "/smartlock/123")
        assert result["id"] == 123


def test_lock_calls_action(client):
    instance = SmartlockInstance(client, smartlock_id=123)
    with patch.object(instance, "_action") as mock_action:
        mock_action.return_value = {"status": "locked"}
        result = instance.lock()
        mock_action.assert_called_once_with(2, option = None)
        assert result["status"] == "locked"

    # full lock
    with patch.object(instance, "_action") as mock_action:
        mock_action.return_value = {"status": "full_locked"}
        result = instance.lock(full=True)
        mock_action.assert_called_once_with(2, option=4)
        assert result["status"] == "full_locked"
        assert result["status"] == "full_locked"


def test_unlock_calls_action(client):
    instance = SmartlockInstance(client, smartlock_id=123)
    with patch.object(instance, "_action") as mock_action:
        mock_action.return_value = {"status": "unlocked"}
        result = instance.unlock()
        mock_action.assert_called_once_with(1, option = None)
        assert result["status"] == "unlocked"


def test_unlatch_calls_action(client):
    instance = SmartlockInstance(client, smartlock_id=123)
    with patch.object(instance, "_action") as mock_action:
        mock_action.return_value = {"status": "unlatched"}
        result = instance.unlatch()
        mock_action.assert_called_once_with(3)
        assert result["status"] == "unlatched"


def test_lock_and_go_calls_action(client):
    instance = SmartlockInstance(client, smartlock_id=123)

    # without unlatch
    with patch.object(instance, "_action") as mock_action:
        mock_action.return_value = {"status": "locked_go"}
        result = instance.lock_and_go()
        mock_action.assert_called_once_with(4)
        assert result["status"] == "locked_go"

    # with unlatch
    with patch.object(instance, "_action") as mock_action:
        mock_action.return_value = {"status": "locked_go_unlatch"}
        result = instance.lock_and_go(unlatch=True)
        mock_action.assert_called_once_with(5)
        assert result["status"] == "locked_go_unlatch"


def test_action_calls_client_request(client):
    instance = SmartlockInstance(client, smartlock_id=123)

    with patch.object(client, "_request") as mock_request, \
         patch.object(instance, "refresh") as mock_refresh:

        mock_request.return_value = {"status": "ok"}

        result = instance._action(42)

        mock_request.assert_called_once_with(
            "POST",
            "/smartlock/123/action",
            json={"action": 42},
        )
        mock_refresh.assert_called_once()
        assert result["status"] == "ok"


def test_action_includes_option(client):
    """_action should include 'option' in payload if provided."""
    instance = SmartlockInstance(client, smartlock_id=123)

    with patch.object(client, "_request") as mock_request, \
         patch.object(instance, "refresh") as mock_refresh:

        mock_request.return_value = {"status": "ok"}

        result = instance._action(action=2, option=4)

        mock_request.assert_called_once_with(
            "POST",
            "/smartlock/123/action",
            json={"action": 2, "option": 4},
        )

        mock_refresh.assert_called_once()
        assert result["status"] == "ok"

def test_raw_data_property():
    """raw_data property returns the internal _data dictionary."""
    initial_data = {"id": 123, "state": {"state": 1}}
    instance = SmartlockInstance(client=None, smartlock_id=123, data=initial_data)

    # Access the property
    data = instance.raw_data
    assert data == initial_data

    # Modify internal _data and verify property updates
    instance._data["state"]["state"] = 0
    assert instance.raw_data["state"]["state"] == 0