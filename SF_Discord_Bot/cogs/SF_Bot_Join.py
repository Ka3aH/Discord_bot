# SF_Bot_Join.py

import discord
from discord.ext import commands
import asyncio

# Словарь для хранения времени последнего запроса пользователя
request_timestamps = {}

# Время между запросами (в секундах)
REQUEST_COOLDOWN = 3600

# Блокировка для предотвращения одновременного создания дубликатов
lock = asyncio.Lock()

class SF_Bot_Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command(help="Allows you to create a private channel for joining the team.")
    async def join(self, ctx):
        # Проверка антиспама
        now = int(ctx.message.created_at.timestamp())
        user_id = ctx.author.id
        last_request_time = request_timestamps.get(user_id, 0)
        
        if now - last_request_time < REQUEST_COOLDOWN:
            await ctx.author.send(f'Please wait {REQUEST_COOLDOWN - (now - last_request_time)} seconds before making another request.')
            return
        
        request_timestamps[user_id] = now

        async with lock:
            guild = ctx.guild
            category = discord.utils.get(guild.categories, name='Join Requests')

            if not category:
                try:
                    category = await guild.create_category('Join Requests')
                    print('Created category: Join Requests')
                except Exception as e:
                    print(f'Error creating category: {e}')
                    await ctx.author.send('Cannot create category.')
                    return

            # Формируем уникальное имя канала
            channel_name = f'join-{ctx.author.name.lower().replace(" ", "-").replace("_", "-")}-{int(ctx.message.created_at.timestamp())}'
            print(f'Channel name to check: {channel_name}')  # Отладочное сообщение

            # Обновляем список каналов
            await guild.fetch_channels()  # Обновляем кэш каналов

            # Проверка наличия канала для данного пользователя
            existing_channel = discord.utils.get(category.channels, name=channel_name.lower())
            if existing_channel:
                print(f'Found existing channel: {existing_channel.name}')  # Отладочное сообщение
                await ctx.author.send('You already have an open channel.')
                return

            # Создание нового текстового канала в категории "Join Requests"
            try:
                channel = await category.create_text_channel(channel_name)
                print(f'Created channel: {channel.name}')
            except Exception as e:
                print(f'Error creating channel: {e}')
                await ctx.author.send('Cannot create channel.')
                return

            # Назначение прав доступа для роли @everyone и роли @Junior
            try:
                # Установите права для @everyone
                await channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)
                
                # Установите права для роли @Junior и @Developer
                junior_role = discord.utils.get(guild.roles, name='Junior')
                developer_role = discord.utils.get(guild.roles, name='Developer')
                if junior_role:
                    await channel.set_permissions(junior_role, read_messages=True, send_messages=True)
                if developer_role:
                    await channel.set_permissions(developer_role, read_messages=True, send_messages=True)
                
                # Установите права для пользователя
                await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

                print(f'Set permissions for channel: {channel.name}')
            except Exception as e:
                print(f'Error setting permissions: {e}')
                await ctx.author.send('Error setting permissions.')

            # Отправка сообщения в новый канал
            try:
                await channel.send("""This channel is exclusively for you and users with the Developer role. Only you and these users can view it.

This channel and the command as a whole are created for those who want to join the SoftField team.

Terms of Cooperation:
1. You will be hired as a Junior. Basic modeling skills are required; you will receive training for the rest.
2. As a Junior, you will need to complete one asset assigned by your lead.
3. After completing the task, you will either connect to the server to set up your model in Unreal Engine 5 according to the instructions provided, or everything will be set up for you. There is also an option to receive an isolated Framework for setting up the model.
4. Once the asset passes all revisions and checks, it will be prepared for sale.
5. You will create screenshots of your asset as you see it. These screenshots may be adjusted or added to by your lead at the final stage.
6. You will prepare a document for the transfer of rights to the model and a list of what you are relinquishing, transferring all ownership rights to SoftField.
7. The agreement will specify the terms of cooperation, where you will receive 50% of the sales from the asset if created independently, and 47.5% if a lead was involved. Team members' general assistance and answers to minor questions do not count as participation in the asset.
8. If multiple people worked on an asset, such as a modeler and an animator/rigor, you will receive a smaller share. The principle is: each asset involves SoftField and other contributors. If three people worked on the asset, you will receive 33.3% of the sales, or 31.6% if a lead was involved.
9. Payment can be made by any convenient method, preferably via PayPal. Currency for payment is Euros.
10. All necessary instructions, document templates, and other materials will be provided.

- The principles are similar, but there are differences in details and payment methods. Payment is performance-based.""")

                print('Sent test message to channel.')
            except Exception as e:
                print(f'Error sending message: {e}')
                await ctx.author.send('Error sending message.')

            await ctx.author.send(f'New channel created: {channel.mention}')

async def setup(bot):
    await bot.add_cog(SF_Bot_Join(bot))
