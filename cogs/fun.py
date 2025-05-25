
from discord.ext import commands
import random
from twitch_api import is_stream_live
import time
import random 
import sys

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="GuteNacht", help="Stops the bot")
    @commands.is_owner()  # Only the bot owner can use this command
    async def GuteNacht(self, ctx):
        await ctx.send("Gute Nacht!")
        await self.bot.close()
        sys.exit(0)  # Optional: if running in a script

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="live")
    async def live(self, ctx):
        if is_stream_live():
            await ctx.send("🔴 LumiZAP ist **LIVE**! Schau vorbei: https://twitch.tv/lumizap")
        else:
            await ctx.send("📴 Lumi ist aktuell nicht live.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        target_user = message.guild.get_member(366204965363908610)
        target_user2 = message.guild.get_member(970379709596729446)
        content = message.content.lower()
        if "zap" in content:
            await message.add_reaction("⚡")
        if "lumi" in content:
            await message.add_reaction("💜")
        if "zauberwort" in content:
           await message.reply("**ZAPALICIOUS!** ⚡")
           await message.add_reaction("⚡")
        if "bester mod" in content:
            await message.add_reaction("💻")
            await message.reply("es ist natürlich **Oliver!** :computer:")
        if "beste mod" in content:
            await message.add_reaction("💻")
            await message.reply("es ist natürlich **Oliver!** :computer:")
        if "💀" in content:
            await message.add_reaction("💀")
        if "☠️" in content:
            await message.add_reaction("☠️")
        if self.bot.user in message.mentions and "bester bot" in message.content.lower():
            await message.reply(f"**Gut so!! {message.author.mention} ** <:angy:1376308675052044329>")
            await message.add_reaction("<:angy:1376308675052044329>")
        elif self.bot.user in message.mentions:
            await message.reply(f"**Ping mich nicht an! {message.author.mention} ** <:angy:1376308675052044329>")
            await message.add_reaction("<:angy:1376308675052044329>")
        if target_user2 and target_user2 in message.mentions:
            if random.randint(1, 50) == 1:
                await message.add_reaction("<:dev1:1376317790893641848>")
                time.sleep(0.1)
                await message.add_reaction("<:dev2:1376317982128734269>")
                time.sleep(0.1)
                await message.add_reaction("<:dev3:1376318021051613194>")
        if "🤙" in content:
            await message.reply(f"**I didnt know you where chill like that! {message.author.mention} ** 🤙")
            await message.add_reaction("🤙")
        if target_user in message.mentions:
            if message.author.id == target_user.id:
                # target user pinged themselves
                await message.reply("**Warum pingst du dich selber Oliver!?**")
                await message.add_reaction("<:angy:1376308675052044329>")
        else:
            if random.randint(1, 100) == 1:
                await message.reply(f"**Ping nicht meinen Lieblings-Mod an! {message.author.mention}** <:angy:1376308675052044329>")
                await message.add_reaction("<:angy:1376308675052044329>")

async def setup(bot):
    await bot.add_cog(Fun(bot))
    await bot.add_cog(AdminCommands(bot))