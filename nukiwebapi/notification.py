class Notification:
    """Sub-client for managing notifications."""

    def __init__(self, client):
        self.client = client

    # ---- Notification CRUD ----
    def list_notifications(self, reference_id: str | None = None) -> list[dict]:
        """Get all notifications attached to your account.

        GET /notification

        Args:
            reference_id (str, optional): Filter by the reference ID to the third-party system.

        Returns:
            list[dict]: List of notification objects containing:
                - notificationId (str)
                - referenceId (str)
                - pushId (str)
                - secret (str)
                - os (int)
                - language (str)
                - status (int)
                - lastActiveDate (str)
                - settings (list[dict])
        """
        params = {"referenceId": reference_id} if reference_id else None
        return self.client._request("GET", "/notification", params=params)

    def create_notification(self, notification_data: dict) -> dict:
        """Create a notification configuration.

        PUT /notification

        Args:
            notification_data (dict): Notification representation.

        Returns:
            dict: Created notification object.
        """
        return self.client._request("PUT", "/notification", json=notification_data)

    def get_notification(self, notification_id: str) -> dict:
        """Get a specific notification configuration.

        GET /notification/{notificationId}

        Args:
            notification_id (str): The unique notification ID.

        Returns:
            dict: Notification object.
        """
        return self.client._request("GET", f"/notification/{notification_id}")

    def update_notification(self, notification_id: str, notification_data: dict) -> dict:
        """Update a notification configuration.

        POST /notification/{notificationId}

        Args:
            notification_id (str): The unique notification ID.
            notification_data (dict): Updated notification representation.

        Returns:
            dict: Updated notification object.
        """
        return self.client._request("POST", f"/notification/{notification_id}", json=notification_data)

    def delete_notification(self, notification_id: str) -> None:
        """Delete a notification configuration.

        DELETE /notification/{notificationId}

        Args:
            notification_id (str): The unique notification ID.

        Returns:
            None
        """
        return self.client._request("DELETE", f"/notification/{notification_id}")
