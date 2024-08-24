import discord
from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_levels = {}

    def get_level(self, user_id):
        return self.user_levels.get(user_id, 1)

    def increment_level(self, user_id):
        self.user_levels[user_id] = self.user_levels.get(user_id, 1) + 1

    @commands.command(name='level')
    async def check_level(self, ctx):
        level = self.get_level(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, ваш текущий уровень: {level}.")

    @commands.command(name='updatelvl')
    @commands.has_permissions(administrator=True)
    async def update_level(self, ctx, member: discord.Member):
        self.increment_level(member.id)
        level = self.get_level(member.id)
        await ctx.send(f"{member.mention} теперь на уровне {level}.")

