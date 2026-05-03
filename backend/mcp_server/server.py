import asyncio
import os
import sys

# Change event loop policy on Windows for better pipe support
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("TravelPlanningTools")

@mcp.tool()
def get_flights(origin: str, destination: str, date: str) -> str:
    """
    Search for mock flights between two cities.
    :param origin: The departure city.
    :param destination: The destination city.
    :param date: The date of travel (YYYY-MM-DD).
    """
    return (
        f"✈️ Mock Flights from {origin} to {destination} on {date}:\n"
        f"1. SkyBound AI-101 | 08:00 - 10:30 | $245 | Non-stop\n"
        f"2. AeroLink AI-402 | 13:45 - 16:15 | $210 | Non-stop\n"
        f"3. GlobalJet AI-990 | 19:20 - 21:50 | $185 | Non-stop"
    )

@mcp.tool()
def get_hotels(location: str, check_in: str, check_out: str) -> str:
    """
    Search for mock hotels in a location.
    :param location: The city or area to search in.
    :param check_in: Check-in date (YYYY-MM-DD).
    :param check_out: Check-out date (YYYY-MM-DD).
    """
    return (
        f"🏨 Mock Hotels in {location} ({check_in} to {check_out}):\n"
        f"1. The Grand Meridian | ⭐⭐⭐⭐⭐ | $320/night | Breakfast Included\n"
        f"2. Urban Oasis Suites | ⭐⭐⭐⭐ | $185/night | City View\n"
        f"3. Nomadic Stay Hostel | ⭐⭐⭐ | $45/night | Shared Lounge"
    )

@mcp.tool()
def get_activities(location: str) -> str:
    """
    Search for mock activities and tours in a location.
    :param location: The city or area to search in.
    """
    return (
        f"🎡 Mock Activities in {location}:\n"
        f"- Historical Walking Tour | 3 hours | $35\n"
        f"- Sunset Boat Cruise | 2 hours | $60\n"
        f"- Local Foodie Adventure | 4 hours | $85\n"
        f"- Art & Tech Gallery Entry | Flexible | $20"
    )

if __name__ == "__main__":
    # Start the MCP server process (uses stdio transport by default)
    mcp.run()
