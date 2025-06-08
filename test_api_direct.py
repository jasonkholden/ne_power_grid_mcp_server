#!/usr/bin/env python3
"""
Direct API test script for ISO New England fuel mix endpoint

This script tests the API call directly to see the response format.
Make sure to set your credentials in the .env file first.
"""

import asyncio
import sys
import os
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_api_direct():
    """Test the API call directly."""
    try:
        from src.config.settings import settings
        from src.api.iso_ne_client import ISONewEnglandClient
        
        if not settings.validate_credentials():
            print("❌ Error: Please set ISO_NE_USERNAME and ISO_NE_PASSWORD in .env file")
            print("📝 Copy .env.example to .env and add your real ISO Express credentials")
            return
        
        print("🔧 Testing ISO New England API...")
        print(f"📍 Base URL: {settings.ISO_NE_BASE_URL}")
        print(f"👤 Username: {settings.ISO_NE_USERNAME}")
        print("=" * 50)
        
        client = ISONewEnglandClient()
        
        # Test the current fuel mix endpoint
        print("🔥 Testing fuel mix endpoint...")
        fuel_mix_data = await client.get_current_fuel_mix()
        
        print("✅ Success! Raw API response:")
        import json
        print(json.dumps(fuel_mix_data, indent=2))
        
        print("\n" + "=" * 50)
        print("🎯 Testing marginal fuels extraction...")
        marginal_fuels = await client.get_marginal_fuels()
        print(f"⚡ Marginal fuels: {marginal_fuels}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_direct())
