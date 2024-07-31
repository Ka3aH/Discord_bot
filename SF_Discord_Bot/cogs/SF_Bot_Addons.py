# SF_Bot_Addons.py

import discord
from discord.ext import commands

class SF_Bot_Addons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command(name='Addons', aliases=['extra_info', 'plugin_info'], help="Sends a personal message with specific text.")
    @commands.has_any_role('Developer', 'Junior')
    async def addons(self, ctx):
        try:
            await ctx.author.send("НАПИШИ СЮДА ТЕКСТ ЧТО НАДО ОТПРАВЛЯТЬ")
            await ctx.send("I have sent you a personal message!")
        except discord.Forbidden:
            await ctx.send("I cannot send you a personal message. Please check your privacy settings.")

async def setup(bot):
    await bot.add_cog(SF_Bot_Addons(bot))
