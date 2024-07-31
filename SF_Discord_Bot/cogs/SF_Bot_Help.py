# SF_Bot_Help.py

import discord
from discord.ext import commands

class SF_Bot_Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Help commands loaded for {self.bot.user.name}')

    @commands.command(name='Info', aliases=['commandslist', 'listcommands'], help="Sends a personal message with a list of all available commands and their descriptions.")
    async def botinfo(self, ctx):
        help_text = (
            "Here are the available commands:\n"
            "\n**!Info**: List of all available commands on the server, including those not available to you."
            "\n "
            "\n**!Core**: Description of what SoftField Core (Framework) is."
            "\n "
            "\n**!Join**: Creates a separate channel for recruitment purposes. Use this command if you want to apply to join the team."
            "\n "
            "\n**!Library**: Excel library with various useful links (available to Developers only)."
            "\n "
            "\n**!Addons**: Link to Blender addons (available to Developers only)."
            "\n "
            "\n**!GPMask**: Link to download the P and G masks archive, which includes Substance Smart Material and Exporter (available to Developers only)."
            "\n "
            "\n**!Report**: Creates a report of completed work. Just enter the command and then the text of what you did, and the system will automatically forward it to the appropriate place. You can write anywhere and in any chat (available to Developers only)."
            "\n "
            "\n**!Test_reminder**: Debugging command for administration only."
            "\n "
            "\n**!Task № Name**: Creates a task for convenience. Simply enter the command, followed by any number and, optionally, the task name, then press enter and write your message (available to Developers only)."
            "\n "
            "\n**!Tasklog №**: Allows you to find a message that was tagged in any chat by its number; just enter the command and the task number (available to Developers only)."
            "\n "
            "\n**!TaskLog_All**: Allows you to view the log of all tasks in memory (available to Developers only)."
            "\n "
            "\n**!Task_Remove № № №**: Allows you to delete a task from memory; you can delete each one individually or several at once by listing their numbers separated by spaces (available to Developers only)."
        )
        try:
            await ctx.author.send(help_text)
            await ctx.send("I have sent you a personal message with the list of available commands!")
        except discord.Forbidden:
            await ctx.send("I cannot send you a personal message. Please check your privacy settings.")

async def setup(bot):
    await bot.add_cog(SF_Bot_Help(bot))
