# server.py
import datetime
from mcp.server.fastmcp import FastMCP
import logging

import requests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import os
from garth.exc import GarthHTTPError

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

# Load environment variables from .env file
load_dotenv()

print(f"Starting Garmin MCP server for {os.getenv('GARMIN_EMAIL')}")

# Load environment variables if defined
email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")
tokenstore = os.getenv("GARMIN_TOKEN_STORE") or "~/.garminconnect"
tokenstore_base64 = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"
api = None

def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        # Using Oauth1 and OAuth2 token files from directory
        print(
            f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...\n"
        )

        # Using Oauth1 and Oauth2 tokens from base64 encoded string
        # print(
        #     f"Trying to login to Garmin Connect using token data from file '{tokenstore_base64}'...\n"
        # )
        # dir_path = os.path.expanduser(tokenstore_base64)
        # with open(dir_path, "r") as token_file:
        #     tokenstore = token_file.read()

        garmin = Garmin()
        garmin.login(tokenstore)

    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            # # Ask for credentials if not set as environment variables
            # if not email or not password:
            #     email, password = get_credentials()

            garmin = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            garmin.login()
            # Save Oauth1 and Oauth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            print(
                f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)\n"
            )
            # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
            token_base64 = garmin.garth.dumps()
            dir_path = os.path.expanduser(tokenstore_base64)
            with open(dir_path, "w") as token_file:
                token_file.write(token_base64)
            print(
                f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)\n"
            )
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error(err)
            return None

    return garmin



api = init_api(email, password)

# Create an MCP server
mcp = FastMCP("Garmin Connect MCP Server")

# Add an addition tool
@mcp.tool()
def fetch_sleep_data(date: str) -> dict:
    """Returns sleep data for a given date
    Args:
        date: str - date in format YYYY-MM-DD
    Returns:
        dict - sleep data
    """
    return api.get_sleep_data(date)

@mcp.tool()
def fetch_sleps_data(date_from: str, date_to: str) -> dict:
    """Returns steps data for the for the given date range
    Args:
        date_from: str - start date in format YYYY-MM-DD
        date_to: str - end date in format YYYY-MM-DD
    Returns:
        dict - steps data
    """
    return api.get_daily_steps(date_from, date_to)

@mcp.tool()
def fetch_activities_data(num_activities: int) -> dict:
    """Returns activitie data for the for the given date range
    Args:
        num_activitie: int - number of activitie to fetch
    Returns:
        dict - workouts data
    """
    activities = api.get_activities(limit=num_activities)
    
    # # Get last fetched workout
    # workout_id = workouts[-1]["workoutId"]
    # workout_name = workouts[-1]["workoutName"]
    
    # downloaded_workouts = []
    # for i in range(num_workouts):
    #     workout_id = workouts[-(i + 1)]["workoutId"]
    #     workout_name = workouts[-(i + 1)]["workoutName"]
        
    #     workout_data = api.download_workout(workout_id)

    #     downloaded_workouts.append(workout_data)

    # return downloaded_workouts
    return activities

@mcp.tool()
def fetch_heart_rate_data(date: str) -> dict:
    """Returns heart rate data for a given date
    Args:
        date: str - date in format YYYY-MM-DD
    Returns:
        dict - heart rate data
    """
    return api.get_rhr_day(date)

@mcp.tool()
def fetch_stress_data(date: str) -> dict:
    """Returns stress data for a given date
    Args:
        date: str - date in format YYYY-MM-DD
    Returns:
        dict - stress data
    """
    return api.get_stress_data(date)

@mcp.tool()
def fetch_body_battery_data(start_date: str, end_date: str) -> dict:
    """Returns body battery data for a given date
    Args:
        start_date: str - start date in format YYYY-MM-DD
        end_date: str - end date in format YYYY-MM-DD
    Returns:
        dict - body battery data
    """
    api.get_body_battery(start_date, end_date)

    

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

 