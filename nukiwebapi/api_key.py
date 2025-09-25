class ApiKey:
    """Sub-client for managing API keys, advanced keys, and tokens."""

    def __init__(self, client):
        self.client = client

    # ---- API Keys ----
    def list_api_keys(self):
        """List all API keys.

        GET /api/key

        Returns:
            list[dict]: List of API key objects.
        """
        return self.client._request("GET", "/api/key")

    def create_api_key(self, key_data: dict):
        """Create a new API key.

        PUT /api/key

        Args:
            key_data (dict): Data for creating the API key.

        Returns:
            dict: Created API key object.
        """
        return self.client._request("PUT", "/api/key", json=key_data)

    def update_api_key(self, api_key_id: int, key_data: dict):
        """Update an existing API key.

        POST /api/key/{apiKeyId}

        Args:
            api_key_id (int): ID of the API key to update.
            key_data (dict): Update data.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("POST", f"/api/key/{api_key_id}", json=key_data)

    def delete_api_key(self, api_key_id: int):
        """Delete an API key.

        DELETE /api/key/{apiKeyId}

        Args:
            api_key_id (int): ID of the API key to delete.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("DELETE", f"/api/key/{api_key_id}")

    # ---- Advanced API Keys ----
    def get_advanced_api_key(self, api_key_id: int):
        """Get details of an advanced API key.

        GET /api/key/{apiKeyId}/advanced

        Args:
            api_key_id (int): ID of the advanced API key.

        Returns:
            dict: Advanced API key object.
        """
        return self.client._request("GET", f"/api/key/{api_key_id}/advanced")

    def create_advanced_api_key(self, api_key_id: int, key_data: dict):
        """Create an advanced API key.

        PUT /api/key/{apiKeyId}/advanced

        Args:
            api_key_id (int): ID of the base API key.
            key_data (dict): Data for creating the advanced API key.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("PUT", f"/api/key/{api_key_id}/advanced", json=key_data)

    def update_advanced_api_key(self, api_key_id: int, key_data: dict):
        """Update an advanced API key.

        POST /api/key/{apiKeyId}/advanced

        Args:
            api_key_id (int): ID of the advanced API key.
            key_data (dict): Update data.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("POST", f"/api/key/{api_key_id}/advanced", json=key_data)

    def delete_advanced_api_key(self, api_key_id: int):
        """Delete an advanced API key.

        DELETE /api/key/{apiKeyId}/advanced

        Args:
            api_key_id (int): ID of the advanced API key.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("DELETE", f"/api/key/{api_key_id}/advanced")

    def reactivate_advanced_api_key(self, api_key_id: int):
        """Reactivate a deactivated advanced API key.

        POST /api/key/{apiKeyId}/advanced/reactivate

        Args:
            api_key_id (int): ID of the advanced API key.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("POST", f"/api/key/{api_key_id}/advanced/reactivate")

    # ---- API Key Tokens ----
    def list_api_key_tokens(self, api_key_id: int):
        """List all tokens for a given API key.

        GET /api/key/{apiKeyId}/token

        Args:
            api_key_id (int): ID of the API key.

        Returns:
            list[dict]: List of API key token objects.
        """
        return self.client._request("GET", f"/api/key/{api_key_id}/token")

    def create_api_key_token(self, api_key_id: int, token_data: dict):
        """Create a token for a given API key.

        PUT /api/key/{apiKeyId}/token

        Args:
            api_key_id (int): ID of the API key.
            token_data (dict): Data for the new token.

        Returns:
            dict: Created API key token object.
        """
        return self.client._request("PUT", f"/api/key/{api_key_id}/token", json=token_data)

    def update_api_key_token(self, api_key_id: int, token_id: str, token_data: dict):
        """Update an API key token.

        POST /api/key/{apiKeyId}/token/{id}

        Args:
            api_key_id (int): ID of the API key.
            token_id (str): ID of the token.
            token_data (dict): Update data.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("POST", f"/api/key/{api_key_id}/token/{token_id}", json=token_data)

    def delete_api_key_token(self, api_key_id: int, token_id: str):
        """Delete an API key token.

        DELETE /api/key/{apiKeyId}/token/{id}

        Args:
            api_key_id (int): ID of the API key.
            token_id (str): ID of the token.

        Returns:
            dict: API response (usually empty with 204 status).
        """
        return self.client._request("DELETE", f"/api/key/{api_key_id}/token/{token_id}")
