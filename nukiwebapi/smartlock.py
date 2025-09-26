from typing import Any

from nukiwebapi.smartlock_instance import SmartlockInstance


class Smartlock:
    """Sub-client for managing smartlocks."""

    def __init__(self, client):
        self.client = client

    # ---- Smartlocks ----
    def list_smartlocks(self, auth_id: int | None = None, type_: int | None = None) -> dict[str, Any]:
        """Get a list of smartlocks.

        GET /smartlock

        Args:
            auth_id (int, optional): Filter by authorization ID.
            type_ (int, optional): Filter by smartlock type.

        Returns:
            dict: List of smartlocks.
        """
        params = {}
        if auth_id is not None:
            params["authId"] = auth_id
        if type_ is not None:
            params["type"] = type_

        return self.client._request("GET", "/smartlock", params=params or None).json()

    def get_smartlock(self, smartlock_id: int) -> SmartlockInstance:
        """
        Retrieve a smartlock by ID and return a SmartlockInstance wrapper.

        Args:
            smartlock_id (int): The ID of the smartlock.

        Returns:
            SmartlockInstance: An instance with full data and convenience methods.
        """
        # Fetch the full smartlock data
        data = self.client._request("GET", f"/smartlock/{smartlock_id}")
        # Wrap in SmartlockInstance, preserving all API fields
        return SmartlockInstance(self, smartlock_id, data=data)

    def update_smartlock(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update a smartlock.

        POST /smartlock/{smartlockId}

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): Update payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}", json=data or {})

    def delete_smartlock(self, smartlock_id: int) -> None:
        """Delete a smartlock.

        DELETE /smartlock/{smartlockId}

        Args:
            smartlock_id (int): Smartlock ID.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("DELETE", f"/smartlock/{smartlock_id}")

    def action(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Perform an action on a smartlock.

        POST /smartlock/{smartlockId}/action

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): Action payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/action", json=data or {})

    def lock_smartlock(self, smartlock_id: int) -> None:
        """Lock a smartlock.

        POST /smartlock/{smartlockId}/action/lock

        Args:
            smartlock_id (int): Smartlock ID.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/action/lock")

    def unlock_smartlock(self, smartlock_id: int) -> None:
        """Unlock a smartlock.

        POST /smartlock/{smartlockId}/action/unlock

        Args:
            smartlock_id (int): Smartlock ID.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/action/unlock")

    def update_admin_pin(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update the admin PIN.

        POST /smartlock/{smartlockId}/admin/pin

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): PIN payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/admin/pin", json=data or {})

    def update_advanced_config(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update advanced smartlock configuration.

        POST /smartlock/{smartlockId}/advanced/config

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): Advanced config.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/advanced/config", json=data or {})

    def update_opener_advanced_config(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update opener-specific advanced config.

        POST /smartlock/{smartlockId}/advanced/openerconfig

        Args:
            smartlock_id (int): Smartlock (opener) ID.
            data (dict, optional): Opener config.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/advanced/openerconfig", json=data or {})

    def update_smartdoor_advanced_config(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update smartdoor-specific advanced config.

        POST /smartlock/{smartlockId}/advanced/smartdoorconfig

        Args:
            smartlock_id (int): Smartdoor ID.
            data (dict, optional): Smartdoor config.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/advanced/smartdoorconfig", json=data or {})

    def update_config(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update general smartlock config.

        POST /smartlock/{smartlockId}/config

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): Config payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/config", json=data or {})

    def sync_smartlock(self, smartlock_id: int) -> None:
        """Sync smartlock state.

        POST /smartlock/{smartlockId}/sync

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): Sync payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/sync")

    def bulk_web_config(self, data: dict[str, Any] | None = None) -> None:
        """Apply bulk web configuration to smartlocks.

        POST /bulk-web-config

        Args:
            data (dict, optional): Bulk config payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", "/bulk-web-config", json=data or {})

    def update_web_config(self, smartlock_id: int, data: dict[str, Any] | None = None) -> None:
        """Update web config for a smartlock.

        POST /smartlock/{smartlockId}/web/config

        Args:
            smartlock_id (int): Smartlock ID.
            data (dict, optional): Web config payload.

        Returns:
            None: Empty response on success.
        """
        return self.client._request("POST", f"/smartlock/{smartlock_id}/web/config", json=data or {})
