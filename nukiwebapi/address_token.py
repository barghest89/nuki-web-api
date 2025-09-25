from typing import Any, Dict, List, Optional


class AddressToken:
    """Sub-client for managing address tokens."""

    def __init__(self, client):
        self.client = client

    # ---- Token Info ----
    def get_token_info(self, token_id: str) -> Dict[str, Any]:
        """
        Get info about a specific address token.

        GET /address/token/{tokenId}

        Args:
            token_id (str): Token ID.

        Returns:
            Token representation as dict.
        """
        if not isinstance(token_id, str):
            raise ValueError("token_id must be a string")

        return self.client._request(
            "GET", f"/address/token/{token_id}"
        ).json()

    def get_redeemed_token(self, token_id: str) -> Dict[str, Any]:
        """
        Get info about a redeemed address token.

        GET /address/token/{tokenId}/redeem

        Args:
            token_id (str): Token ID.

        Returns:
            Redeemed token representation as dict.
        """
        if not isinstance(token_id, str):
            raise ValueError("token_id must be a string")

        return self.client._request(
            "GET", f"/address/token/{token_id}/redeem"
        ).json()

    def redeem_token(self, token_id: str, email: bool = True) -> Dict[str, Any]:
        """
        Redeem an address token.

        POST /address/token/{tokenId}/redeem

        Args:
            token_id (str): Token ID.
            email (bool, optional): Whether to send an email. Defaults to True.

        Returns:
            API response as dict.
        """
        if not isinstance(token_id, str):
            raise ValueError("token_id must be a string")
        if not isinstance(email, bool):
            raise ValueError("email must be a boolean")

        return self.client._request(
            "POST",
            f"/address/token/{token_id}/redeem",
            params={"email": email},
            json={}
        ).json()

    def list_tokens(self, address_id: int) -> List[Dict[str, Any]]:
        """
        Get a list of tokens for a specific address.

        GET /address/{addressId}/token

        Args:
            address_id (int): Address ID.

        Returns:
            List of token representations.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")

        return self.client._request(
            "GET", f"/address/{address_id}/token"
        ).json()
