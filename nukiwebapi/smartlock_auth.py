from datetime import datetime
from typing import Any, Dict, Optional


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

    def create_auth(
        self,
        name: str,
        remote_allowed: bool,
        type: int = 13,  # default to keypad for special case
        allowed_from_date: str = "1970-01-01T00:00:00Z",
        allowed_until_date: str = "2099-12-31T23:59:59Z",
        allowed_week_days: int = 127,
        allowed_from_time: int = 0,
        allowed_until_time: int = 1440,
        account_user_id: int = 0,
        smart_actions_enabled: bool = False,
        code: int = 0,
        smartlock_ids: Optional[list[int]] = None
    ) -> Dict[str, Any]:
        """Creates a smartlock authorization. Only `name` and `remote_allowed` are required."""

        payload = {
            "name": name,
            "allowedFromDate": allowed_from_date,
            "allowedUntilDate": allowed_until_date,
            "allowedWeekDays": allowed_week_days,
            "allowedFromTime": allowed_from_time,
            "allowedUntilTime": allowed_until_time,
            "accountUserId": account_user_id,
            "remoteAllowed": remote_allowed,
            "smartActionsEnabled": smart_actions_enabled,
            "type": type,
            "code": code,
        }

        if smartlock_ids is not None:
            payload["smartlockIds"] = smartlock_ids

        return self.client._request("PUT", "/smartlock/auth", json=payload)

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
        return self.client._request("POST", f"/smartlock/{smartlock_id}/auth/{auth_id}", json=auth_data)

    def delete_smartlock_auth(self, smartlock_id: str, auth_id: str) -> Dict[str, Any]:
        """Deletes a specific smartlock authorization asynchronously.

        DELETE /smartlock/{smartlockId}/auth/{id}
        """
        return self.client._request("DELETE", f"/smartlock/{smartlock_id}/auth/{auth_id}")