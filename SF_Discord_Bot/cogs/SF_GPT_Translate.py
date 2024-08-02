import discord
from discord.ext import commands
import openai
import asyncio
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Файл для хранения общего количества токенов
TOKEN_USAGE_FILE = 'token_usage.txt'

def read_total_tokens():
    """Чтение общего количества токенов из файла."""
    if os.path.exists(TOKEN_USAGE_FILE):
        with open(TOKEN_USAGE_FILE, 'r') as file:
            return int(file.read().strip())
    return 0

def write_total_tokens(total_tokens):
    """Запись общего количества токенов в файл."""
    with open(TOKEN_USAGE_FILE, 'w') as file:
        file.write(str(total_tokens))

def log_usage(response):
    """Логирование использования токенов и обновление общего количества токенов."""
    tokens_used = response['usage']['total_tokens']
    logging.info(f"Tokens used: {tokens_used}")

    # Обновление общего количества токенов
    total_tokens = read_total_tokens() + tokens_used
    write_total_tokens(total_tokens)

class GPTCommands(commands.Cog):
    """Cog для команд, связанных с GPT"""

    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv('OPENAI_API_KEY')

    @commands.command()
    async def tr(self, ctx, channel_name: str, *, text: str):
        """Команда для перевода текста с использованием GPT и подтверждения отправки."""
        if "Project Manager" not in [role.name for role in ctx.author.roles]:
            await ctx.send("У вас нет прав для использования этой команды.")
            return

        # Запрос перевода
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Используйте новую модель
                messages=[
                    {"role": "user", "content": f"Translate the following text from Russian to English:\n{text}"}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            log_usage(response)  # Логирование использования токенов
            translated_text = response.choices[0].message['content'].strip()

            # Запрос подтверждения
            confirmation_message = await ctx.send(
                f"Вот перевод:\n\n{translated_text}\n\nОтправить этот вариант? (да/нет)"
            )

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['да', 'нет', 'yes', 'no']

            try:
                response_message = await self.bot.wait_for('message', timeout=60.0, check=check)
                if response_message.content.lower() in ['да', 'yes']:
                    # Отправка перевода в указанный канал
                    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
                    if channel:
                        await channel.send(f"Переведенный текст:\n\n{translated_text}")
                        await ctx.send(f"Переведенный текст отправлен в канал {channel_name}.")
                    else:
                        await ctx.send(f"Канал с именем {channel_name} не найден.")
                else:
                    await ctx.send("Отправка перевода отменена.")
            except asyncio.TimeoutError:
                await ctx.send("Время на подтверждение истекло, отправка перевода отменена.")

        except Exception as e:
            await ctx.send(f"Произошла ошибка: {e}")

    @commands.command()
    async def token(self, ctx):
        """Команда для отображения общего количества использованных токенов."""
        if "Project Manager" not in [role.name for role in ctx.author.roles]:
            await ctx.send("У вас нет прав для использования этой команды.")
            return

        total_tokens = read_total_tokens()
        await ctx.send(f"Общее количество использованных токенов: {total_tokens}")

async def setup(bot):
    await bot.add_cog(GPTCommands(bot))
