# Model Context Protocol for ISO New England Energy Grid Information

This project implements a Model Context Protocal (MCP) Server for information on New Englands power grid.
Data is sourced from [ISO New England](https://iso-ne.com), which oversees the day-to-day operation of
the New England Power Grid.  This MCP server is built atop the ISO Express web services API from ISO New England, documented at [https://webservices.iso-ne.com/docs/v1.1/]


## What is an MCP Server and Why Do We Need One

An MCP server is a standardized interface to provide "tools" for artificial intelligence models, in particular, large language models (LLMs).  A canonical example is a question to an LLM like "what is the weather in San Fransciso right now?".  An LLM can't answer that on its own.  It needs a "tool" to be able to go and get the weather right now to answer that question

## What do you need to use this MCP Server
You need to create a [free ISO Express account](https://www.iso-ne.com/isoexpress/login) with ISO New England to get a username and password

## What questions can this MCP server answer

Example Question: What is the marginal fuel right now in new england?
Example Answer: The marginal fuel is Natural Gas and Wood 
Internal Implementation: accesses the /genfuelmix/current api endpoint
Note: The marginal fuel is the type of power that will be used if you wanted to use power on the grid right now, how would the grid provide that additional power

## What is the base api for iso-ne
The base api for the iso-new webservices api is [https://webservices.iso-ne.com/api/v1.1]

## Installation and Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your ISO Express credentials:
   ```
   ISO_NE_USERNAME=your_actual_username
   ISO_NE_PASSWORD=your_actual_password
   ```

### 3. Test the Server
Run the test script to verify everything is working:
```bash
python test_server.py
```

## Running the MCP Server

### Option 1: Direct Execution
```bash
python run_mcp_server.py
```

### Option 2: Using the main module
```bash
python main.py
```

The server will communicate via JSON-RPC over stdin/stdout and can be connected to MCP clients like Claude Desktop.

## MCP Client Configuration

### Claude Desktop Configuration
Add this to your Claude Desktop MCP configuration file:

```json
{
  "mcpServers": {
    "iso-newengland": {
      "command": "python",
      "args": ["/path/to/your/iso_newengland_mcp_server/run_mcp_server.py"],
      "env": {
        "ISO_NE_USERNAME": "your_iso_ne_username",
        "ISO_NE_PASSWORD": "your_iso_ne_password"
      }
    }
  }
}
```

Replace `/path/to/your/` with the actual path to your project directory.

## Available Tools

### `get_marginal_fuel()`
Returns the current marginal fuel types for the New England power grid. The marginal fuel is the type of power generation that would be used if additional power was needed on the grid right now.

**Example Usage:**
"What is the marginal fuel right now in New England?"

### `get_full_fuel_mix()`
Returns the complete current generation fuel mix for the New England power grid, including generation amounts in megawatts and which fuels are marginal.

**Example Usage:**
"Show me the complete fuel mix for New England's power grid right now."

## Project Structure

```
iso_newengland_mcp_server/
├── main.py                 # Main entry point
├── run_mcp_server.py       # Convenience script with better error handling
├── test_server.py          # Test script
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── mcp-config.json        # Example MCP client configuration
└── src/
    ├── __init__.py
    ├── server.py          # FastMCP server implementation
    ├── api/
    │   ├── __init__.py
    │   └── iso_ne_client.py   # ISO New England API client
    ├── config/
    │   ├── __init__.py
    │   └── settings.py        # Configuration management
    └── models/
        ├── __init__.py
        └── fuel_mix.py        # Pydantic data models
```

## API Details

This MCP server uses the ISO New England Web Services API v1.1. The base URL is:
```
https://webservices.iso-ne.com/api/v1.1
```

### Endpoints Used
- `/genfuelmix/current` - Current generation fuel mix data

Full endpoint example to get a json result: [https://webservices.iso-ne.com/api/v1.1//genfuelmix/current.json]

### Authentication
The API requires HTTP Basic Authentication over SSL using your ISO Express credentials.

## Troubleshooting

### Common Issues

1. **Missing Credentials Error**
   - Make sure you've created a `.env` file with your ISO Express credentials
   - Verify your username and password are correct

2. **API Authentication Errors**
   - Verify your ISO Express account is active
   - Check that your credentials are correctly set in the `.env` file

3. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Verify you're running from the project root directory