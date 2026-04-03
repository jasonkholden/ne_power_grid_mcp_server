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

@mcp.tool()
async def get_hourly_load_forecast(day: str = None) -> str:
    """
    Get the hourly load forecast for the New England power grid.

    Returns the forecasted electricity demand (load) for each hour of the
    specified day, in megawatts (MW). Defaults to tomorrow's forecast.

    Args:
        day: Optional date in YYYYMMDD format (e.g. "20260314"). Defaults to tomorrow.

    Returns:
        A formatted string with the hourly load forecast data.
    """
    try:
        forecast_data = await iso_client.get_hourly_load_forecast(day)

        forecasts = forecast_data["HourlyLoadForecasts"]["HourlyLoadForecast"]

        if not forecasts:
            return "No hourly load forecast data is currently available."

        creation_date = forecasts[0]["CreationDate"] if forecasts else "Unknown"
        result = f"Hourly Load Forecast (created {creation_date}):\n\n"
        result += f"{'Hour':<22} {'Load MW':>10} {'Net MW':>10}\n"
        result += f"{'─'*22} {'─'*10} {'─'*10}\n"

        for entry in forecasts:
            begin_date = entry["BeginDate"]
            load_mw = entry["LoadMw"]
            net_load_mw = entry["NetLoadMw"]
            result += f"{begin_date:<22} {load_mw:>10,.0f} {net_load_mw:>10,.0f}\n"

        peak = max(forecasts, key=lambda e: e["NetLoadMw"])
        low = min(forecasts, key=lambda e: e["NetLoadMw"])
        result += f"\nPeak: {peak['NetLoadMw']:,.0f} MW at {peak['BeginDate']}\n"
        result += f" Low: {low['NetLoadMw']:,.0f} MW at {low['BeginDate']}\n"

        return result

    except Exception as e:
        logger.error(f"Error getting hourly load forecast: {e}")
        return f"Error retrieving hourly load forecast data: {str(e)}"

@mcp.tool()
async def get_system_load_with_btm_solar(day: str = None) -> str:
    """
    Get the system load for the New England power grid, including
    estimated behind-the-meter (BTM) solar generation.

    Returns 5-minute interval data for the specified day with grid load,
    native load, and the estimated BTM solar output in megawatts (MW).
    BTM solar is derived as: SystemLoadBtmPv - LoadMw.

    Args:
        day: Optional date in YYYYMMDD format (e.g. "20260313"). Defaults to today.

    Returns:
        A formatted table with system load and BTM solar data.
    """
    try:
        data = await iso_client.get_five_minute_system_load(day)

        entries = data["FiveMinSystemLoads"]["FiveMinSystemLoad"]

        if not entries:
            return "No system load data is currently available."

        result = f"System Load with BTM Solar ({entries[0]['BeginDate'][:10]}):\n\n"
        result += f"{'Time':<10} {'Grid MW':>10} {'Native MW':>10} {'ARD MW':>8} {'BTM Solar MW':>12}\n"
        result += f"{'─'*10} {'─'*10} {'─'*10} {'─'*8} {'─'*12}\n"

        for entry in entries:
            time = entry["BeginDate"][11:19]
            load_mw = entry["LoadMw"]
            native = entry["NativeLoad"]
            ard = entry["ArdDemand"]
            btm_solar = entry["SystemLoadBtmPv"] - load_mw
            result += f"{time:<10} {load_mw:>10,.1f} {native:>10,.1f} {ard:>8,.1f} {btm_solar:>12,.1f}\n"

        return result

    except Exception as e:
        logger.error(f"Error getting system load: {e}")
        return f"Error retrieving system load data: {str(e)}"

@mcp.tool()
async def get_seven_day_forecast() -> str:
    """
    Get the seven-day capacity forecast for the New England power grid.

    Returns:
        A JSON string representation of the seven-day forecast data.
    """
    try:
        forecast_data = await iso_client.get_seven_day_forecast()
        return json.dumps(forecast_data, indent=2)

    except Exception as e:
        logger.error(f"Error getting seven day forecast: {e}")
        return f"Error retrieving seven day forecast data: {str(e)}"

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
