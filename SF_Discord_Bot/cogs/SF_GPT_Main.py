import discord
from discord.ext import commands
from .sf_gpt_library import get_knowledge_response  # Используйте относительный импорт

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
