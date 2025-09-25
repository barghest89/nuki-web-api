class Company:
    """Sub-client for managing companies."""

    def __init__(self, client):
        self.client = client

    def list_companies(self) -> list[dict]:
        """Get a list of companies.

        GET /company

        Returns:
            list[dict]: List of companies, each containing:
                - name (str)
                - email (str)
        """
        return self.client._request("GET", "/company")
