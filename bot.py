import aiohttp
import asyncio
import json
import random

import discord
from discord.ext import commands

description = ''' Squid Squad Bot '''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')

''' Import Dictionaries '''
from dictionaries.IDs import IDs
from dictionaries.destiny_lists import *
from dictionaries.help_docs import *
from dictionaries.lists import *

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

@bot.group(pass_context=True)
async def help(ctx):
	if ctx.invoked_subcommand is None:
		await bot.send_message(ctx.message.channel, help_default)

@help.command(pass_context=True)
async def auto(ctx):
	await bot.send_message(ctx.message.channel, help_auto)

@help.command(pass_context=True)
async def cmds(ctx):
	await bot.send_message(ctx.message.channel, help_commands)
	
@help.command(pass_context=True)
async def music(ctx):
	await bot.send_message(ctx.message.channel, help_music)

@bot.command(pass_context=True)
async def conch(ctx):
	await bot.send_message(ctx.message.channel, 'Conch: {0}'.format(
									random.choice([k for k in conch_items for dummy in range(conch_items[k])])))

@bot.command(pass_context=True)
async def crypto(ctx, symbol: str):
	print('in crypto function')
	url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
	async with aiohttp.get(url) as response:
		if response.status == 200:
			data = await response.json()
			for c in data:
				if c['symbol'].lower() == symbol.split()[0].lower():
					await bot.send_message(ctx.message.channel, '{0} is at ${1} USD'.format(c['name'], c['price_usd']))
					return
			await bot.send_message(ctx.message.channel, '{0} is not a known cryptocurrency symbol'.format(symbol.split()[0].upper()))
		else:
			print('HTTP Error: {0} {1}'.format(response.status, response.text))

@crypto.error
async def crypto_err(error, ctx):
	# Should only get in here if no arg was supplied
	await bot.send_message(ctx.message.channel, '<@{0}> No Cryptocurrency Symbol entered! Try "!crypto XRB"'.format(
																				ctx.message.author.id))

@bot.command(pass_context=True)
async def emojiparty(ctx):
	emojis = ctx.message.server.emojis
	emoji_count = min(len(emojis), 20)
	random_emoji = random.sample(emojis, emoji_count)
	for e in random_emoji:
		await bot.add_reaction(ctx.message, '{0}:{1}'.format(e.name, e.id))

@bot.command(pass_context=True)
async def lootbox(ctx):
	weapon_type = random.choice(list({'Kinetic', 'Energy', 'Power'}))
	if weapon_type == 'Kinetic':
		weapons = kinetic_weapons.copy()
	elif weapon_type == 'Energy':
		weapons = energy_weapons.copy()
	else:
		weapons = power_weapons.copy()

	roll = random.randint(1, 100)
	if roll > 95:
		rarity = 'Exotic'
	else:
		rarity = 'Legendary'
	
	category, weapons_list = random.choice(list(weapons[rarity].items()))
	await bot.send_message(ctx.message.channel, "<@{0}> rolled a {1} {2} weapon {3}: {4}".format(
	 										ctx.message.author.id, rarity, weapon_type, category, random.choice(list(weapons_list))))

@bot.command(pass_context=True)
async def timer(ctx, time: str):
	t = time.split()[0]
	if t.isdigit():
		duration = min(int(t), 60)
		await bot.send_message(ctx.message.channel, '{0} minute timer set for <@{1}>'.format(duration, ctx.message.author.id))
		await asyncio.sleep(duration*60)
		await bot.send_message(ctx.message.channel, '<@{0}> {1} minute timer is done!'.format(ctx.message.author.id, duration))
	else:
		await bot.send_message(ctx.message.channel, 'Incorrect usage. Use a number for time.')

@timer.error
async def timer_err(error, ctx):
	await bot.send_message(ctx.message.channel, 'Incorrect usage. use "!timer X" ')

@bot.event
async def on_ready():
	# await bot.edit_profile(username="Squid Squad BOT")
	await bot.change_presence(game=discord.Game(name='Testing Sim'))
	print('-----------------------------------------------------------')
	print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
	print('-----------------------------------------------------------')

bot.run(IDs['TestToken'])
