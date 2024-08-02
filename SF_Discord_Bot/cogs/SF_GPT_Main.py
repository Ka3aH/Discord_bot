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

    async def get_gpt_response(self, query):
        """Получение ответа от GPT-4o-mini на основе запроса."""
        try:
            response = openai.Completion.create(
                engine="gpt-4o-mini",  # Убедитесь, что имя модели правильное
                prompt=query,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Ошибка при вызове GPT-4o-mini API: {e}")
            return "Произошла ошибка при получении ответа. Попробуйте позже."

    @commands.command()
    async def sf(self, ctx, *, query: str = None):
        """Команда для получения ответа от GPT-4o-mini."""
        if query is None:
            await ctx.send("Пожалуйста, введите вопрос или запрос.")
            return

        # Получение ответа от GPT-4o-mini
        response = await self.get_gpt_response(query)
        await ctx.send(response)

async def setup(bot):
    print("Setting up SF_GPT_Main...")
    await bot.add_cog(SF_GPT_Main(bot))
