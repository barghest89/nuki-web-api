from typing import Any, Dict, List, Optional


class AdvancedApi:
    """Sub-client for managing advanced API functionality."""

    def __init__(self, client):
        self.client = client

    # ---- Decentralized Webhooks ----
    def list_decentral_webhooks(self) -> List[Dict[str, Any]]:
        """
        Get all registered decentral webhooks.

        GET /api/decentralWebhook

        Returns:
            List of webhook objects.
        """
        return self.client._request("GET", "/api/decentralWebhook").json()

    def create_decentral_webhook(self, webhook_url: str, webhook_features: List[str]) -> Dict[str, Any]:
        """
        Create a new decentral webhook.

        PUT /api/decentralWebhook

        Args:
            webhook_url (str): The HTTPS URL to receive webhooks.
            webhook_features (List[str]): Features to trigger webhooks. Must be subset of:
                ["DEVICE_STATUS", "DEVICE_MASTERDATA", "DEVICE_CONFIG",
                 "DEVICE_LOGS", "DEVICE_AUTHS", "ACCOUNT_USER"]

        Returns:
            API response dict.
        """
        if not webhook_url.startswith("https://"):
            raise ValueError("webhook_url must start with https://")

        allowed_features = {
            "DEVICE_STATUS", "DEVICE_MASTERDATA", "DEVICE_CONFIG",
            "DEVICE_LOGS", "DEVICE_AUTHS", "ACCOUNT_USER"
        }

        if not isinstance(webhook_features, list) or not all(f in allowed_features for f in webhook_features):
            raise ValueError(f"webhook_features must be a list containing only allowed values: {allowed_features}")

        payload = {
            "webhookUrl": webhook_url,
            "webhookFeatures": list(set(webhook_features))  # ensure uniqueness
        }

        return self.client._request("PUT", "/api/decentralWebhook", json=payload).json()

    def delete_decentral_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """
        Unregister a decentral webhook.

        DELETE /api/decentralWebhook/{id}

        Args:
            webhook_id (int): ID of the webhook to delete.

        Returns:
            API response dict.
        """
        if not isinstance(webhook_id, int):
            raise ValueError("webhook_id must be an integer")
        return self.client._request("DELETE", f"/api/decentralWebhook/{webhook_id}").json()

    def get_webhook_logs(self, api_key_id: int, id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get a list of webhook logs for a given API key (descending order).

        GET /api/key/{apiKeyId}/webhook/logs

        Args:
            api_key_id (int): API key ID.
            id (str, optional): Filter for older logs.
            limit (int): Maximum number of logs (max 100, default 50).

        Returns:
            List of webhook logs.
        """
        if not isinstance(api_key_id, int):
            raise ValueError("api_key_id must be an integer")
        if limit > 100 or limit < 1:
            raise ValueError("limit must be between 1 and 100")

        params: Dict[str, Any] = {"limit": limit}
        if id:
            params["id"] = id

        return self.client._request(
            "GET",
            f"/api/key/{api_key_id}/webhook/logs",
            params=params
        ).json()

    # ---- Smartlock Advanced Authorizations ----
    def create_smartlock_auth_advanced(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create asynchronous smartlock authorizations.

        PUT /smartlock/auth/advanced

        Args:
            auth_data (dict): Smartlock authorization creation payload.

        Returns:
            API response dict.
        """
        return self.client._request("PUT", "/smartlock/auth/advanced", json=auth_data).json()

    def action_smartlock_advanced(self, smartlock_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a smartlock action with callback.

        POST /smartlock/{smartlockId}/action/advanced

        Args:
            smartlock_id (str): Smartlock ID.
            action_data (dict): Smartlock action payload.

        Returns:
            API response dict.
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/action/advanced", json=action_data
        ).json()

    def lock_smartlock_advanced(self, smartlock_id: str, lock_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Lock a smartlock (advanced).

        POST /smartlock/{smartlockId}/action/lock/advanced

        Args:
            smartlock_id (str): Smartlock ID.
            lock_data (dict, optional): Optional payload.

        Returns:
            API response dict.
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/action/lock/advanced", json=lock_data or {}
        ).json()

    def unlock_smartlock_advanced(self, smartlock_id: str, unlock_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Unlock a smartlock (advanced).

        POST /smartlock/{smartlockId}/action/unlock/advanced

        Args:
            smartlock_id (str): Smartlock ID.
            unlock_data (dict, optional): Optional payload.

        Returns:
            API response dict.
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/action/unlock/advanced", json=unlock_data or {}
        ).json()
