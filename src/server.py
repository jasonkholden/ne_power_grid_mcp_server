import asyncio
from fastmcp import FastMCP
from .api.iso_ne_client import ISONewEnglandClient
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("ISO New England Energy Grid")

# Initialize the ISO-NE client
iso_client = ISONewEnglandClient()

@mcp.tool()
async def get_marginal_fuel() -> str:
    """
    Get the current marginal fuel types for the New England power grid.
    
    The marginal fuel is the type of power generation that would be used 
    if additional power was needed on the grid right now.
    
    Returns:
        A string describing the current marginal fuel types.
    """
    try:
        marginal_fuels = await iso_client.get_marginal_fuels()
        
        if not marginal_fuels:
            return "No marginal fuels are currently identified."
        
        if len(marginal_fuels) == 1:
            return f"The current marginal fuel is {marginal_fuels[0]}."
        else:
            fuel_list = ", ".join(marginal_fuels[:-1]) + f" and {marginal_fuels[-1]}"
            return f"The current marginal fuels are {fuel_list}."
            
    except Exception as e:
        logger.error(f"Error getting marginal fuel: {e}")
        return f"Error retrieving marginal fuel data: {str(e)}"

@mcp.tool()
async def get_full_fuel_mix() -> str:
    """
    Get the complete current generation fuel mix for the New England power grid.
    
    Returns detailed information about all fuel types currently generating power,
    including generation amounts in megawatts and which fuels are marginal.
    
    Returns:
        A formatted string with the complete fuel mix data.
    """
    try:
        fuel_mix_data = await iso_client.get_current_fuel_mix()
        
        fuel_mix_response = fuel_mix_data["GenFuelMixes"]["GenFuelMix"]
        begin_date = fuel_mix_response[0]["BeginDate"] if fuel_mix_response else "Unknown"
        
        result = f"Generation Fuel Mix as of {begin_date}:\n\n"
        
        for entry in fuel_mix_response:
            fuel_type = entry["FuelCategory"]
            generation_mw = entry["GenMw"]
            is_marginal = entry["MarginalFlag"].upper() == "Y"
            marginal_text = " (MARGINAL)" if is_marginal else ""
            
            result += f"• {fuel_type}: {generation_mw:.1f} MW{marginal_text}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting fuel mix: {e}")
        return f"Error retrieving fuel mix data: {str(e)}"

def run_sync():
    """Run the MCP server synchronously, handling asyncio loop conflicts."""
    try:
        mcp.run()
    except RuntimeError as e:
        if "asyncio is already running" in str(e):
            # Handle case where asyncio loop is already running
            import nest_asyncio
            nest_asyncio.apply()
            mcp.run()
        else:
            raise

if __name__ == "__main__":
    run_sync()
