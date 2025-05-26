import discord
from discord.ext import commands
import json
import os

DATA_FILE = "data/watchtime.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class Watchtime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="verknüpfe")
    async def verknuepfe(self, ctx, twitchname: str):
        data = load_data()
        data.setdefault(twitchname, {})
        data[twitchname]["discord"] = str(ctx.author)
        save_data(data)
        await ctx.send(f"✅ Twitch-Nutzer **{twitchname}** wurde mit dir verknüpft!")

    @commands.command(name="watchtime")
    async def watchtime(self, ctx, twitchname: str = None):
        data = load_data()
        if twitchname is None:
            twitchname = next((k for k, v in data.items() if v.get("discord") == str(ctx.author)), None)
            if twitchname is None:
                await ctx.send("⚠️ Du hast noch keinen Twitch-Namen verknüpft. Nutze `!verknüpfe <twitchname>`.")
                return

        entry = data.get(twitchname)
        if not entry:
            await ctx.send(f"⚠️ Kein Eintrag für **{twitchname}** gefunden.")
            return

        watch_minutes = entry.get("watchtime_minutes", 0)
        stunden = watch_minutes // 60
        await ctx.send(f"🕒 **{twitchname}** hat ca. **{stunden} Stunden** Lumi geschaut.")

async def setup(bot):
    await bot.add_cog(Watchtime(bot))