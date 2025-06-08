import httpx
import logging
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
    
    async def get_current_fuel_mix(self) -> Dict[str, Any]:
        """Get current generation fuel mix data."""
        url = f"{self.base_url}/genfuelmix/current.json"
        
        logger.info(f"Requesting fuel mix data from: {url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                auth=self.auth,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            return data
    
    async def get_marginal_fuels(self) -> List[str]:
        """Get list of current marginal fuels."""
        fuel_mix_data = await self.get_current_fuel_mix()
        
        # Parse the response using our Pydantic model
        fuel_mix_response = FuelMixResponse(**fuel_mix_data)
        
        # Extract marginal fuels
        marginal_fuels = [
            entry.fuel_category 
            for entry in fuel_mix_response.gen_fuel_mixes.gen_fuel_mix 
            if entry.marginal_flag.upper() == "Y"
        ]
        
        return marginal_fuels
