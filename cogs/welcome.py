
import discord
from discord.ext import commands
from config import WILLKOMMEN_CHANNEL_ID
import os

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(WILLKOMMEN_CHANNEL_ID)
        rolle = discord.utils.get(member.guild.roles, name=os.getenv("AUTOROLLEN_NAME"))
        if rolle:
            await member.add_roles(rolle, reason="Auto-Rolle beim Beitritt")
        if channel:
            embed = discord.Embed(
                title="⚡ Willkommen bei der Lumination!",
                description=f"Hey {member.mention}, mach's dir gemütlich und fühl dich wie zu Hause! 💜",
                color=discord.Color.purple()
            )
            embed.set_footer(text="LumiGuard: Sei lieb, oder ich zappe!")
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
