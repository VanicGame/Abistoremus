from keep_alive import keep_alive

import discord
from discord.ext import commands
import os
import random

# Привилегированные намерения.
intents = discord.Intents.default()
intents.members = True

print('---------------------')
print('[[Запуск]]')

# Класс бота (ссылка на класс)
bot = commands.Bot(command_prefix = "!", intents=intents)

# Сообщение о готовности
@bot.event 
async def on_ready():
    print('[[Готов к работе]]')
    print('---------------------')

# Приветсвенное сообщение
@bot.event
async def on_member_join(member):
      guild = member.guild
      role = guild.get_role(869994658430844949)
      await member.add_roles(role, reason=None, atomic=True)
      if guild.system_channel  is not None:
          to_send = 'Приветствуем {0.mention} на {1.name}!'.format(member, guild)
          await guild.system_channel.send(to_send)
'''
@bot.event
async def on_member_join(member):
      guild = member.guild
      if guild.system_channel  is not None:
            to_send = 'Приветствуем {0.mention} на {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)
        
'''
# Команда - когда пользователь присоединился к серву
@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

# dice
@bot.command()
async def dice(ctx):
    await ctx.send(random.randint(1, 12))
# keep_alive()

# run
bot.run(os.environ['TOKEN'])