import discord
from discord.ext import commands

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_warnings = {}

    def add_warning(self, user_id):
        self.user_warnings[user_id] = self.user_warnings.get(user_id, 0) + 1
        return self.user_warnings[user_id]

    def reset_warnings(self, user_id):
        if user_id in self.user_warnings:
            del self.user_warnings[user_id]

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn_user(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        warnings = self.add_warning(member.id)
        await ctx.send(f"{member.mention} был предупрежден. Всего предупреждений: {warnings}")

        if warnings >= 3:
            await member.kick(reason=f"Тройное предупреждение: {reason}")
            self.reset_warnings(member.id)
            await ctx.send(f"{member.mention} был кикнут за три предупреждения.")

    @commands.command(name='clearwarns')
    @commands.has_permissions(manage_messages=True)
    async def clear_warnings(self, ctx, member: discord.Member):
        self.reset_warnings(member.id)
        await ctx.send(f"Предупреждения для {member.mention} очищены.")

