class AdvancedApi:
    """Sub-client for managing advanced API functionality."""

    def __init__(self, client):
        self.client = client

    # ---- Decentralized Webhooks ----
    def list_decentral_webhooks(self):
        """Get all registered decentral webhooks.

        GET /api/decentralWebhook
        """
        return self.client._request("GET", "/api/decentralWebhook")

    def create_decentral_webhook(self, webhook_url: str, webhook_features: list[str]):
        """
        Create a new decentral webhook.

        PUT /api/decentralWebhook

        Args:
            webhook_url (str): The HTTPS URL where webhooks should point to (required).
            webhook_features (list[str]): List of features to trigger webhooks. Must be subset of:
                ["DEVICE_STATUS", "DEVICE_MASTERDATA", "DEVICE_CONFIG",
                 "DEVICE_LOGS", "DEVICE_AUTHS", "ACCOUNT_USER"]

        Returns:
            dict: API response
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
            "webhookFeatures": list(set(webhook_features))  # unique
        }

        return self.client._request("PUT", "/api/decentralWebhook", json=payload)

    def delete_decentral_webhook(self, webhook_id):
        """Unregister a decentral webhook.

        DELETE /api/decentralWebhook/{id}
        """
        return self.client._request("DELETE", f"/api/decentralWebhook/{webhook_id}")

    def get_webhook_logs(self, api_key_id):
        """Get a list of webhook logs for a given API key (descending).

        GET /api/key/{apiKeyId}/webhook/logs
        """
        return self.client._request("GET", f"/api/key/{api_key_id}/webhook/logs")

    # ---- Smartlock Advanced Authorizations ----
    def create_smartlock_auth_advanced(self, auth_data):
        """Create asynchronous smartlock authorizations.

        PUT /smartlock/auth/advanced
        """
        return self.client._request("PUT", "/smartlock/auth/advanced", json=auth_data)

    def action_smartlock_advanced(self, smartlock_id, action_data):
        """Execute a smartlock action with callback.

        POST /smartlock/{smartlockId}/action/advanced
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/action/advanced", json=action_data
        )

    def lock_smartlock_advanced(self, smartlock_id, lock_data=None):
        """Lock a smartlock (advanced).

        POST /smartlock/{smartlockId}/action/lock/advanced
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/action/lock/advanced", json=lock_data or {}
        )

    def unlock_smartlock_advanced(self, smartlock_id, unlock_data=None):
        """Unlock a smartlock (advanced).

        POST /smartlock/{smartlockId}/action/unlock/advanced
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/action/unlock/advanced", json=unlock_data or {}
        )
