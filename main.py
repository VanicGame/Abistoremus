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
    self.statsDict = {}
    self.stats = stats # Список хар-к
    self.hp = int(stats[0]) # Здоровье
    self.ar = int(stats[1]) # Защита
    self.it = int(stats[2]) # Интеллект
    self.pw = int(stats[3]) # Сила
    self.dx = int(stats[4]) # Ловкость
    self.ch = int(stats[5]) # Харизма
    self.member = member

# Инициализация персонажей
def getPers():
  persons = {}
  PersonsFile = open('persons.txt')
  for line in PersonsFile:
    P1 = line.split(',')
    P2 = P1[1].split('-')
    P3 = P2[1].split('/')
    P4 = Pers(P2[0], P3, P1[0])
    persons[int(P1[0])] = P4
  PersonsFile.close
  return persons

def savePers(persons):
  PersonsFile = open('persons.txt', 'w')
  for key in persons:
    value = persons[key]
    s = value
    stats = [str(s.hp), str(s.ar), str(s.it),
    str(s.pw), str(s.dx), str(s.ch)]
    P3 = "/".join(stats)
    P2 = value.name + '-' + P3
    P1 = str(value.member) + ',' + P2
    PersonsFile.write(P1 + enter)
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
@bot.command() # Показывает хар-ки
async def stats(ctx):
  persons = getPers()
  member = ctx.author.id
  Person = persons.get(member)
  disc = '**Имя:** ' + Person.name + enter + enter
  disc = disc + '<:heal:870700594027966464> **Здоровье:** ' + str(Person.hp) + enter
  disc = disc + '<:armor:870700741990416414> **Защита:** ' + str(Person.ar)+ enter
  disc = disc + '<:inti:870763465650892820> **Интеллект:** ' + str(Person.it) + enter
  disc = disc + '<:power:870763303004143687> **Сила:** ' + str(Person.pw) + enter
  disc = disc + '<:dx:870763635511812166> **Ловкость:** ' + str(Person.dx) + enter
  disc = disc + '<:ch:877141854821433355> **Харизма:** ' + str(Person.ch) + enter
  embed = FastEmbed('Характеристики', disc)
  await ctx.send(embed = embed)

@bot.command() # Изменяет хар-ку
async def edit(ctx, member: discord.Member, stat, value: int):
  persons = getPers()
  member = member.id
  Person = persons.get(member)
  Person.statsDict[stat] = value
  savePers(persons)
  await ctx.send(Person.name + str(Person.statsDict))

@bot.command() # Создает нового персонажа
async def newpers(ctx, *, name):
  persons = getPers()
  memberId = ctx.author.id
  P4 = Pers(name, ['100', '2', '2', '2', '2', '4'], memberId)
  persons[memberId] = P4
  await ctx.send(P4.name + str(P4.statsDict))
  Person = persons[memberId]
  await ctx.send(Person.name + str(Person.statsDict))
  savePers(persons)
# run
bot.run(os.environ['TOKEN'])