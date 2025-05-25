import os
import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.remove_command("help")

@bot.command(name="reload")
@commands.has_permissions(administrator=True)
async def reload_cogs(ctx):
    reloaded = []
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.reload_extension(f"cogs.{filename[:-3]}")
                reloaded.append(filename)
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Neuladen von {filename}: {e}")
    await ctx.send(f"🔄 Cogs neu geladen: {', '.join(reloaded)}")

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="📘 LumiGuard Befehle",
        description="Hier sind einige nützliche Befehle:",
        color=discord.Color.green()
    )
    embed.add_field(name="!hilfe", value="Zeigt diese Hilfe an.", inline=False)
    embed.add_field(name="!live", value="Prüft ob LumiZAP gerade live ist.", inline=False)
    embed.add_field(name="!lumiliebe", value="Zeigt dir etwas Liebe von Lumi 💜", inline=False)
    embed.add_field(name="!status", value="Zeigt die Server-Statistiken an.", inline=False)
    embed.add_field(name="!kick / !ban / !warn", value="Moderationsbefehle für Admins.", inline=False)
    embed.set_footer(text="Mit ❤️ von LumiWächter")
    await ctx.send(embed=embed)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")
    await load_cogs()
    await bot.tree.sync()


bot.run(config.TOKEN)
