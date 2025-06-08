#!/usr/bin/env python3
"""
Test MCP tools directly to verify they work with real API data
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_mcp_tools():
    """Test the MCP tools directly."""
    print("🚀 Starting MCP tools test...")
    try:
        from src.server import iso_client
        print("✅ Imported iso_client")
        
        print("🔥 Testing get_marginal_fuel...")
        marginal_fuels = await iso_client.get_marginal_fuels()
        print(f"✅ Marginal fuels: {marginal_fuels}")
        
        # Test the actual MCP tool functions
        print("\n🎯 Testing MCP tool: get_marginal_fuel()")
        from src.server import get_marginal_fuel
        result1 = await get_marginal_fuel()
        print(f"📝 Result: {result1}")
        
        print("\n🎯 Testing MCP tool: get_full_fuel_mix()")
        from src.server import get_full_fuel_mix
        result2 = await get_full_fuel_mix()
        print(f"📝 Result:\n{result2}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
