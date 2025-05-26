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

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
IRC_TOKEN = os.getenv("IRC_TOKEN")
USERNAME = "LumiGuard"
BOT_NICK = "LumiGuard"
CHANNEL = "#lumizap"
DATA_FILE = "data/watchtime.json"
SESSIONS = {}

WATCHTIME_ROLES = {
    100: "🎖️ 100h Zuschauer",
    200: "🏅 200h Ehrenzuschauer"
}

class twitch_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        threading.Thread(target=self.run_irc_bot, daemon=True).start()

    def is_stream_live(self):
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {IRC_TOKEN}" 
        }
        url = f"https://api.twitch.tv/helix/streams?user_login={USERNAME}"
        response = requests.get(url, headers=headers).json()
        return bool(response.get("data"))

    @commands.command(name="live")
    async def live(self, ctx):
        """Zeigt an, ob Lumi gerade auf Twitch live ist."""
        if self.is_stream_live():
            await ctx.send("🟣 Lumi ist gerade **LIVE** auf Twitch! 👉 https://twitch.tv/lumizap")
        else:
            await ctx.send("⚫ Lumi ist momentan **offline**.")

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
            # CAP REQs für volle Features
            s.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
            s.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
            s.send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
            s.send(f"JOIN {CHANNEL}\r\n".encode("utf-8"))
            print(f"[IRC] Verbunden mit {CHANNEL}")

            data = self.load_data()
            last_activity = {}
            last_print = time.time()

            buffer = ""

            while True:
                resp = s.recv(2048).decode("utf-8")
                buffer += resp
                lines = buffer.split("\r\n")
                buffer = lines.pop() 

                for line in lines:
                    if line.startswith("PING"):
                        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                        continue

                    if "PRIVMSG" in line:
                        user = line.split("!", 1)[0][1:]
                        msg_text = line.split(":", 2)[2].strip()
                        now = time.time()

                        if user not in SESSIONS:
                            SESSIONS[user] = now
                        last_activity[user] = now
                        print(f"[IRC] Nachricht von {user}: {msg_text}")

                now = time.time()
                if now - last_print > 300:
                    print(f"[IRC] Aktive Sessions: {len(SESSIONS)}")
                    last_print = now

                for user in list(SESSIONS.keys()):
                    last = last_activity.get(user)
                    if last is None:
                        del SESSIONS[user]
                        continue
                    if now - last > 1800:  # 30 Minuten Inaktivität
                        session_time = int((last - SESSIONS[user]) / 60)
                        data.setdefault(user, {}).setdefault("watchtime_minutes", 0)
                        data[user]["watchtime_minutes"] += session_time
                        print(f"[IRC] {user}: {session_time} Minuten gespeichert")
                        del SESSIONS[user]
                        self.save_data(data)

        except Exception as e:
            print(f"[IRC] Fehler: {e}")
        finally:
            s.close()

    @commands.command(name="verknüpfe")
    async def verknuepfe(self, ctx, twitchname: str):
        data = self.load_data()
        twitchname = twitchname.lower()
        data.setdefault(twitchname, {})
        data[twitchname]["discord"] = str(ctx.author)
        self.save_data(data)
        await ctx.send(f"✅ Twitch-Nutzer **{twitchname}** wurde mit dir verknüpft!")

    @commands.command(name="watchtime")
    async def watchtime(self, ctx, twitchname: str = None):  # type: ignore
        data = self.load_data()

        if twitchname is None:
            # Suche verknüpften Twitchnamen
            twitchname = next((k for k, v in data.items() if v.get("discord") == str(ctx.author)), None)
            if twitchname is None:
                await ctx.send("⚠️ Du hast noch keinen Twitch-Namen verknüpft. Nutze `!verknüpfe <twitchname>`.")
                return

        twitchname = twitchname.lower()
        entry = data.get(twitchname)
        if not entry:
            await ctx.send(f"⚠️ Kein Eintrag für **{twitchname}** gefunden.")
            return

        minutes = entry.get("watchtime_minutes", 0)
        hours = minutes // 60
        await ctx.send(f"🕒 **{twitchname}** hat ca. **{hours} Stunden** Lumi geschaut.")
        if twitchname == ctx.author.name.lower() or entry.get("discord") == str(ctx.author):
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
                except Exception as e:
                    print(f"[Discord Role Error] {e}")

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
            hours = info.get("watchtime_minutes", 0) // 60
            name = info.get("discord", user)
            embed.add_field(name=f"{i}. {name}", value=f"{hours} Stunden", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(twitch_api(bot))
