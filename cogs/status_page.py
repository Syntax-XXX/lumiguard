import discord
from discord.ext import commands
import threading
from flask import Flask, render_template_string

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>LumiZAP Status</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1b1b2f; color: #eee; padding: 2em; text-align: center; }
        h1 { color: #a78bfa; font-size: 2.5em; }
        .info-box { background: #292947; padding: 1em; border-radius: 10px; margin: 1em auto; max-width: 400px; box-shadow: 0 0 20px rgba(167, 139, 250, 0.2); }
        .info-box strong { color: #93c5fd; font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>Status für Lumination</h1>
    <div class="info-box"><strong>👥 Mitglieder:</strong> {{ members }}</div>
    <div class="info-box"><strong>🏷️ Rollen:</strong> {{ roles }}</div>
    <div class="info-box"><strong>📺 Kanäle:</strong> {{ channels }}</div>
</body>
</html>
'''

app = Flask(__name__)
status_data = {"members": "?", "roles": "?", "channels": "?"}

@app.route("/")
def status_page():
    return render_template_string(HTML_TEMPLATE, **status_data)

class StatusPage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        threading.Thread(target=self.run_flask, daemon=True).start()

    def run_flask(self):
        app.run(host="0.0.0.0", port=6969)

    @commands.command(name="status")
    async def status(self, ctx):
        guild = ctx.guild
        status_data["members"] = guild.member_count
        status_data["roles"] = len(guild.roles)
        status_data["channels"] = len(guild.channels)

        embed = discord.Embed(
            title=f"📊 Serverstatus von {guild.name}",
            description="Live verfügbar unter: http://localhost:6969/",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Mitglieder", value=str(guild.member_count), inline=True)
        embed.add_field(name="Rollen", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Kanäle", value=str(len(guild.channels)), inline=True)
        embed.set_footer(text="LumiWächter Status Seite")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StatusPage(bot))
