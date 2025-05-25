
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
USERNAME = os.getenv("TWITCH_USERNAME")


def is_stream_live():
    token = "f68ki9rqow62c8x0i325an9fjq90vm"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.twitch.tv/helix/streams?user_login={USERNAME}"
    response = requests.get(url, headers=headers).json()
    return bool(response["data"])
