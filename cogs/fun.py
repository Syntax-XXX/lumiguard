
from discord.ext import commands
import discord
import random
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

    @commands.command(name="hilfe", aliases=["help"])
    async def help(self, message):
        embed = discord.Embed(
        title="📘 LumiGuard Befehle",
        description="Hier sind einige nützliche Befehle für dich:",
        color=discord.Color.green()
         )
        embed.add_field(name="!hilfe", value="Zeigt diese Hilfe an.", inline=False)
        embed.add_field(name="!live", value="Prüft, ob LumiZAP gerade live ist.", inline=False)
        embed.add_field(name="!status", value="Zeigt die Server-Statistiken an.", inline=False)
        embed.add_field(name="!watchtime [TwitchName]", value="Zeigt deine oder eine andere Watchtime an.", inline=False)
        embed.add_field(name="!verknüpfe <TwitchName>", value="Verknüpft deinen Discord mit einem Twitch-Konto.", inline=False)
        embed.add_field(name="!topwatchtime", value="Zeigt das Watchtime-Leaderboard (Top 5) an.", inline=False)
        embed.add_field(name="!kick / !ban / !warn", value="Moderationsbefehle für Admins.", inline=False)
        embed.set_footer(text="Mit ❤️ von LumiGuard")
        await message.reply(embed=embed)

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