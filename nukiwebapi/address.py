class Address:
    """Sub-client for managing addresses and address units."""

    def __init__(self, client):
        self.client = client

    # ---- Address CRUD ----
    def list_addresses(self):
        """List all addresses.

        GET /address
        """
        return self.client._request("GET", "/address")

    def create_address(self, name: str, smartlock_ids: list[int]):
        """Create a new address.

        PUT /address

        Args:
            name (str): Name of the address (mandatory).
            smartlock_ids (list[int]): List of smartlock IDs (mandatory).
        """
        if not name:
            raise ValueError("name is required")
        if not smartlock_ids or not all(isinstance(s, int) for s in smartlock_ids):
            raise ValueError("smartlock_ids must be a non-empty list of integers")

        payload = {
            "name": name,
            "smartlockIds": smartlock_ids,
        }
        return self.client._request("PUT", "/address", json=payload)

    def update_address(self, address_id: int, name: str | None = None,
                       smartlock_ids: list[int] | None = None, settings: dict | None = None):
        """Update an existing address.

        POST /address/{addressId}
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")

        payload = {}
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

        return self.client._request("POST", f"/address/{address_id}", json=payload)

    def delete_address(self, address_id: int):
        """Delete an existing address.

        DELETE /address/{addressId}
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")

        return self.client._request("DELETE", f"/address/{address_id}")

    # ---- Address Units ----
    def list_address_units(self, address_id: int):
        """List all address units for a given address.

        GET /address/{addressId}/unit
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")

        return self.client._request("GET", f"/address/{address_id}/unit")

    def create_address_unit(self, address_id: int, name: str):
        """Create a new unit for a given address.

        PUT /address/{addressId}/unit
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not name:
            raise ValueError("name is required for creating an address unit")

        payload = {"name": name}
        return self.client._request("PUT", f"/address/{address_id}/unit", json=payload)

    def delete_address_units(self, address_id: int, unit_ids: list[str]):
        """Delete multiple units of a given address asynchronously.

        DELETE /address/{addressId}/unit

        Args:
            address_id (int): ID of the address.
            unit_ids (list[str]): List of unit IDs to delete.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(unit_ids, list) or not all(isinstance(u, str) for u in unit_ids):
            raise ValueError("unit_ids must be a list of strings")

        return self.client._request("DELETE", f"/address/{address_id}/unit", json=unit_ids)

    def delete_address_unit(self, address_id: int, unit_id: str):
        """Delete a specific unit of a given address.

        DELETE /address/{addressId}/unit/{id}
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(unit_id, str):
            raise ValueError("unit_id must be a string")

        return self.client._request("DELETE", f"/address/{address_id}/unit/{unit_id}")
