import json
import openai
import discord
from discord.ext import commands
import os
import faiss
import numpy as np

# Загрузите ваш API ключ OpenAI из переменных окружения
openai.api_key = os.getenv('OPENAI_API_KEY')

# Определите максимальную длину ответа для Discord
MAX_RESPONSE_LENGTH = 2000

class SF_GPT_Main(commands.Cog):
    """Cog для обработки команды !sf и использования GPT-4o-mini для ответов на запросы."""

    def __init__(self, bot):
        self.bot = bot
        self.knowledge_base = self.load_knowledge_base()
        self.index, self.embeddings = self.create_index()

    def load_knowledge_base(self):
        """Загрузка базы знаний из файла JSON."""
        knowledge_base_file = 'SF_GPT_Library.json'
        if not os.path.exists(knowledge_base_file):
            raise FileNotFoundError(f"Knowledge base file {knowledge_base_file} does not exist.")
        with open(knowledge_base_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def create_index(self):
        """Создание индекса FAISS для быстрого поиска по базе знаний."""
        embeddings = []
        for item in self.knowledge_base:
            embeddings.append(self.get_embedding(item['content']))
        embeddings = np.array(embeddings).astype('float32')
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, embeddings

    def get_embedding(self, text):
        """Получение эмбеддинга текста с использованием GPT-4o-mini."""
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response['data'][0]['embedding']

    def find_relevant_content(self, query, top_k=5):
        """Ищет наиболее релевантное содержание в базе знаний по запросу."""
        query_embedding = np.array(self.get_embedding(query)).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.knowledge_base[idx] for idx in indices[0]]

    async def get_gpt_response(self, query, relevant_content):
        """Получение ответа от GPT-4o-mini на основе запроса и релевантного контента."""
        context = "Используйте только информацию из базы знаний SoftField для ответов.\n\n"
        for item in relevant_content:
            context += f"Заголовок: {item.get('title', '')}\nСодержание: {item.get('content', '')}\n\n"

        prompt = f"{context}\nЗапрос: {query}"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": query}
                ],
                max_tokens=150,
                temperature=0.7
            )
            gpt_response = response.choices[0].message['content'].strip()
            return gpt_response
        except Exception as e:
            print(f"Ошибка при вызове GPT-4 API: {e}")
            return "Произошла ошибка при получении ответа. Попробуйте позже."

    def split_response(self, response, max_length):
        """Разбивает ответ на части, чтобы каждая часть не превышала максимальную длину."""
        parts = []
        while len(response) > max_length:
            split_index = response.rfind(' ', 0, max_length)
            if split_index == -1:
                split_index = max_length
            parts.append(response[:split_index])
            response = response[split_index:].strip()
        if response:
            parts.append(response)
        return parts

    @commands.command(name='sf', aliases=['SF'])
    async def sf(self, ctx, *, query: str = None):
        """Команда для получения ответа от GPT-4 или из базы знаний."""
        if query is None:
            await ctx.send("Пожалуйста, введите вопрос или запрос.")
            return

        # Поиск релевантного контента в базе знаний
        relevant_content = self.find_relevant_content(query)

        # Использование GPT для обработки запроса с учетом релевантного контента
        response = await self.get_gpt_response(query, relevant_content)
        
        # Разбиваем ответ на части, если он превышает максимальную длину
        response_parts = self.split_response(response, MAX_RESPONSE_LENGTH)
        
        # Отправка ответа пользователю
        for part in response_parts:
            await ctx.send(part)

async def setup(bot):
    await bot.add_cog(SF_GPT_Main(bot))
