from unittest.mock import patch, Mock, call

def test_get_token_info(client):
    with patch.object(client, "_request") as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {"tokenId": "T1", "status": "active"}
        mock_request.return_value = mock_response

        result = client.address_token.get_token_info("T1")

        mock_request.assert_called_once_with("GET", "/address/token/T1")
        assert result["status"] == "active"


def test_get_redeemed_token(client):
    with patch.object(client, "_request") as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {"tokenId": "T1", "redeemed": True}
        mock_request.return_value = mock_response

        result = client.address_token.get_redeemed_token("T1")

        mock_request.assert_called_once_with("GET", "/address/token/T1/redeem")
        assert result["redeemed"] is True


def test_redeem_token_with_email(client):
    with patch.object(client, "_request") as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {"status": "redeemed"}
        mock_request.return_value = mock_response

        result = client.address_token.redeem_token("T1", email=True)

        mock_request.assert_called_once_with(
            "POST", "/address/token/T1/redeem", params={"email": True}, json={}
        )
        assert result["status"] == "redeemed"


def test_redeem_token_without_email(client):
    with patch.object(client, "_request") as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {"status": "redeemed"}
        mock_request.return_value = mock_response

        result = client.address_token.redeem_token("T1")

        mock_request.assert_called_once_with(
            "POST", "/address/token/T1/redeem", params={"email": True}, json={}
        )
        assert result["status"] == "redeemed"


def test_list_tokens(client):
    with patch.object(client, "_request") as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = [{"tokenId": "T1"}, {"tokenId": "T2"}]
        mock_request.return_value = mock_response

        result = client.address_token.list_tokens(123)

        mock_request.assert_called_once_with("GET", "/address/123/token")
        assert isinstance(result, list)
        assert len(result) == 2
