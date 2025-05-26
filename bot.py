import os
import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.remove_command("help") # type: ignore

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
                await ctx.send(f"❌ {filename}: {e}")
    await ctx.send(f"🔄 Cogs neu geladen: {', '.join(reloaded)}")

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")
    await load_cogs()
    await bot.tree.sync()


bot.run(config.TOKEN)# type: ignore
