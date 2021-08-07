from keep_alive import keep_alive

import discord
import typing
from discord.ext import commands
import os
import random
from replit import db
from PIL import Image, ImageDraw, ImageFont

myfont = ImageFont.truetype('./Myfont.htm', size = 280)

# перенос строки
enter = '''
'''

im = Image.new('RGB', (200,200), color=('#FAACAC'))
draw_text = ImageDraw.Draw(im)
draw_text.text(
    (100,100),
    'Test Text',
    fill=('#1C0606')
    )
im.save('./pict.jpg')

# Панели
def FastEmbed(titl, desc):
  embed = discord.Embed(
    title = titl,
    description = desc,
    colour = 0xffe24f
  )
  return embed

# Класс персонажа
class Pers():
  def __init__(self, name, stats, member):
    self.name = name
    self.stats = stats
    self.statsDict = {
      'hp' : stats[1],
      'ar' : stats[2],
      'an' : stats[3],
      'pw' : stats[4],
      'dx' : stats[5],
      'ac' : stats[6]
    }
    self.member = member

  def edit_stat(self, stat, value):
    self.statsDict[stat] = value

  def get_stat(self, stat):
    return self.statsDict.get(stat)

# Инициализация персонажей
def getPers():
  persons = {}
  PersonsFile = open('persons.txt')
  for line in PersonsFile:
    P1 = line.split(',')
    P2 = P1[2].split('-')
    P3 = P2[2].split('/')
    P4 = Pers(int(P2[1]), P3, P1[1])
    persons[int(P1[1])] = P4
  PersonsFile.close
  return persons

def savePers(persons):
  PersonsFile = open('persons.txt', 'w')
  for key, value in persons:
    P3 = "/".join(value.stats)
    P2 = value.name + '-' + P3
    P1 = str(value.member) + ',' + P2
    write(P1 + '/n')
  PersonsFile.close

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
    await ctx.send('{0.name} joined in {0.joined_at}, <:emoji_10:870700594027966464>'.format(member))

# dice
@bot.command()
async def dice(ctx, modif: typing.Optional[int] = 0):
  dice = random.randint(1, 12)
  if (modif >= -11) and (modif <= 11):
    result = dice + modif
    if result < 1:
        result = 1
    if result > 12:
        result = 12
    await ctx.send(embed = FastEmbed('Dice', '<:dice:871337451627638814> ' + str(result) + str(enter) + '||(' + str(dice) + ' + ' + str(modif) + ')||'))
  else:
    await ctx.send(embed = FastEmbed('Error', 'Модификатор не может быть меньше -11 и больше 11'))

@bot.command()
async def image(ctx):
    await ctx.send(file = discord.File('./pict.jpg'))
    
# RP
@bot.command()
async def stats(ctx):
  persons = getPers()
  member = ctx.author.id
  Person = persons.get(member)
  await ctx.send(Peson.name + Person.stats)
  
@bot.command()
async def newpers(ctx, name):
  member = ctx.author.id
  P4 = Pers(name, ('30', '20', '60', '50', '50', '30'), member)
  persons = {
    member : P4
  }
  savePers(persons)
  

# keep_alive()

# run
bot.run(os.environ['TOKEN'])