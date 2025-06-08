#!/usr/bin/env python3
"""
Convenience script to run the ISO New England MCP Server

This script provides an easy way to start the MCP server with proper error handling.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.server import run_sync

async def main():
    """Run the MCP server with proper error handling."""
    print("🚀 Starting ISO New England MCP Server...")
    print("📡 Server will communicate via JSON-RPC over stdin/stdout")
    print("🔌 Connect this server to an MCP client (like Claude Desktop)")
    print("⚠️  Make sure your ISO_NE_USERNAME and ISO_NE_PASSWORD are set in .env")
    print("=" * 60)
    
    try:
        # Validate environment before starting
        from src.config.settings import settings
        if not settings.validate_credentials():
            print("❌ Error: ISO_NE_USERNAME and ISO_NE_PASSWORD must be set in .env file")
            print("📝 Copy .env.example to .env and add your ISO Express credentials")
            sys.exit(1)
        
        print("✅ Credentials found, starting server...")
        run_sync()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down MCP server...")
    except Exception as e:
        print(f"❌ Error running MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Run synchronously to avoid asyncio conflicts
    try:
        from src.config.settings import settings
        if not settings.validate_credentials():
            print("❌ Error: ISO_NE_USERNAME and ISO_NE_PASSWORD must be set in .env file")
            print("📝 Copy .env.example to .env and add your ISO Express credentials")
            sys.exit(1)
        
        print("🚀 Starting ISO New England MCP Server...")
        print("✅ Credentials found, starting server...")
        run_sync()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down MCP server...")
    except Exception as e:
        print(f"❌ Error running MCP server: {e}", file=sys.stderr)
        sys.exit(1)
