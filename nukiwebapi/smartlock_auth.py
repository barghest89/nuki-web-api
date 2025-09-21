from typing import Any, Dict, List, Optional


class SmartlockAuth:
    """Sub-client for managing smartlock authorizations."""

    def __init__(self, client):
        self.client = client

    # ---- Account-level authorizations ----
    def list_auths(self) -> Dict[str, Any]:
        """Get a list of smartlock authorizations for your smartlocks.

        GET /smartlock/auth
        """
        return self.client._request("GET", "/smartlock/auth")

    def create_auth(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates asynchronous smartlock authorizations.

        PUT /smartlock/auth
        """
        return self.client._request("PUT", "/smartlock/auth", json=auth_data)

    def update_auth(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates smartlock authorizations asynchronously.

        POST /smartlock/auth
        """
        return self.client._request("POST", "/smartlock/auth", json=auth_data)

    def delete_auth(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Deletes smartlock authorizations asynchronously.

        DELETE /smartlock/auth
        """
        return self.client._request("DELETE", "/smartlock/auth", json=auth_data)

    def list_auths_paged(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a paginated list of smartlock authorizations for your smartlocks.

        GET /smartlock/auth/paged
        """
        return self.client._request("GET", "/smartlock/auth/paged", params=params)

    # ---- Smartlock-specific authorizations ----
    def list_auths_for_smartlock(self, smartlock_id: str) -> Dict[str, Any]:
        """Get a list of smartlock authorizations for a specific smartlock.

        GET /smartlock/{smartlockId}/auth
        """
        return self.client._request("GET", f"/smartlock/{smartlock_id}/auth")

    def create_auth_for_smartlock(self, smartlock_id: str, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates an asynchronous smartlock authorization for a specific smartlock.

        PUT /smartlock/{smartlockId}/auth
        """
        return self.client._request("PUT", f"/smartlock/{smartlock_id}/auth", json=auth_data)

    def update_auths_for_smartlock(self, smartlock_id: str, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update multiple smartlock authorizations for a smartlock.

        POST /smartlock/{smartlockId}/auth

        Args:
            smartlock_id (str): The smartlock ID.
            updates (list[dict]): List of SmartlockAuthMultiUpdate objects.

        Required fields in each update:
            - id (str): unique ID of the auth
            - name (str): name of the authorization
        """
        if not isinstance(smartlock_id, (str, int)):
            raise ValueError("smartlock_id must be a string or integer")
        if not isinstance(updates, list) or not all(isinstance(u, dict) for u in updates):
            raise ValueError("updates must be a list of dicts")
        for u in updates:
            if "id" not in u or "name" not in u:
                raise ValueError("each update must include 'id' and 'name'")

        return self.client._request("POST", f"/smartlock/{smartlock_id}/auth", json=updates)

    def generate_shared_key_auth(self, smartlock_id: str, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new smartlock auth with a shared key.

        POST /smartlock/{smartlockId}/auth/advanced/sharedkey
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/auth/advanced/sharedkey", json=auth_data
        )

    def get_smartlock_auth(self, smartlock_id: str, auth_id: str) -> Dict[str, Any]:
        """Get a specific smartlock authorization.

        GET /smartlock/{smartlockId}/auth/{id}
        """
        return self.client._request("GET", f"/smartlock/{smartlock_id}/auth/{auth_id}")

    def update_smartlock_auth(self, smartlock_id: str, auth_id: str, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a specific smartlock authorization asynchronously.

        POST /smartlock/{smartlockId}/auth/{id}
        """
        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/auth/{auth_id}", json=auth_data
        )

    def delete_smartlock_auth(self, smartlock_id: str, auth_id: str) -> Dict[str, Any]:
        """Deletes a specific smartlock authorization asynchronously.

        DELETE /smartlock/{smartlockId}/auth/{id}
        """
        return self.client._request("DELETE", f"/smartlock/{smartlock_id}/auth/{auth_id}")
        