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
        allowed_from_date: str,
        allowed_until_date: str,
        allowed_week_days: int,
        allowed_from_time: int,
        allowed_until_time: int,
        account_user_id: int,
        smartlock_ids: list[int],
        remote_allowed: bool,
        smart_actions_enabled: bool,
        type: int = 0,
        code: int | None = None,
    ) -> Dict[str, Any]:
        """Creates asynchronous smartlock authorizations.

        PUT /smartlock/auth
        """
        payload = {
            "name": name,
            "allowedFromDate": allowed_from_date,
            "allowedUntilDate": allowed_until_date,
            "allowedWeekDays": allowed_week_days,
            "allowedFromTime": allowed_from_time,
            "allowedUntilTime": allowed_until_time,
            "accountUserId": account_user_id,
            "smartlockIds": smartlock_ids,
            "remoteAllowed": remote_allowed,
            "smartActionsEnabled": smart_actions_enabled,
            "type": type,
        }
        if type == 13 and code is not None:
            payload["code"] = code

        return self.client._request("PUT", "/smartlock/auth", json=payload)

    def update_auth(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates smartlock authorizations asynchronously.

        POST smartlock/auth
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