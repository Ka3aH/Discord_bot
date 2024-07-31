# SF_Bot_Report.py

import discord
from discord.ext import commands, tasks
import datetime

REMINDER_CHANNEL_ID = 1267187290015535104
REPORT_CHANNEL_ID = 1267187290015535104

reports = {}

class SF_Bot_Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_day_for_reminder.start()

    @tasks.loop(minutes=1)
    async def check_day_for_reminder(self):
        now = datetime.datetime.now()
        if now.weekday() == 4 and now.hour == 10 and now.minute == 0:
            await self.send_reminder()

    async def send_reminder(self):
        channel = self.bot.get_channel(REMINDER_CHANNEL_ID)
        if channel:
            role = discord.utils.get(channel.guild.roles, name='Developer')
            if role:
                await channel.send(f"**Reminder for role {role.mention}: Please submit your weekly report!**\n\n"
                                   "Enter the command `!report` and write what you have done over the week.\n\n"
                                   "Your reports will be stored with the time and date of submission for record-keeping purposes.")

    @commands.command(help="Submit your weekly report. This command is available only for Developers.")
    @commands.has_role('Developer')
    async def report(self, ctx, *, report_text: str):
        report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reports[ctx.author.id] = {
            'time': report_time,
            'username': ctx.author.name,
            'report': report_text
        }

        report_channel = self.bot.get_channel(REPORT_CHANNEL_ID)
        
        if report_channel:
            await report_channel.send(f"**New report submitted:**\n\n"
                                      f"**Date and Time:** {report_time}\n"
                                      f"**Username:** {ctx.author.name}\n"
                                      f"**Report:**\n{report_text}")
            await ctx.send(f"**Thank you, {ctx.author.name}! Your report has been recorded and sent to the report channel.**")
        else:
            await ctx.send("Error: The report channel could not be found.")

    @commands.command(help="Get the list of all reports.")
    @commands.has_role('Developer')
    async def reportlist(self, ctx):
        if reports:
            response = "\n".join([f"**Date and Time:** {report['time']}\n"
                                  f"**Username:** {report['username']}\n"
                                  f"**Report:**\n{report['report']}\n" for report in reports.values()])
            await ctx.send(f"**All reports:**\n{response}")
        else:
            await ctx.send("No reports available.")

    @commands.command(help="Manually trigger the reminder and show the next scheduled reminder time. This command is available only for Administration and Project Manager roles.")
    @commands.has_any_role('Administration', 'Project Manager')
    async def test_reminder(self, ctx):
        await self.send_reminder()
        
        now = datetime.datetime.now()
        next_friday = now + datetime.timedelta((4 - now.weekday()) % 7)
        next_reminder_time = next_friday.replace(hour=10, minute=0, second=0, microsecond=0)
        
        await ctx.send(f"**Manual reminder sent.**\n\n"
                       f"The next scheduled reminder will be on {next_reminder_time.strftime('%A, %B %d, %Y at %H:%M')}.")

    @report.error
    @reportlist.error
    @test_reminder.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the required role to use this command.")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have any of the required roles to use this command.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

async def setup(bot):
    await bot.add_cog(SF_Bot_Report(bot))
