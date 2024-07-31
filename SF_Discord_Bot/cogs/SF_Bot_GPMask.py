# SF_Bot_GPMask.py

import discord
from discord.ext import commands

class SF_Bot_GPMask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command(name='GPMask', aliases=['gp_mask', 'mask_info'], help="Sends a personal message with specific text.")
    @commands.has_any_role('Developer', 'Junior')
    async def gp_mask(self, ctx):
        try:
            await ctx.author.send("НАПИШИ СЮДА ТЕКСТ ЧТО НАДО ОТПРАВЛЯТЬ")
            await ctx.send("I have sent you a personal message!")
        except discord.Forbidden:
            await ctx.send("I cannot send you a personal message. Please check your privacy settings.")

    @gp_mask.error
    async def gp_mask_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have the required role to use this command.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(SF_Bot_GPMask(bot))
