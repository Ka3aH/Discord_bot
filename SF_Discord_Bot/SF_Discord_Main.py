# SF_Discord_Main.py

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import openai

#временный код отладки
print("OpenAI version:", openai.__version__)
print("Discord.py version:", discord.__version__)
#временный код отладки

# Загрузка переменных окружения из файла .env
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Настройка OpenAI API ключа
openai.api_key = OPENAI_API_KEY

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

@bot.command()
async def tr(ctx, channel_name: str, *, text: str):
    """Команда для перевода текста с использованием GPT и подтверждения отправки."""
    if "Project Manager" not in [role.name for role in ctx.author.roles]:
        await ctx.send("У вас нет прав для использования этой команды.")
        return

    # Запрос перевода
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Используйте подходящую модель
            messages=[
                {"role": "user", "content": f"Translate the following text from Russian to English:\n{text}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        translated_text = response.choices[0].message['content'].strip()

        # Запрос подтверждения
        confirmation_message = await ctx.send(
            f"Вот перевод:\n\n{translated_text}\n\nОтправить этот вариант? (да/нет)"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['да', 'нет', 'yes', 'no']

        try:
            response_message = await bot.wait_for('message', timeout=60.0, check=check)
            if response_message.content.lower() in ['да', 'yes']:
                # Отправка перевода в указанный канал
                for channel in ctx.guild.channels:
                    if channel.name == channel_name:
                        await channel.send(f"Переведенный текст:\n\n{translated_text}")
                        await ctx.send(f"Переведенный текст отправлен в канал {channel_name}.")
                        return
                await ctx.send(f"Канал с именем {channel_name} не найден.")
            else:
                await ctx.send("Отправка перевода отменена.")
        except asyncio.TimeoutError:
            await ctx.send("Время на подтверждение истекло, отправка перевода отменена.")

    except Exception as e:
        await ctx.send(f"Произошла ошибка: {e}")

async def main():
    await load_extensions()
    await bot.start(DISCORD_TOKEN)

asyncio.run(main())
