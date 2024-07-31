# SF_Bot_Core.py

import discord
from discord.ext import commands

class SF_Bot_Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command(name='Core', aliases=['core_info', 'core_details'], help="Sends a personal message with specific text.")
    async def core(self, ctx):
        try:
            await ctx.author.send("НАПИШИ СЮДА ТЕКСТ ЧТО НАДО ОТПРАВЛЯТЬ")
            await ctx.send("I have sent you a personal message!")
        except discord.Forbidden:
            await ctx.send("I cannot send you a personal message. Please check your privacy settings.")

async def setup(bot):
    await bot.add_cog(SF_Bot_Core(bot))
