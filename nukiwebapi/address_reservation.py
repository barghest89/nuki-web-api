from typing import Any, Dict, List


class AddressReservation:
    """Sub-client for managing address reservations."""

    def __init__(self, client):
        self.client = client

    # ---- Address Reservations ----
    def list_reservations(self, address_id: int) -> List[Dict[str, Any]]:
        """
        Get a list of reservations for a specific address.

        GET /address/{addressId}/reservation

        Args:
            address_id (int): ID of the address.

        Returns:
            List of reservation representations.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")

        return self.client._request(
            "GET", f"/address/{address_id}/reservation"
        ).json()

    def issue_reservation(self, address_id: int, reservation_id: str) -> Dict[str, Any]:
        """
        Issue authorizations for an address reservation.

        POST /address/{addressId}/reservation/{id}/issue

        Args:
            address_id (int): ID of the address.
            reservation_id (str): Reservation ID to issue authorizations for.

        Returns:
            API response. 204 No Content if successful.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(reservation_id, str):
            raise ValueError("reservation_id must be a string")

        return self.client._request(
            "POST", f"/address/{address_id}/reservation/{reservation_id}/issue"
        )

    def revoke_reservation(self, address_id: int, reservation_id: str) -> Dict[str, Any]:
        """
        Revoke authorizations for an address reservation.

        POST /address/{addressId}/reservation/{id}/revoke

        Args:
            address_id (int): ID of the address.
            reservation_id (str): Reservation ID to revoke authorizations for.

        Returns:
            API response. 204 No Content if successful.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(reservation_id, str):
            raise ValueError("reservation_id must be a string")

        return self.client._request(
            "POST", f"/address/{address_id}/reservation/{reservation_id}/revoke"
        )

    def update_reservation_access_times(
        self, address_id: int, reservation_id: str, access_times: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update access times for a reservation.

        POST /address/{addressId}/reservation/{id}/update/accesstimes

        Args:
            address_id (int): ID of the address.
            reservation_id (str): Reservation ID to update.
            access_times (dict): Dictionary with access times. Example: {"checkInTime": 0, "checkOutTime": 0}

        Returns:
            API response. 204 No Content if successful.
        """
        if not isinstance(address_id, int):
            raise ValueError("address_id must be an integer")
        if not isinstance(reservation_id, str):
            raise ValueError("reservation_id must be a string")
        if not isinstance(access_times, dict):
            raise ValueError("access_times must be a dict")

        return self.client._request(
            "POST",
            f"/address/{address_id}/reservation/{reservation_id}/update/accesstimes",
            json=access_times,
        )
