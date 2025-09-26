from typing import Any, Dict, Optional


class SmartlockInstance:
    """
    Represents a single smartlock and its instance-level operations.

    This helper wraps the Smartlock API for a specific smartlock ID and exposes
    convenience methods like `lock()`, `unlock()`, `unlatch()`, and `lock_and_go()`.
    It also keeps the last known data (`_data`) in memory and provides properties
    for easy access (e.g., `name`, `is_locked`, `battery_charge`).
    """

    def __init__(self, client, smartlock_id: int, data: Optional[Dict[str, Any]] = None):
        self.client = client
        self.id: int = smartlock_id
        self._data = data or {}

        # Hex representation of smartlock ID for convenience
        hex_str = f"{smartlock_id:X}"
        self.hex_id: str = f"{smartlock_id:X}"[1:]  if len(hex_str) > 1 else hex_str

    # --- Metadata properties ---

    @property
    def raw_data(self) -> Dict[str, Any]:
        """Return the full last known API data for this smartlock."""
        return self._data

    @property
    def name(self) -> Optional[str]:
        """Return the smartlock name from config if available."""
        return self._data.get("name") or self._data.get("config", {}).get("name")

    @property
    def state(self) -> Optional[Dict[str, Any]]:
        """Return the full state dictionary if available."""
        return self._data.get("state")

    @property
    def battery_charge(self) -> Optional[int]:
        """Return the remaining battery percentage, if known."""
        return self._data.get("state", {}).get("batteryCharge")

    @property
    def is_locked(self) -> bool:
        """True if the smartlock state indicates it is locked."""
        return self._data.get("state", {}).get("state") == 1

    # --- Data sync ---

    def refresh(self) -> Dict[str, Any]:
        """
        Fetch the latest data for this smartlock.

        Returns:
            dict: The latest smartlock state object from the API.
        """
        self._data = self.client._request("GET", f"/smartlock/{self.id}")
        return self._data

    # --- Internal action helper ---

    def _action(self, action: int, option: Optional[int] = None) -> Dict[str, Any]:
        """
        Send an action command to the smartlock.

        Args:
            action (int): Action code (1=unlock, 2=lock, 3=unlatch, 4=lock’n’go, 5=lock’n’go+unlatch).
            option (int, optional): Option mask (2=force, 4=full lock).

        Returns:
            dict: API response.
        """
        payload: Dict[str, Any] = {"action": action}
        if option is not None:
            payload["option"] = option

        response = self.client._request(
            "POST", f"/smartlock/{self.id}/action", json=payload
        )
        self.refresh()
        return response

    # --- Convenience actions ---

    def lock(self, force: bool = False, full: bool = False) -> Dict[str, Any]:
        """
        Lock the smartlock.

        Args:
            force (bool): If True, use force option (option=2).
            full (bool): If True, request a full lock (option=4).

        Returns:
            dict: API response.
        """
        option = 2 if force else 4 if full else None
        return self._action(2, option=option)

    def unlock(self, force: bool = False) -> Dict[str, Any]:
        """
        Unlock the smartlock.

        Args:
            force (bool): If True, use force option (option=2).

        Returns:
            dict: API response.
        """
        option = 2 if force else None
        return self._action(1, option=option)

    def unlatch(self) -> Dict[str, Any]:
        """
        Unlatch the smartlock.

        Returns:
            dict: API response.
        """
        return self._action(3)

    def lock_and_go(self, unlatch: bool = False) -> Dict[str, Any]:
        """
        Perform lock ’n’ go.

        Args:
            unlatch (bool): If True, perform lock ’n’ go with unlatch (action=5).

        Returns:
            dict: API response.
        """
        return self._action(5 if unlatch else 4)
