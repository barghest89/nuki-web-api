class Opener:
    """Sub-client for managing intercom/openers."""

    def __init__(self, client):
        self.client = client

    # ---- Intercom Brands ----
    def list_brands(self) -> list[dict]:
        """Get all intercom brands.

        GET /opener/brand

        Returns:
            list[dict]: List of intercom brands with fields:
                - brandId (int)
                - brand (str)
        """
        return self.client._request("GET", "/opener/brand")

    def get_brand(self, brand_id: int) -> dict:
        """Get a specific intercom brand.

        GET /opener/brand/{brandId}

        Args:
            brand_id (int): The brand ID.

        Returns:
            dict: Brand object with fields:
                - brandId (int)
                - brand (str)
        """
        return self.client._request("GET", f"/opener/brand/{brand_id}")

    # ---- Intercom Models ----
    def list_intercoms(
        self,
        brand_id: int | None = None,
        ignore_verified: bool | None = None,
        recently_changed: bool | None = None,
    ) -> list[dict]:
        """Get a list of intercom models.

        GET /opener/intercom

        Args:
            brand_id (int, optional): Filter for brandId. Required if recently_changed is not set.
            ignore_verified (bool, optional): If True, return intercoms ignoring their verified value.
            recently_changed (bool, optional): If True, return all intercoms which were recently updated.

        Returns:
            list[dict]: List of intercom objects with fields:
                - intercomId (int)
                - brandId (int)
                - type (int)
                - model (str)
                - verified (int)
                - conGndBus (str)
                - conBusAudio (str)
                - conAudioout (str)
                - conDoorbellPlus (str)
                - conDoorbellMinus (str)
                - conOpendoor (str)
                - conGndAnalogue (str)
                - busModeSwitch (int)
                - busModeSwitchShortCircuitDuration (int)
                - creationDate (str)
                - updateDate (str)
        """
        params = {}
        if brand_id is not None:
            params["brandId"] = brand_id
        if ignore_verified is not None:
            params["ignoreVerified"] = ignore_verified
        if recently_changed is not None:
            params["recentlyChanged"] = recently_changed
        return self.client._request("GET", "/opener/intercom", params=params or None)

    def get_intercom(self, intercom_id: int) -> dict:
        """Get a specific intercom model.

        GET /opener/intercom/{intercomId}

        Args:
            intercom_id (int): The intercom ID.

        Returns:
            dict: Intercom object with fields:
                - intercomId (int)
                - brandId (int)
                - type (int)
                - model (str)
                - verified (int)
                - conGndBus (str)
                - conBusAudio (str)
                - conAudioout (str)
                - conDoorbellPlus (str)
                - conDoorbellMinus (str)
                - conOpendoor (str)
                - conGndAnalogue (str)
                - busModeSwitch (int)
                - busModeSwitchShortCircuitDuration (int)
                - creationDate (str)
                - updateDate (str)
        """
        return self.client._request("GET", f"/opener/intercom/{intercom_id}")
