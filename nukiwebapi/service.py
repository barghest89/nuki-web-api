class Service:
    """Sub-client for managing services."""

    def __init__(self, client):
        self.client = client

    # ---- Services ----
    def list_services(self, service_ids: list[str] | None = None) -> list[dict]:
        """Get a list of services.

        GET /service

        Args:
            service_ids (list[str], optional): Filter for service IDs. Will be
                joined into a comma-separated string (e.g. ["airbnb", "guesty"]).

        Returns:
            list[dict]: List of service objects.
        """
        params = {}
        if service_ids:
            params["serviceIds"] = ",".join(service_ids)
        return self.client._request("GET", "/service", params=params or None)

    def get_service(self, service_id: str) -> dict:
        """Get a specific service.

        GET /service/{serviceId}

        Args:
            service_id (str): The service ID.

        Returns:
            dict: A service object containing fields like:
                - context (dict)
                - enabled (bool)
                - started (bool)
                - stopped (bool)
        """
        return self.client._request("GET", f"/service/{service_id}")

    def link_service(self, service_id: str, data: dict | None = None) -> str:
        """Link a service.

        POST /service/{serviceId}/link

        Args:
            service_id (str): The service ID.
            data (dict, optional): Payload for linking (may be empty).

        Returns:
            str: A confirmation message from the API.
        """
        return self.client._request(
            "POST", f"/service/{service_id}/link", json=data or {}
        )

    def sync_service(self, service_id: str, data: dict | None = None) -> None:
        """Sync a service.

        POST /service/{serviceId}/sync

        Args:
            service_id (str): The service ID.
            data (dict, optional): Payload for syncing (may be empty).

        Returns:
            None: On success, the API returns HTTP 204 (no content).
        """
        return self.client._request(
            "POST", f"/service/{service_id}/sync", json=data or {}
        )

    def unlink_service(self, service_id: str, data: dict | None = None) -> None:
        """Unlink a service.

        POST /service/{serviceId}/unlink

        Args:
            service_id (str): The service ID.
            data (dict, optional): Payload for unlinking (may be empty).

        Returns:
            None: On success, the API returns HTTP 204 (no content).
        """
        return self.client._request(
            "POST", f"/service/{service_id}/unlink", json=data or {}
        )
