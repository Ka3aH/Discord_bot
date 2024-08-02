import json
import os
import discord
from discord.ext import commands

# Путь к файлу JSON с библиотекой знаний
KNOWLEDGE_BASE_FILE = 'SF_GPT_Library.json'

def load_knowledge_base():
    """Загрузка базы знаний из файла JSON."""
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        raise FileNotFoundError(f"Knowledge base file {KNOWLEDGE_BASE_FILE} does not exist.")
    with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as file:
        print("Loading knowledge base...")
        return json.load(file)

def get_knowledge_response(query):
    """Получение ответа из базы знаний на основе запроса."""
    knowledge_base = load_knowledge_base()
    for item in knowledge_base:
        if query.lower() in item['title'].lower() or query.lower() in item['content'].lower():
            return item['content']
    return "Извините, я не могу ответить на этот вопрос, так как я создан для помощи по SoftField."

class SF_GPT_Main(commands.Cog):
    """Cog для обработки команды !SF и использования базы знаний из JSON файла."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sf(self, ctx, *, query: str = None):
        """Команда для получения ответа на основе базы знаний из JSON файла."""
        if query is None:
            await ctx.send("Пожалуйста, введите вопрос или запрос.")
            return

        # Получение ответа из базы знаний
        response = get_knowledge_response(query)
        await ctx.send(response)

async def setup(bot):
    print("Setting up SF_GPT_Main...")
    await bot.add_cog(SF_GPT_Main(bot))
