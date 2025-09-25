from typing import Any, Dict, Optional, Union


class AccountUser:
    """Sub-client for managing account users."""

    ALLOWED_LANGUAGES = {"en", "de", "es", "fr", "it", "nl", "cs", "sk"}

    def __init__(self, client):
        self.client = client

    # ---- Account Users ----
    def list_account_users(self) -> Dict[str, Any]:
        """
        List all account users.

        GET /account/user

        Returns:
            Dict[str, Any]: List of account users.
        """
        return self.client._request("GET", "/account/user").json()

    def create_account_user(
        self,
        email: str,
        name: str,
        type: Optional[int] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new account user.

        PUT /account/user

        Args:
            email (str): Email of the user (mandatory).
            name (str): Name of the user (mandatory).
            type (int, optional): User type, 0 = user, 1 = company.
            language (str, optional): Language code. Allowed: ["en", "de", "es", "fr", "it", "nl", "cs", "sk"]

        Returns:
            Dict[str, Any]: Created account user representation.
        """
        payload = {"email": email, "name": name}

        if type is not None:
            if type not in (0, 1):
                raise ValueError("type must be 0 (user) or 1 (company)")
            payload["type"] = str(type)

        if language is not None:
            if language not in self.ALLOWED_LANGUAGES:
                raise ValueError(f"language must be one of {self.ALLOWED_LANGUAGES}")
            payload["language"] = language

        return self.client._request("PUT", "/account/user", json=payload).json()

    def get_account_user(self, account_user_id: int) -> Dict[str, Any]:
        """
        Get details of a specific account user.

        GET /account/user/{accountUserId}

        Args:
            account_user_id (int): ID of the account user to retrieve.

        Returns:
            Dict[str, Any]: Account user representation.
        """
        return self.client._request("GET", f"/account/user/{account_user_id}").json()

    def update_account_user(
        self,
        account_user_id: int,
        email: str,
        name: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Update details of a specific account user.

        POST /account/user/{accountUserId}

        Args:
            account_user_id (int): ID of the account user to update.
            email (str): New email (mandatory).
            name (str): New name (mandatory).
            language (str): Language code (mandatory). Allowed: ["en", "de", "es", "fr", "it", "nl", "cs", "sk"]

        Returns:
            Dict[str, Any]: Updated account user representation.
        """
        if language not in self.ALLOWED_LANGUAGES:
            raise ValueError(f"language must be one of {self.ALLOWED_LANGUAGES}")

        payload = {
            "email": email,
            "name": name,
            "language": language
        }

        return self.client._request("POST", f"/account/user/{account_user_id}", json=payload).json()

    def delete_account_user(self, account_user_id: int) -> Dict[str, Any]:
        """
        Delete a specific account user asynchronously.

        DELETE /account/user/{accountUserId}

        Args:
            account_user_id (int): ID of the account user to delete.

        Returns:
            Dict[str, Any]: API response confirming deletion.
        """
        return self.client._request("DELETE", f"/account/user/{account_user_id}")
