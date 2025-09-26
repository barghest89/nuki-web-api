from typing import Any, Dict, List, Optional


class SmartlockLog:
    """
    Sub-client for retrieving smartlock logs.

    The log endpoints return activity history for smartlocks at either
    the account level (`/smartlock/log`) or for a specific smartlock
    (`/smartlock/{smartlockId}/log`).
    """

    def __init__(self, client):
        self.client = client

    # ---- Account-level logs ----
    def list_logs(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get a list of smartlock logs for all smartlocks in the account.

        GET /smartlock/log

        Args:
            params (dict, optional): Query filters such as:
                - accountUserId (int): Filter by account user ID.
                - fromDate (str): Start date (RFC3339).
                - toDate (str): End date (RFC3339).
                - action (int): Filter by action code.
                - id (str): Return logs older than this ID.
                - limit (int): Max number of logs (default: 20, max: 50).

        Returns:
            list[dict]: List of smartlock log entries.
        """
        return self.client._request("GET", "/smartlock/log", params=params)

    # ---- Smartlock-specific logs ----
    def list_logs_for_smartlock(
        self, smartlock_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get a list of smartlock logs for a specific smartlock.

        GET /smartlock/{smartlockId}/log

        Args:
            smartlock_id (int): The smartlock ID.
            params (dict, optional): Query filters such as:
                - authId (str): Filter by authorization ID.
                - accountUserId (int): Filter by account user ID.
                - fromDate (str): Start date (RFC3339).
                - toDate (str): End date (RFC3339).
                - action (int): Filter by action code.
                - id (str): Return logs older than this ID.
                - limit (int): Max number of logs (default: 20, max: 50).

        Returns:
            list[dict]: List of smartlock log entries.
        """
        return self.client._request(
            "GET", f"/smartlock/{smartlock_id}/log", params=params
        )
