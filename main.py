#!/usr/bin/env python3
"""
ISO New England MCP Server

This MCP server provides tools to query ISO New England's power grid data,
including current marginal fuel types and generation fuel mix.

Usage:
    python main.py

Environment Variables:
    ISO_NE_USERNAME: Your ISO Express username
    ISO_NE_PASSWORD: Your ISO Express password
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.server import mcp

async def main():
    """Run the MCP server."""
    try:
        await mcp.run()
    except KeyboardInterrupt:
        print("\nShutting down MCP server...")
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
