import aiohttp
import json

import discord
from discord.ext import commands

description = ''' Squid Squad Bot '''
bot = commands.Bot(command_prefix='!', description=description)

''' Import Dictionaries '''
from dictionaries.IDs import IDs

@bot.event
async def on_message(msg):
	# Ignore Bot messages
	if msg.author.id == IDs['ProdBot'] or msg.author.id == IDs['TestBot']:
		return

	# Output received message to Python console
	line = '{0};;{1}'.format(msg.author, msg.content)
	print('Chat: {0}'.format(line))

	# Log line - Ignore messages from Test Server
	if msg.server.id != IDs['TestServer']:
		f = open('logs/chat_history.log', 'a')
		f.write('\n{0}'.format(line))
		f.close()

	# Create lowercase version of msg
	m = msg.content.lower()

	#
	# Block of automated reactions based on message text
	#

	if 'bet' in m:
		await bot.add_reaction(msg, '🇧')
		await bot.add_reaction(msg, '🇪')
		await bot.add_reaction(msg, '🇹')

	if 'brb' in m:
		if msg.author.id == IDs['Jesse']:
			await bot.send_file(msg.channel, 'images/JesseBRB.jpg')
		elif 'jeremybrb' not in m and 'chrisbrb' not in m and 'vincebrb' not in m:
			await bot.add_reaction(msg, 'JesseBRB:334162261922807808')

	if 'snow' in m or 'tahoe' in m:
		await bot.add_reaction(msg, '❄')

	if 'taco' in m:
		if 'bavo' in m:
			await bot.add_reaction(msg, '🚫')
			await bot.send_message(msg.channel, 'PSA by <@{0}>: AVOID TACO BRAVO'.format(IDs['Leon']))
			await bot.send_file(msg.channel, 'images/HereLiesLeon.png')
		else:
			await bot.add_reaction(msg, '🌮')

	if 'ww@' in m:
		await bot.add_reaction(msg, 'TryAskingAgain:355216367324233730')

	if '(╯°□°）╯︵ ┻━┻' in m:
		await bot.send_message(msg.channel, '┬─┬ ノ( ゜-゜ノ) - Calm down <@{0}>'.format(msg.author.id))

	#
	# Reactions based on game titles
	#

	if ('aram' in m or 'destiny' in m or 'overwatch' in m) or\
		('league' in m and 'rocket' not in m):
		await bot.add_reaction(msg, '💩')

	if 'pubg' in m or 'fortnite' in m:
		await bot.add_reaction(msg, '🇵')
		await bot.add_reaction(msg, '🇺')
		await bot.add_reaction(msg, '🇧')
		await bot.add_reaction(msg, '🇬')
		await bot.add_reaction(msg, '❔')

	if 'raid' in m or 'prestige' in m:
		if 'lair' in m:
			await bot.add_reaction(msg, '🇱')
			await bot.add_reaction(msg, '🇦')
			await bot.add_reaction(msg, '🇮')
			await bot.add_reaction(msg, '🇷')
			await bot.add_reaction(msg, '❔')
		else:
			await bot.add_reaction(msg, '🇷')
			await bot.add_reaction(msg, '🇦')
			await bot.add_reaction(msg, '🇮')
			await bot.add_reaction(msg, '🇩')
			await bot.add_reaction(msg, '❔')

	if 'vr' in m and 'chat' in m:
		await bot.add_reaction(msg, '🇻')
		await bot.add_reaction(msg, '🇷')
		await bot.add_reaction(msg, '🇨')
		await bot.add_reaction(msg, '🇭')
		await bot.add_reaction(msg, '🇦')
		await bot.add_reaction(msg, '🇹')

	#
	# Very Meme-based reactions
	#

	uganda1 = ['do', 'due', 'du', 'dyu']
	uganda2 = ['you', 'u', 'yu', 'yo', 'ue']
	uganda3 = ['know', 'kno', 'no', 'knw']
	uganda4 = ['the', 'teh', 'de', 'da']
	uganda5 = ['way', 'wai', 'weigh', 'whey', 'wei', 'wae']

	if (any(u1 in m for u1 in uganda1) and
		any(u2 in m for u2 in uganda2) and
		any(u3 in m for u3 in uganda3) and
		any(u4 in m for u4 in uganda4) and
		any(u5 in m for u5 in uganda5)) or\
		'uganda' in m or\
		'devil' in m or\
		'queen' in m:
		await bot.add_reaction(msg, 'UgandanWarrior:398354889346121738') 

	#
	# End automated reactions block
	#

	# Process ! commands
	await bot.process_commands(msg)

@bot.command(pass_context=True)
async def crypto(ctx, currency: str):
	print('in crypto function')
	url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
	async with aiohttp.get(url) as response:
		if response.status == 200:
			data = await response.json()
			for c in data:
				if c['symbol'].lower() == currency.split()[0].lower():
					await bot.send_message(ctx.message.channel, '{0} is at ${1} USD'.format(c['name'], c['price_usd']))
					return
			await bot.send_message(ctx.message.channel, '{0} is not a known cryptocurrency'.format(currency.split()[0].upper()))
		else:
			print('HTTP Error: {0} {1}'.format(response.status, response.text))

#async def crypto(ctx, *, msg: str):
#	print('{0} said "{1}", but msg picked up "{2}"'.format(
#				ctx.message.author, ctx.message.content, msg))

@bot.event
async def on_command_error(error, ctx):
	print('Command error! {0}'.format(error))
	

@bot.event
async def on_ready():
	# await bot.edit_profile(username="Squid Squad BOT")
	await bot.change_presence(game=discord.Game(name='Testing Sim'))
	print('-----------------------------------------------------------')
	print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
	print('-----------------------------------------------------------')

bot.run(IDs['TestToken'])
