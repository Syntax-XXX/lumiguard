
import discord
from discord.ext import commands, tasks
import itertools

class StatusChanger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = itertools.cycle([
            discord.Game(name="mit Lumi"),
            discord.Game(name="mit Olivers Zeugnis"),
            discord.Game(name="mit SyntaxXXX"),
            discord.Activity(type=discord.ActivityType.watching, name="über Lumi's Server")
        ])
        self.change_status.start()

    @tasks.loop(seconds=30)
    async def change_status(self):
        await self.bot.change_presence(activity=next(self.statuses))

    def cog_unload(self):
        self.change_status.cancel()

async def setup(bot):
    await bot.add_cog(StatusChanger(bot))
