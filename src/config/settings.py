import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the ISO New England MCP server."""
    
    ISO_NE_BASE_URL = "https://webservices.iso-ne.com/api/v1.1"
    ISO_NE_USERNAME: Optional[str] = os.getenv("ISO_NE_USERNAME")
    ISO_NE_PASSWORD: Optional[str] = os.getenv("ISO_NE_PASSWORD")
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that required credentials are present."""
        return bool(cls.ISO_NE_USERNAME and cls.ISO_NE_PASSWORD)

settings = Settings()
