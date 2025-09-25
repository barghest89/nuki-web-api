from unittest.mock import patch, call


def test_list_services_without_filter(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = [{"id": "airbnb"}, {"id": "guesty"}]
        result = client.service.list_services()

        mock_request.assert_called_once_with(
            "GET", "/service", params=None
        )
        assert isinstance(result, list)
        assert result[0]["id"] == "airbnb"


def test_list_services_with_filter(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = [{"id": "airbnb"}]
        result = client.service.list_services(["airbnb", "guesty"])

        mock_request.assert_called_once_with(
            "GET", "/service", params={"serviceIds": "airbnb,guesty"}
        )
        assert isinstance(result, list)
        assert result[0]["id"] == "airbnb"


def test_get_service(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {
            "enabled": True,
            "started": True,
            "stopped": False,
        }
        result = client.service.get_service("airbnb")

        mock_request.assert_called_once_with(
            "GET", "/service/airbnb"
        )
        assert result["enabled"] is True


def test_link_service(client):
    payload = {"authToken": "xyz"}
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = "Linked"
        result = client.service.link_service("airbnb", payload)

        mock_request.assert_called_once_with(
            "POST", "/service/airbnb/link", json=payload
        )
        assert result == "Linked"


def test_link_service_without_payload(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = "Linked"
        result = client.service.link_service("airbnb")

        mock_request.assert_called_once_with(
            "POST", "/service/airbnb/link", json={}
        )
        assert result == "Linked"


def test_sync_service(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = None
        result = client.service.sync_service("airbnb")

        mock_request.assert_called_once_with(
            "POST", "/service/airbnb/sync", json={}
        )
        assert result is None


def test_unlink_service(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = None
        result = client.service.unlink_service("airbnb")

        mock_request.assert_called_once_with(
            "POST", "/service/airbnb/unlink", json={}
        )
        assert result is None
