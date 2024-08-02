import json  # Добавьте этот импорт
import openai
import discord
from discord.ext import commands
import os

# Загрузите ваш API ключ OpenAI из переменных окружения
openai.api_key = os.getenv('OPENAI_API_KEY')

class SF_GPT_Main(commands.Cog):
    """Cog для обработки команды !SF и использования GPT-4o-mini для ответов на запросы."""

    def __init__(self, bot):
        self.bot = bot
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):
        """Загрузка базы знаний из файла JSON."""
        knowledge_base_file = 'SF_GPT_Library.json'
        if not os.path.exists(knowledge_base_file):
            raise FileNotFoundError(f"Knowledge base file {knowledge_base_file} does not exist.")
        with open(knowledge_base_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def is_query_in_knowledge_base(self, query):
        """Проверяет, есть ли запрос в базе знаний."""
        for item in self.knowledge_base:
            if query.lower() in item['title'].lower() or query.lower() in item['content'].lower():
                return True
        return False

    async def get_gpt_response(self, query):
        """Получение ответа от GPT-4o-mini на основе запроса."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Убедитесь, что имя модели правильное
                messages=[
                    {"role": "user", "content": query}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Ошибка при вызове GPT-4o-mini API: {e}")
            return "Произошла ошибка при получении ответа. Попробуйте позже."

    @commands.command()
    async def sf(self, ctx, *, query: str = None):
        """Команда для получения ответа от GPT-4o-mini."""
        if query is None:
            await ctx.send("Пожалуйста, введите вопрос или запрос.")
            return

        if not self.is_query_in_knowledge_base(query):
            # Если запрос не найден в базе знаний
            response = "Я тут, чтобы помогать вам с SoftField, а не для других тем. Для обсуждения других вопросов, пожалуйста, посетите сайт ChatGPT."
        else:
            # Получение ответа от GPT-4o-mini, если запрос найден в базе знаний
            response = await self.get_gpt_response(query)
        
        await ctx.send(response)

async def setup(bot):
    print("Setting up SF_GPT_Main...")
    await bot.add_cog(SF_GPT_Main(bot))
