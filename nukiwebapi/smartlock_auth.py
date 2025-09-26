from typing import Any, Dict, List, Optional


class SmartlockAuth:
    """
    Sub-client for managing smartlock authorizations.

    Supports listing, creating, updating, and deleting authorizations
    at the account level and for specific smartlocks.
    """

    def __init__(self, client):
        self.client = client

    # --- Account-level authorizations ---
    def list_auths(self, account_user_id: Optional[int] = None, types: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all smartlock authorizations for the account.

        GET /smartlock/auth

        Args:
            account_user_id (int, optional): Filter by account user ID.
            types (str, optional): Comma-separated authorization types, e.g., '0,2,3'.

        Returns:
            list[dict]: List of SmartlockAuth objects.
        """
        params = {}
        if account_user_id is not None:
            params["accountUserId"] = account_user_id
        if types is not None:
            params["types"] = types
        return self.client._request("GET", "/smartlock/auth", params=params).json()

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
    ) -> None:
        """Create asynchronous authorizations for multiple smartlocks.

        PUT /smartlock/auth

        Returns:
            None
        """
        payload = {
            "name": name,
            "smartlockIds": smartlock_ids,
            "remoteAllowed": remote_allowed,
            "type": type,
        }
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
        if smart_actions_enabled is not None:
            payload["smartActionsEnabled"] = smart_actions_enabled
        if code is not None:
            payload["code"] = code

        self.client._request("PUT", "/smartlock/auth", json=payload)

    def update_auths_bulk(self, auth_list: List[Dict[str, Any]]) -> None:
        """Update multiple authorizations asynchronously (POST /smartlock/auth).

        Args:
            auth_list (list[dict]): List of authorization update payloads.

        Returns:
            None
        """
        self.client._request("POST", "/smartlock/auth", json=auth_list)

    def delete_auths(self, ids: List[str]) -> None:
        """Delete one or multiple authorizations.

        DELETE /smartlock/auth

        Args:
            ids (list[str]): List of authorization IDs to delete.

        Returns:
            None
        """
        self.client._request("DELETE", "/smartlock/auth", json=ids)

    # --- Smartlock-specific authorizations ---
    def list_auths_for_smartlock(self, smartlock_id: int, types: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get authorizations for a specific smartlock.

        GET /smartlock/{smartlockId}/auth

        Returns:
            list[dict]: List of SmartlockAuth objects for the smartlock.
        """
        params = {"types": types} if types else None
        return self.client._request("GET", f"/smartlock/{smartlock_id}/auth", params=params).json()

    def create_auth_for_smartlock(
        self,
        smartlock_id: int,
        name: str,
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
    ) -> None:
        """Create authorization for a single smartlock.

        PUT /smartlock/{smartlockId}/auth

        Returns:
            None
        """
        payload = {
            "name": name,
            "remoteAllowed": remote_allowed,
            "type": type,
        }
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
        if smart_actions_enabled is not None:
            payload["smartActionsEnabled"] = smart_actions_enabled
        if code is not None:
            payload["code"] = code

        self.client._request("PUT", f"/smartlock/{smartlock_id}/auth", json=payload)

    def get_auth(self, smartlock_id: int, auth_id: str) -> Dict[str, Any]:
        """Get a single authorization.

        GET /smartlock/{smartlockId}/auth/{id}

        Returns:
            dict: SmartlockAuth object.
        """
        return self.client._request("GET", f"/smartlock/{smartlock_id}/auth/{auth_id}")

    def update_auth(
        self,
        smartlock_id: int,
        auth_id: str,
        name: Optional[str] = None,
        allowed_from_date: Optional[str] = None,
        allowed_until_date: Optional[str] = None,
        allowed_week_days: Optional[int] = None,
        allowed_from_time: Optional[int] = None,
        allowed_until_time: Optional[int] = None,
        account_user_id: Optional[int] = None,
        enabled: Optional[bool] = None,
        remote_allowed: Optional[bool] = None,
        code: Optional[int] = None,
    ) -> None:
        """Update a single authorization asynchronously.

        POST /smartlock/{smartlockId}/auth/{id}

        Returns:
            None
        """
        payload = {}
        if name is not None:
            payload["name"] = name
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

        self.client._request("POST", f"/smartlock/{smartlock_id}/auth/{auth_id}", json=payload)

    def delete_auth(self, smartlock_id: int, auth_id: str) -> None:
        """Delete a single authorization.

        DELETE /smartlock/{smartlockId}/auth/{id}

        Returns:
            None
        """
        self.client._request("DELETE", f"/smartlock/{smartlock_id}/auth/{auth_id}")

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
    ) -> None:
        """Generate a shared key authorization.

        POST /smartlock/{smartlockId}/auth/advanced/sharedkey

        Returns:
            None
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

        self.client._request(
            "POST",
            f"/smartlock/{smartlock_id}/auth/advanced/sharedkey",
            json=payload,
        )

    def list_auths_paged(
        self,
        page: int = 0,
        size: int = 100,
        account_user_id: Optional[int] = None,
        types: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a paginated list of authorizations.

        GET /smartlock/auth/paged

        Returns:
            dict: Pagination response with results.
        """
        params = {"page": page, "size": size}
        if account_user_id is not None:
            params["accountUserId"] = account_user_id
        if types is not None:
            params["types"] = types

        return self.client._request("GET", "/smartlock/auth/paged", params=params)
