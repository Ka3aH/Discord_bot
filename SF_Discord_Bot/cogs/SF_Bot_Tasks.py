# SF_Bot_Tasks.py

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Словарь для хранения задач
tasks = {}

class SF_Bot_Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command(help="Create a new task with a unique ID and optional name. After executing this command, provide the task description.")
    @commands.has_role('Lead')
    async def task(self, ctx, task_id: str, *, task_name: str = None):
        # Проверка, что задача с таким ID уже существует
        if task_id in tasks:
            await ctx.send(f"Task {task_id} already exists. Please choose a different ID.")
            return
        
        # Уведомление о необходимости предоставить описание
        await ctx.send("Please provide the task description.")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        # Ждем описание задачи
        description_message = await self.bot.wait_for('message', check=check)
        
        # Сохраняем задачу
        tasks[task_id] = {
            'name': task_name if task_name else "No name provided",
            'description': description_message.content,
            'message_link': description_message.jump_url
        }
        
        await ctx.send(f"Task {task_id} created successfully!")

    @commands.command(help="Get the description of a task by its ID.")
    @commands.has_any_role('Developer', 'Junior')
    async def tasklog(self, ctx, task_id: str):
        task = tasks.get(task_id)
        
        if task:
            await ctx.send(f"Task {task_id} ({task['name']}):\nLink: {task['message_link']}")
        else:
            await ctx.send(f"Task {task_id} not found.")

    @commands.command(help="Get the list of all tasks with their names and links.")
    @commands.has_any_role('Developer', 'Junior')
    async def tasklog_all(self, ctx):
        if tasks:
            # Сортировка задач по ключу, поддерживающая дробные номера
            sorted_tasks = sorted(tasks.items(), key=lambda item: [int(i) if i.isdigit() else i for i in item[0].split('.')])
            response = "\n".join([f"Task {task_id} ({task_data['name']}): {task_data['message_link']}" for task_id, task_data in sorted_tasks])
            await ctx.send(f"All tasks:\n{response}")
        else:
            await ctx.send("No tasks available.")

    @commands.command(help="Remove a task by its ID.")
    @commands.has_role('Lead')
    async def task_remove(self, ctx, *task_ids: str):
        removed_tasks = []
        for task_id in task_ids:
            if task_id in tasks:
                del tasks[task_id]
                removed_tasks.append(task_id)
        
        if removed_tasks:
            await ctx.send(f"Removed tasks: {', '.join(removed_tasks)}")
        else:
            await ctx.send("No tasks were removed. Make sure the IDs are correct.")

    # Обработчик ошибок для команд с правами доступа
    @task.error
    @task_remove.error
    @tasklog.error
    @tasklog_all.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the required role to use this command.")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have any of the required roles to use this command.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(SF_Bot_Tasks(bot))
