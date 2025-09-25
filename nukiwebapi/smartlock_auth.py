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

    def create_auth_for_smartlocks(
        self,
        name: str,
        smartlock_ids: List[int],
        remote_allowed: bool,
        allowed_from_date: Optional[str] = None,
        allowed_until_date: Optional[str] = None,
        allowed_week_days: Optional[int] = None,
        allowed_from_time: Optional[int] = None,
        allowed_until_time: Optional[int] = None,

        account_user_id: Optional[int] = None,
            smart_actions_enabled: Optional[bool] = None,
        type: Optional[int] = 0,
        code: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create asynchronous smartlock authorizations.

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
            "type": type,
        }

        if smart_actions_enabled is not None:
            payload["smartActionsEnabled"] = smart_actions_enabled
        if code is not None:
            payload["code"] = code

        return self.client._request("PUT", "/smartlock/auth", json=payload)

    def update_auth(
        self,
        id: int,
        name: str,
        smartlockId:int,
        allowed_from_date: Optional[str] = None,
        allowed_until_date: Optional[str] = None,
        allowed_week_days: Optional[int] = None,
        allowed_from_time: Optional[int] = None,
        allowed_until_time: Optional[int] = None,
        account_user_id: Optional[int] = None,
        enabled: Optional[bool] = None,
        remote_allowed: Optional[bool] = None,
        code: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update a single smartlock authorization asynchronously.

        POST /smartlock/{smartlockId}/auth/{id}
        """
        payload = {"name": name}
        if allowed_from_date is not None:
            payload["allowedFromDate"] = allowed_from_date
        if allowed_until_date is not None:
            payload["allowedUntilDate"] = allowed_until_date
        if allowed_week_days is not None:
            payload["allowedWeekDays"] = allowed_week_days
        if allowed_from_time is not None:
            payload["allowedFromTime"] = allowed_from_time
        if allowed_until_time is not None:
            payload["allowedUntilTime"] = allowed_until_time
        if account_user_id is not None:
            payload["accountUserId"] = account_user_id
        if enabled is not None:
            payload["enabled"] = enabled
        if remote_allowed is not None:
            payload["remoteAllowed"] = remote_allowed
        if code is not None:
            payload["code"] = code
        return self.client._request("POST", f"/smartlock/{smartlockId}/auth/{id}", json=payload)

    def update_auth_bulk(
        self,
        auth_list: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Update multiple smartlock authorizations asynchronously.

        POST /smartlock/auth
        """
        return self.client._request("POST", "/smartlock/auth", json=auth_list)

    def delete_auth(self, id: str) -> Dict[str, Any]:
        """Delete smartlock authorizations asynchronously.

        DELETE /smartlock/auth
        """
        ids = [id]
        return self.client._request("DELETE", "/smartlock/auth", json=ids)

    #TODO add test case
    def delete_auths(self, ids: List[str]) -> Dict[str, Any]:
        """Delete smartlock authorizations asynchronously.

        DELETE /smartlock/auth
        """
        return self.client._request("DELETE", "/smartlock/auth", json=ids)

    # ---- Smartlock-specific authorizations ----
    def list_auths_for_smartlock(self, smartlock_id: int) -> Dict[str, Any]:
        """Get a list of smartlock authorizations for a specific smartlock.

        GET /smartlock/{smartlockId}/auth
        """
        return self.client._request("GET", f"/smartlock/{smartlock_id}/auth").json()

    #TODO add test case
    def create_auth_for_smartlock(
        self,
        smartlock_id: int,
        name: str,
        allowed_from_date: str,
        allowed_until_date: str,
        allowed_week_days: int,
        allowed_from_time: int,
        allowed_until_time: int,
        account_user_id: Optional[int],
        remote_allowed: bool,
        smart_actions_enabled: Optional[bool] = None,
        type: Optional[int] = 0,
        code: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a smartlock authorization for a specific smartlock.

        PUT /smartlock/{smartlockId}/auth
        """
        payload = {
            "name": name,
            "allowedFromDate": allowed_from_date,
            "allowedUntilDate": allowed_until_date,
            "allowedWeekDays": allowed_week_days,
            "allowedFromTime": allowed_from_time,
            "allowedUntilTime": allowed_until_time,
            "accountUserId": account_user_id,
            "remoteAllowed": remote_allowed,
            "type": type,
        }

        if smart_actions_enabled is not None:
            payload["smartActionsEnabled"] = smart_actions_enabled
        if code is not None:
            payload["code"] = code

        return self.client._request("PUT", f"/smartlock/{smartlock_id}/auth", json=payload)

    def generate_shared_key_auth(
        self,
        smartlock_id: int,
        name: str,
        allowed_from_date: Optional[str] = None,
        allowed_until_date: Optional[str] = None,
        allowed_week_days: Optional[int] = None,
        allowed_from_time: Optional[int] = None,
        allowed_until_time: Optional[int] = None,
        account_user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate a smartlock authorization with a shared key.

        POST /smartlock/{smartlockId}/auth/advanced/sharedkey
        """
        payload = {"name": name}
        if allowed_from_date is not None:
            payload["allowedFromDate"] = allowed_from_date
        if allowed_until_date is not None:
            payload["allowedUntilDate"] = allowed_until_date
        if allowed_week_days is not None:
            payload["allowedWeekDays"] = allowed_week_days
        if allowed_from_time is not None:
            payload["allowedFromTime"] = allowed_from_time
        if allowed_until_time is not None:
            payload["allowedUntilTime"] = allowed_until_time
        if account_user_id is not None:
            payload["accountUserId"] = account_user_id

        return self.client._request(
            "POST",
            f"/smartlock/{smartlock_id}/auth/advanced/sharedkey",
            json=payload,
        )

    def get_smartlock_auth(self, smartlock_id: int, auth_id: str) -> Dict[str, Any]:
        """Get a specific smartlock authorization.

        GET /smartlock/{smartlockId}/auth/{id}
        """
        return self.client._request("GET", f"/smartlock/{smartlock_id}/auth/{auth_id}").json()

    def update_smartlock_auth(
        self,
        smartlock_id: int,
        auth_id: str,
        name: str,
        allowed_from_date: Optional[str] = None,
        allowed_until_date: Optional[str] = None,
        allowed_week_days: Optional[int] = None,
        allowed_from_time: Optional[int] = None,
        allowed_until_time: Optional[int] = None,
        account_user_id: Optional[int] = None,
        enabled: Optional[bool] = None,
        remote_allowed: Optional[bool] = None,
        code: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update a specific smartlock authorization asynchronously.

        POST /smartlock/{smartlockId}/auth/{id}
        """
        payload = {"name": name}
        if allowed_from_date is not None:
            payload["allowedFromDate"] = allowed_from_date
        if allowed_until_date is not None:
            payload["allowedUntilDate"] = allowed_until_date
        if allowed_week_days is not None:
            payload["allowedWeekDays"] = allowed_week_days
        if allowed_from_time is not None:
            payload["allowedFromTime"] = allowed_from_time
        if allowed_until_time is not None:
            payload["allowedUntilTime"] = allowed_until_time
        if account_user_id is not None:
            payload["accountUserId"] = account_user_id
        if enabled is not None:
            payload["enabled"] = enabled
        if remote_allowed is not None:
            payload["remoteAllowed"] = remote_allowed
        if code is not None:
            payload["code"] = code

        return self.client._request(
            "POST", f"/smartlock/{smartlock_id}/auth/{auth_id}", json=payload
        ).json()

    def delete_smartlock_auth(self, smartlock_id: int, auth_id: str) -> Dict[str, Any]:
        """Delete a specific smartlock authorization asynchronously.

        DELETE /smartlock/{smartlockId}/auth/{id}
        """
        return self.client._request(
            "DELETE", f"/smartlock/{smartlock_id}/auth/{auth_id}"
        )
    #TODO add test case
    def list_auths_paged(
        self,
        page: Optional[int] = 0,
        size: Optional[int] = 100,
        account_user_id: Optional[int] = None,
        types: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a paginated list of smartlock authorizations.

        GET /smartlock/auth/paged
        """
        params = {"page": page, "size": size}
        if account_user_id is not None:
            params["accountUserId"] = account_user_id
        if types is not None:
            params["types"] = types

        return self.client._request("GET", "/smartlock/auth/paged", params=params)