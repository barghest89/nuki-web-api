from typing import Any, Dict, List, Optional


class Address:
    """Sub-client for managing addresses and address units."""

    def __init__(self, client):
        self.client = client

    # ---- Address CRUD ----
    def list_addresses(self) -> List[Dict[str, Any]]:
        """
        List all addresses.

        GET /address

        Returns:
            List of address representations.
        """
        return self.client._request("GET", "/address").json()

    def create_address(self, name: str, smartlock_ids: List[int]) -> Dict[str, Any]:
        """
        Create a new address.

        PUT /address

        Args:
            name (str): Name of the address (mandatory).
            smartlock_ids (List[int]): List of smartlock IDs (mandatory).

        Returns:
            Created address representation.
        """
        if not name:
            raise ValueError("name is required")
        if not smartlock_ids or not all(isinstance(s, int) for s in smartlock_ids):
            raise ValueError("smartlock_ids must be a non-empty list of integers")

        payload = {"name": name, "smartlockIds": smartlock_ids}
        return self.client._request("PUT", "/address", json=payload).json()

    def update_address(
        self,
        address_id: int,
        name: Optional[str] = None,
        smartlock_ids: Optional[List[int]] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing address.

        POST /address/{addressId}

        Args:
            address_id (int): Address ID (mandatory).
            name (str, optional): New name for the address.
            smartlock_ids (List[int], optional): Updated list of smartlock IDs.
            settings (dict, optional): Address settings.

        Returns:
            Updated address representation.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")

        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if smartlock_ids is not None:
            if not all(isinstance(s, int) for s in smartlock_ids):
                raise ValueError("smartlock_ids must be a list of integers")
            payload["smartlockIds"] = smartlock_ids
        if settings is not None:
            if not isinstance(settings, dict):
                raise ValueError("settings must be a dict")
            payload["settings"] = settings

        return self.client._request("POST", f"/address/{address_id}", json=payload).json()

    def delete_address(self, address_id: int) -> Dict[str, Any]:
        """
        Delete an existing address.

        DELETE /address/{addressId}

        Args:
            address_id (int): Address ID to delete.

        Returns:
            API response.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        return self.client._request("DELETE", f"/address/{address_id}").json()

    # ---- Address Units ----
    def list_address_units(self, address_id: int) -> List[Dict[str, Any]]:
        """
        List all address units for a given address.

        GET /address/{addressId}/unit

        Args:
            address_id (int): Address ID.

        Returns:
            List of address units.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        return self.client._request("GET", f"/address/{address_id}/unit").json()

    def create_address_unit(self, address_id: int, name: str) -> Dict[str, Any]:
        """
        Create a new unit for a given address.

        PUT /address/{addressId}/unit

        Args:
            address_id (int): Address ID.
            name (str): Name of the new unit.

        Returns:
            Created address unit representation.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not name:
            raise ValueError("name is required for creating an address unit")

        payload = {"name": name}
        return self.client._request("PUT", f"/address/{address_id}/unit", json=payload).json()

    def delete_address_units(self, address_id: int, unit_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple units of a given address asynchronously.

        DELETE /address/{addressId}/unit

        Args:
            address_id (int): Address ID.
            unit_ids (List[str]): List of unit IDs to delete.

        Returns:
            API response with request ID and any errors.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(unit_ids, list) or not all(isinstance(u, str) for u in unit_ids):
            raise ValueError("unit_ids must be a list of strings")

        return self.client._request("DELETE", f"/address/{address_id}/unit", json=unit_ids).json()

    def delete_address_unit(self, address_id: int, unit_id: str) -> Dict[str, Any]:
        """
        Delete a specific unit of a given address.

        DELETE /address/{addressId}/unit/{id}

        Args:
            address_id (int): Address ID.
            unit_id (str): Unit ID to delete.

        Returns:
            API response with request ID and any errors.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(unit_id, str):
            raise ValueError("unit_id must be a string")

        return self.client._request("DELETE", f"/address/{address_id}/unit/{unit_id}").json()
