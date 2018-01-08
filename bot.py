import discord
from discord.ext import commands

description = ''' Squid Squad Bot '''
bot = commands.Bot(command_prefix='!', description=description)

''' Import Dictionaries '''
from IDs import IDs

@bot.event
async def on_ready():
	await bot.edit_profile(username="Squid Squad BOT")
	await bot.change_presence(game=discord.Game(name='Big Brother'))
	print('-----------------------------------------------------------')
	print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
	print('-----------------------------------------------------------')

bot.run(IDs['TestToken'])
