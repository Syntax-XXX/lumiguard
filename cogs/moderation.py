
import discord
from discord.ext import commands
import json
import os

WARN_FILE = "warns.json"

def load_warns():
    if not os.path.exists(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warns(warns):
    with open(WARN_FILE, "w") as f:
        json.dump(warns, f, indent=4)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, grund="Kein Grund angegeben"):
        await member.kick(reason=grund)
        await ctx.send(f"⚠️ {member.mention} wurde rausgeworfen. Grund: {grund}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, grund="Kein Grund angegeben"):
        await member.ban(reason=grund)
        await ctx.send(f"🔨 {member.mention} wurde gebannt! Grund: {grund}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, anzahl: int):
        await ctx.channel.purge(limit=anzahl)
        msg = await ctx.send(f"🧹 {anzahl} Nachrichten gelöscht.")
        await msg.delete(delay=3)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, grund="Kein Grund angegeben"):
        warns = load_warns()
        uid = str(member.id)
        warns[uid] = warns.get(uid, []) + [grund]
        save_warns(warns)
        await ctx.send(f"⚠️ {member.mention} wurde verwarnt. Grund: {grund} (Anzahl: {len(warns[uid])})")

    @commands.command()
    async def warns(self, ctx, member: discord.Member):
        warns = load_warns()
        uid = str(member.id)
        user_warns = warns.get(uid, [])
        if not user_warns:
            await ctx.send(f"✅ {member.display_name} hat keine Verwarnungen.")
        else:
            msg = "\n".join(f"{i+1}. {w}" for i, w in enumerate(user_warns))
            await ctx.send(f"📄 Verwarnungen für {member.display_name}:\n{msg}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
