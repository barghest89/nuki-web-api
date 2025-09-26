from unittest.mock import patch, call


def test_list_brands(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = [{"id": "b1", "name": "BrandA"}]

        result = client.opener.list_brands()

        mock_request.assert_has_calls([
            call("GET", "/opener/brand")
        ])
        assert isinstance(result, list)
        assert result[0]["id"] == "b1"


def test_get_brand(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"id": "b1", "name": "BrandA"}

        result = client.opener.get_brand("b1")

        mock_request.assert_has_calls([
            call("GET", "/opener/brand/b1")
        ])
        assert result["id"] == "b1"


def test_list_intercoms(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = [{"id": "i1", "model": "IntercomX"}]

        # Test default call (no params)
        result = client.opener.list_intercoms()
        mock_request.assert_has_calls([
            call("GET", "/opener/intercom", params=None)
        ])
        assert isinstance(result, list)
        assert result[0]["id"] == "i1"

        # Test with brand_id
        result = client.opener.list_intercoms(brand_id="b1")
        mock_request.assert_called_with("GET", "/opener/intercom", params={"brandId": "b1"})

        # Test with ignore_verified
        result = client.opener.list_intercoms(ignore_verified=True)
        mock_request.assert_called_with("GET", "/opener/intercom", params={"ignoreVerified": True})

        # Test with recently_changed
        result = client.opener.list_intercoms(recently_changed=True)
        mock_request.assert_called_with("GET", "/opener/intercom", params={"recentlyChanged": True})


def test_get_intercom(client):
    with patch.object(client, "_request") as mock_request:
        mock_request.return_value = {"id": "i1", "model": "IntercomX"}

        result = client.opener.get_intercom("i1")

        mock_request.assert_has_calls([
            call("GET", "/opener/intercom/i1")
        ])
        assert result["id"] == "i1"
