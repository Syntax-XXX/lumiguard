
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")# type: ignore
GUILD_ID = int(os.getenv("GUILD_ID"))# type: ignore
WILLKOMMEN_CHANNEL_ID = int(os.getenv("WILLKOMMEN_CHANNEL_ID"))# type: ignore
