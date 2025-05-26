import os
import json
import socket
import threading
import time
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
USERNAME = "Lumizap"
IRC_TOKEN = "f68ki9rqow62c8x0i325an9fjq90vm"
BOT_NICK = "LumiGuard"
CHANNEL = "#lumizap"
DATA_FILE = "data/watchtime.json"
SESSIONS = {}

WATCHTIME_ROLES = {
    100: "🎖️ 100h Zuschauer",
    200: "🏅 200h Ehrenzuschauer"
}

class TwitchWatchtime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watchtime_thread = threading.Thread(target=self.run_irc_bot, daemon=True)
        self.watchtime_thread.start()

    def is_stream_live(self):
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {IRC_TOKEN}"
        }
        url = f"https://api.twitch.tv/helix/streams?user_login={USERNAME}"
        response = requests.get(url, headers=headers).json()
        return bool(response.get("data"))

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def run_irc_bot(self):
        s = socket.socket()
        try:
            s.connect(("irc.chat.twitch.tv", 6667))
            s.send(f"PASS {IRC_TOKEN}\r\n".encode("utf-8"))
            s.send(f"NICK {BOT_NICK}\r\n".encode("utf-8"))
            s.send(f"JOIN {CHANNEL}\r\n".encode("utf-8"))
            print(f"[IRC] Verbunden mit {CHANNEL}")

            data = self.load_data()
            last_activity = {}

            while True:
                resp = s.recv(2048).decode("utf-8")

                if resp.startswith("PING"):
                    s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    continue

                if "PRIVMSG" in resp:
                    user = resp.split("!", 1)[0][1:]
                    now = time.time()

                    if user not in SESSIONS:
                        SESSIONS[user] = now
                    last_activity[user] = now
                    print(f"[IRC] {user} aktiv")

                now = time.time()
                for user in list(SESSIONS.keys()):
                    if now - last_activity.get(user, 0) > 1800:
                        session_time = int((last_activity[user] - SESSIONS[user]) / 60)
                        data.setdefault(user, {}).setdefault("watchtime_minutes", 0)
                        data[user]["watchtime_minutes"] += session_time
                        print(f"[IRC] {user}: {session_time} Minuten gespeichert")
                        del SESSIONS[user]
                        self.save_data(data)

        except Exception as e:
            print(f"[IRC] Fehler: {e}")
        finally:
            s.close()

    @commands.command(name="watchtime")
    async def watchtime(self, ctx, twitch_user: str = None):# type: ignore
        """Zeigt die Twitch-Watchtime eines Benutzers."""
        data = self.load_data()
        user = twitch_user or ctx.author.name
        info = data.get(user.lower())

        if not info:
            await ctx.send(f"📺 Keine Watchtime für `{user}` gefunden.")
            return

        minutes = info.get("watchtime_minutes", 0)
        hours = minutes // 60
        await ctx.send(f"⏱️ `{user}` hat bereits **{hours} Stunden** Lumi zugeschaut!")

        # Versuche Rolle zu vergeben
        await self.assign_roles(ctx, ctx.author, hours)

    async def assign_roles(self, ctx, member, hours):
        if not isinstance(member, discord.Member):
            try:
                member = await ctx.guild.fetch_member(member.id)
            except:
                return

        for hour, role_name in WATCHTIME_ROLES.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role and hours >= hour and role not in member.roles:
                try:
                    await member.add_roles(role, reason="Automatisch durch Watchtime")
                    await ctx.send(f"🎉 {member.mention} hat die Rolle **{role.name}** erhalten!")
                except:
                    pass

    @commands.command(name="topwatchtime")
    async def topwatchtime(self, ctx):
        """Zeigt die Top 5 Zuschauer mit der meisten Watchtime."""
        data = self.load_data()
        sorted_users = sorted(data.items(), key=lambda x: x[1].get("watchtime_minutes", 0), reverse=True)[:5]

        embed = discord.Embed(
            title="🏆 Top 5 Zuschauer",
            color=discord.Color.purple()
        )
        for i, (user, info) in enumerate(sorted_users, 1):
            hours = info["watchtime_minutes"] // 60
            embed.add_field(name=f"{i}. {user}", value=f"{hours} Stunden", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TwitchWatchtime(bot))
