import httpx
import logging
from datetime import date, timedelta
from typing import Dict, Any, List
from ..config.settings import settings
from ..models.fuel_mix import FuelMixResponse

logger = logging.getLogger(__name__)


class ISONewEnglandClient:
    """Client for ISO New England API."""

    def __init__(self):
        if not settings.validate_credentials():
            raise ValueError("ISO_NE_USERNAME and ISO_NE_PASSWORD environment variables must be set")

        self.base_url = settings.ISO_NE_BASE_URL
        self.auth = (settings.ISO_NE_USERNAME, settings.ISO_NE_PASSWORD)
        self._client = httpx.AsyncClient(
            auth=self.auth,
            headers={"Accept": "application/json"},
            timeout=30.0,
        )

    async def _get(self, endpoint: str) -> Dict[str, Any]:
        """Make an authenticated GET request and return parsed JSON."""
        url = f"{self.base_url}/{endpoint}.json"
        logger.info(f"Requesting: {url}")
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_current_fuel_mix(self) -> Dict[str, Any]:
        """Get current generation fuel mix data."""
        return await self._get("genfuelmix/current")

    async def get_hourly_load_forecast(self, day: str = None) -> Dict[str, Any]:
        """Get hourly load forecast data for a given day.

        Args:
            day: Date string in YYYYMMDD format. Defaults to tomorrow.
        """
        if day is None:
            day = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
        return await self._get(f"hourlyloadforecast/day/{day}")

    async def get_five_minute_system_load(self, day: str = None) -> Dict[str, Any]:
        """Get five-minute system load data including BTM solar estimates.

        Args:
            day: Date string in YYYYMMDD format. Defaults to today.
        """
        if day is None:
            day = date.today().strftime("%Y%m%d")
        return await self._get(f"fiveminutesystemload/day/{day}")

    async def get_marginal_fuels(self) -> List[str]:
        """Get list of current marginal fuels."""
        fuel_mix_data = await self.get_current_fuel_mix()
        fuel_mix_response = FuelMixResponse(**fuel_mix_data)
        return [
            entry.fuel_category
            for entry in fuel_mix_response.gen_fuel_mixes.gen_fuel_mix
            if entry.marginal_flag.upper() == "Y"
        ]

    async def get_seven_day_forecast(self) -> Dict[str, Any]:
        """Get the current Seven-Day Capacity Forecast data."""
        return await self._get("sevendayforecast/current")
