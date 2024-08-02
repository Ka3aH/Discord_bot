import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename[:-3]}. {e}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

async def main():
    await load_extensions()
    await bot.start(DISCORD_TOKEN)

asyncio.run(main())
