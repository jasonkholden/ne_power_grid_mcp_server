#!/usr/bin/env python3
"""
Run the ISO New England MCP Server with HTTP transport.

This enables remote access to the MCP tools via HTTP endpoints:
- /mcp - Streamable HTTP transport (recommended)
- /sse - Server-Sent Events transport (legacy compatibility)

Environment variables required:
- ISO_NE_USERNAME: ISO New England API username
- ISO_NE_PASSWORD: ISO New England API password
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.server import mcp
from src.config.settings import settings


def main():
    """Run the MCP server with HTTP transport."""
    # Validate credentials
    if not settings.validate_credentials():
        print("ERROR: ISO_NE_USERNAME and ISO_NE_PASSWORD must be set", file=sys.stderr)
        sys.exit(1)

    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8080"))

    print(f"Starting ISO New England MCP Server (Streamable HTTP transport)")
    print(f"Listening on {host}:{port}")
    print(f"MCP endpoint: http://{host}:{port}/mcp")

    # Run with streamable HTTP transport (recommended over legacy SSE)
    mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    main()
