import discord
from discord.ext import commands

class StatusComm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status")
    async def status(self, ctx):
        guild = ctx.guild
        status_data["members"] = guild.member_count # type: ignore
        status_data["roles"] = len(guild.roles) # type: ignore
        status_data["channels"] = len(guild.channels) # type: ignore

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
    await bot.add_cog(StatusComm(bot))
