from typing import Any, Dict, Optional


class Account:
    """Sub-client for managing account-level operations, OTP, email, integrations, settings, and sub-accounts."""

    def __init__(self, client):
        self.client = client  # reference to the parent NukiClient

    # ---- Account CRUD ----
    def get(self) -> Dict[str, Any]:
        """
        Get account details.

        GET /account

        Returns:
            Dict[str, Any]: Account representation from the API.
        """
        return self.client._request("GET", "/account").json()

    def update(
        self,
        language: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        profile: Optional[Dict[str, Any]] = None,
        delete_api_tokens: bool = True,
    ) -> Dict[str, Any]:
        """
        Update account details.

        POST /account

        Args:
            language (str): The language code (required).
            email (str, optional): The new email address.
            password (str, optional): The account password (min 7 chars).
            name (str, optional): The account name.
            config (dict, optional): Alexa/Google/OTP configuration.
            profile (dict, optional): Profile details (firstName, lastName, address, etc.).
            delete_api_tokens (bool, optional): Whether to delete existing API tokens if password changes. Defaults to True.

        Returns:
            Dict[str, Any]: Updated account representation from the API.
        """
        body: Dict[str, Any] = {"language": language}
        if email is not None:
            body["email"] = email
        if password is not None:
            if len(password) < 7:
                raise ValueError("Password must be at least 7 characters long")
            body["password"] = password
        if name is not None:
            body["name"] = name
        if config is not None:
            body["config"] = config
        if profile is not None:
            body["profile"] = profile

        return self.client._request(
            "POST",
            "/account",
            params={"deleteApiTokens": delete_api_tokens},
            json=body,
        )

    def delete(self) -> Dict[str, Any]:
        """
        Delete the account.

        DELETE /account

        Returns:
            Dict[str, Any]: API response confirming account deletion.
        """
        return self.client._request("DELETE", "/account")

    # ---- Email ----
    def change_email(self, email: str) -> Dict[str, Any]:
        """
        Trigger an email change request for the account.

        POST /account/email/change

        Args:
            email (str): The new email address to change to.

        Returns:
            Dict[str, Any]: API response indicating the email change request was sent.
        """
        data = {"email": email}
        return self.client._request("POST", "/account/email/change", json=data)

    def verify_email(self) -> Dict[str, Any]:
        """
        Verify the email change using the code sent to the new email.

        POST /account/email/verify

        Returns:
            Dict[str, Any]: API response indicating success or failure of the email verification.
        """
        return self.client._request("POST", "/account/email/verify")

    # ---- Integrations ----
    def list_integrations(self) -> Dict[str, Any]:
        """
        List all integrations for the account.

        GET /account/integration

        Returns:
            Dict[str, Any]: List of integrations for this account.
        """
        return self.client._request("GET", "/account/integration").json()

    def delete_integration(self, apiKeyId: str, tokenId: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete a specific integration or its tokens for the account.

        DELETE /account/integration

        Args:
            apiKeyId (str): ID of the API key to delete.
            tokenId (str, optional): Specific token ID to delete. If not provided, all tokens under the API key will be removed.

        Returns:
            Dict[str, Any]: API response indicating success of the deletion.
        """
        data = {"apiKeyId": apiKeyId}
        if tokenId:
            data["tokenId"] = tokenId
        return self.client._request("DELETE", "/account/integration", json=data)

    # ---- OTP ----
    def create_otp(self) -> str:
        """
        Create a one-time password (OTP) secret for the account.

        PUT /account/otp

        Returns:
            str: The OTP secret (Base32) to be used for generating TOTP codes.
        """
        return self.client._request("PUT", "/account/otp").json()

    def enable_otp(self, otp: str) -> Dict[str, Any]:
        """
        Enable OTP for the account using a TOTP code generated from the secret.

        POST /account/otp

        Args:
            otp (str): Time-based one-time password (TOTP) code generated from the OTP secret.

        Returns:
            Dict[str, Any]: API response indicating success of enabling OTP.
        """
        return self.client._request("POST", "/account/otp", json={"otp": otp})

    def disable_otp(self) -> Dict[str, Any]:
        """
        Disable OTP for the account.

        DELETE /account/otp

        Returns:
            Dict[str, Any]: API response indicating OTP was successfully disabled.
        """
        return self.client._request("DELETE", "/account/otp")

    # ---- Password ----
    def reset_password(self, email: str, deleteApiTokens: bool = True) -> Dict[str, Any]:
        """
        Reset the account password and optionally delete existing API tokens.

        POST /account/password/reset

        Args:
            email (str): The email of the account to reset the password for.
            deleteApiTokens (bool, optional): Whether to delete existing API tokens. Defaults to True.

        Returns:
            Dict[str, Any]: API response indicating success of the password reset.
        """
        data = {"email": email, "deleteApiTokens": deleteApiTokens}
        return self.client._request("POST", "/account/password/reset", json=data)

    # ---- Account Settings ----
    def get_setting(self) -> Dict[str, Any]:
        """
        Get account settings.

        GET /account/setting

        Returns:
            Dict[str, Any]: Account settings from the API.
        """
        return self.client._request("GET", "/account/setting").json()

    def update_setting(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update account settings.

        PUT /account/setting

        Args:
            data (dict): Settings data to update.

        Returns:
            Dict[str, Any]: Updated account settings from the API.
        """
        return self.client._request("PUT", "/account/setting", json=data).json()

    def delete_setting(self) -> Dict[str, Any]:
        """
        Delete a specific account setting.

        DELETE /account/setting

        Returns:
            Dict[str, Any]: API response confirming deletion.
        """
        return self.client._request("DELETE", "/account/setting")

    # ---- Sub-Accounts ----
    def list_sub_accounts(self, email: str = None) -> Dict[str, Any]:
        """
        List all sub-accounts, optionally filtered by email.

        GET /account/sub

        Args:
            email (str, optional): Regex to filter sub-account emails.

        Returns:
            Dict[str, Any]: List of sub-account representations.
        """
        params = {}
        if email:
            params["email"] = email
        return self.client._request("GET", "/account/sub", params=params).json()

    def create_sub_account(
        self,
        email: str,
        password: str,
        name: str,
        rights: int,
        language: str,
        profile: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Create a new sub-account.

        PUT /account/sub

        Args:
            email (str): Sub-account email address.
            password (str): Sub-account password (min 7 characters).
            name (str): Name of the sub-account.
            rights (int): Rights bitmask (0–31).
            language (str): Language code (e.g., "de").
            profile (dict): Sub-account profile with keys:
                - firstName (str)
                - lastName (str)
                - address (str)
                - zip (str)
                - city (str)
                - country (str, 2-letter ISO code)

        Returns:
            Dict[str, Any]: Created sub-account representation from the API.
        """
        payload = {
            "email": email,
            "password": password,
            "name": name,
            "rights": rights,
            "language": language,
            "profile": profile
        }
        return self.client._request("PUT", "/account/sub", json=payload).json()

    def get_sub_account(self, account_id: int) -> Dict[str, Any]:
        """
        Get details of a specific sub-account.

        GET /account/sub/{accountId}

        Args:
            account_id (int): ID of the sub-account to retrieve.

        Returns:
            Dict[str, Any]: Sub-account representation from the API.
        """
        return self.client._request("GET", f"/account/sub/{account_id}").json()

    def update_sub_account(self, account_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific sub-account.

        POST /account/sub/{accountId}

        Args:
            account_id (int): ID of the sub-account to update.
            data (dict): Fields to update (email, password, name, rights, language, profile, etc.)

        Returns:
            Dict[str, Any]: Updated sub-account representation from the API.
        """
        return self.client._request("POST", f"/account/sub/{account_id}", json=data)

    def delete_sub_account(self, account_id: int) -> Dict[str, Any]:
        """
        Delete a specific sub-account.

        DELETE /account/sub/{accountId}

        Args:
            account_id (int): ID of the sub-account to delete.

        Returns:
            Dict[str, Any]: API response confirming deletion.
        """
        return self.client._request("DELETE", f"/account/sub/{account_id}")
