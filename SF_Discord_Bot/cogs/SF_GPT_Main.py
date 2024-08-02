import json
import openai
import discord
from discord.ext import commands
import os

# Загрузите ваш API ключ OpenAI из переменных окружения
openai.api_key = os.getenv('OPENAI_API_KEY')

# Определите максимальную длину ответа
MAX_RESPONSE_LENGTH = 2000

class SF_GPT_Main(commands.Cog):
    """Cog для обработки команды !sf и использования GPT-4o-mini для ответов на запросы."""

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

    def find_relevant_content(self, query):
        """Ищет наиболее релевантное содержание в базе знаний по запросу и возвращает выжимку."""
        query_lower = query.lower()
        for item in self.knowledge_base:
            title_lower = item.get('title', '').lower()
            content_lower = item.get('content', '').lower()
            if query_lower in title_lower or query_lower in content_lower:
                return self.extract_summary(item['content'])
        return None

    def extract_summary(self, content):
        """Извлечение выжимки из контента для краткого ответа."""
        return content[:500]

    async def get_gpt_response(self, query):
        """Получение ответа от GPT-4o-mini на основе запроса."""
        context = ("Используй только информацию из базы знаний SoftField для ответов. "
                   "Если запрос касается темы, которая упоминается в базе знаний, используй соответствующую информацию. "
                   "Если данных недостаточно, укажи, что информации нет.")
        prompt = f"{context}\n\nЗапрос: {query}"
        
        try:
            response = openai.Completion.create(
                model="gpt-4o-mini",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7
            )
            gpt_response = response.choices[0].text.strip()
            return gpt_response[:MAX_RESPONSE_LENGTH]
        except Exception as e:
            print(f"Ошибка при вызове GPT-4o-mini API: {e}")
            return "Произошла ошибка при получении ответа. Попробуйте позже."

    @commands.command(name='sf', aliases=['SF'])
    async def sf(self, ctx, *, query: str = None):
        """Команда для получения ответа от GPT-4o-mini или из базы знаний."""
        if query is None:
            await ctx.send("Пожалуйста, введите вопрос или запрос.")
            return

        # Поиск релевантного контента в базе знаний
        relevant_content = self.find_relevant_content(query)

        if relevant_content:
            response = relevant_content
        else:
            # Если в базе знаний нет точного совпадения, используем GPT для обработки запроса
            response = await self.get_gpt_response(query)
        
        # Отправка ответа пользователю
        if len(response) > MAX_RESPONSE_LENGTH:
            response = response[:MAX_RESPONSE_LENGTH]
        await ctx.send(response)

async def setup(bot):
    print("Setting up SF_GPT_Main...")
    await bot.add_cog(SF_GPT_Main(bot))
