import asyncio
import aiohttp
import json
import random
import time
import urllib.request
import discord
from discord.ext import commands
from pathlib import Path

''' 

Import dictionaries 

'''
from help_docs import help_default, help_auto, help_commands, help_music
from IDs import IDs
from destiny_lists import power_weapons, kinetic_weapons, energy_weapons
from lists import magic_8ball_items, yesno_items, conch_items

description = ''' Squid Squad TEST Bot'''
bot = commands.Bot(command_prefix='!', description=description)

async def qotd_bg_task():
	await bot.wait_until_ready()
	qod_filename = 'qod.json'
	while True:
		await asyncio.sleep(30*60)
		async with aiohttp.get('http://quotes.rest/qod.json') as response:
			if response.status == 200:
				data = await response.json()
				with open(qod_filename, 'w') as outfile:
					json.dump(data, outfile)
					outfile.close()
					print('QOTD Updated')
			elif response.status == 429:
				print('HTTP Error 429, being rate limited')

@bot.event
async def on_reaction_add(reaction, user):
	''' Log all reactions and the User who reacted '''
	line = "{0};;{1}".format(user, reaction.emoji)
	print('Reaction: {0}'.format(line))

	''' Ignore logging for PTR Server '''
	if user.server.id != IDs['PTRServer']:
		f = open('logs/emoji_history.log', 'a')
		f.write('\n{0}'.format(line))
		f.close()

@bot.event
async def on_message(message):
	''' Ignore Bot Messages '''
	if message.author.id == bot.user.id:
		return

	''' Display chat message in Python output '''
	line = '{0};;{1}'.format(message.author, message.content)
	print('Chat: {0}'.format(line))

	''' Log line - Ignore chat from PTR Server '''
	if message.server.id != IDs['PTRServer']:
		f = open('logs/chat_history.log', 'a')
		f.write('\n{0}'.format(line))
		f.close()

	msg = message.content.lower()

	'''
	Test block
	'''
	if 'test' in msg and message.author.id == IDs['Eduard']:
		return

	''' 
	
	Capture the !Help command
	
	'''
	if msg.startswith('!help'):
		if len(msg.split()) == 2:
			if 'auto' in msg:
				await bot.send_message(message.channel, help_auto)
			elif 'cmds' in msg or 'commands' in msg:
				await bot.send_message(message.channel, help_commands)
			elif 'music' in msg:
				await bot.send_message(message.channel, help_music)
			else:
				await bot.send_message(message.channel, 'Unknown command!')
		else:
			await bot.send_message(message.channel, help_default)
		return

	''' 
	
	Automated Bot reactions based on message text 
	
	'''
	if 'bet' in msg:
		await bot.add_reaction(message, '🇧')
		await bot.add_reaction(message, '🇪')
		await bot.add_reaction(message, '🇹')

	if 'brb' in msg:
		if message.author.id == IDs['Jesse']:
			await bot.send_file(message.channel, 'images/JesseBRB.jpg')
		else:
			if 'jeremybrb' not in msg and 'chrisbrb' not in msg and 'vincebrb' not in msg:
				await bot.add_reaction(message, 'JesseBRB:334162261922807808')

	if 'monika' in msg:
		if 'monika' in message.content:
			await bot.send_message(message.channel, '<@{0}>: {1}'.format(message.author.id, message.content.replace('monika', 'M̢o̶͟ń͞i̛͘k̢̕a̸̡')))
			await bot.delete_message(message)
		elif 'Monika' in message.content:
			await bot.send_message(message.channel, '<@{0}>: {1}'.format(message.author.id, message.content.replace('Monika', 'M̢o̶͟ń͞i̛͘k̢̕a̸̡')))
			await bot.delete_message(message)

	if 'taco' in msg:
		if 'bravo' in msg:
			await bot.add_reaction(message, '🚫')
			await bot.send_message(message.channel, 'PSA by <@{0}>: AVOID TACO BRAVO'.format(IDs['Leon']))
			await bot.send_file(message.channel, 'images/HereLiesLeon.png')
		else:
			await bot.add_reaction(message, '🌮')

	if 'ww@' in msg:
		await bot.add_reaction(message, 'TryAskingAgain:355216367324233730')

	if '(╯°□°）╯︵ ┻━┻' in msg:
		await bot.send_message(message.channel, '┬─┬ ノ( ゜-゜ノ)')

	'''

	Game name reactions

	'''
	if ('aram' in msg 
		or 'league' in msg
		or 'destiny' in msg
		or 'overwatch' in msg
		):
		await bot.add_reaction(message, '💩')

	if ('pubg' in msg
		or 'fortnite' in msg
		):
		await bot.add_reaction(message, '🇵')
		await bot.add_reaction(message, '🇺')
		await bot.add_reaction(message, '🇧')
		await bot.add_reaction(message, '🇬')
		await bot.add_reaction(message, '❔')

	if 'raid' in msg:
		if 'lair' in msg:
			await bot.add_reaction(message, '🇱')
			await bot.add_reaction(message, '🇦')
			await bot.add_reaction(message, '🇮')
			await bot.add_reaction(message, '🇷')
			await bot.add_reaction(message, '❔')
		else:
			await bot.add_reaction(message, '🇷')
			await bot.add_reaction(message, '🇦')
			await bot.add_reaction(message, '🇮')
			await bot.add_reaction(message, '🇩')
			await bot.add_reaction(message, '❔')

	await bot.process_commands(message)

@bot.command(pass_context=True)
async def magic8ball(ctx):
	await bot.send_message(ctx.message.channel, 'Magic 8-ball says: {0}'.format(random.sample(magic_8ball_items, 1)[0]))

@crypto.error
async def crypto_error(error, ctx):
	print('{0} {1}'.format(error, ctx))

@bot.command(pass_context=True)
async def conch(ctx):
	await bot.send_message(ctx.message.channel, "Conch: " + random.choice([k for k in conch_items for dummy in range(conch_items[k])]))

@bot.command(pass_context=True)
async def crypto(ctx, symbol : str):
	print('In crypto function')
	url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
	async with aiohttp.get(url) as response:
		if response.status == 200:
			data = response.json()
			print(data)

@bot.event
async def on_ready():
	await bot.edit_profile(username="Squid Squad BOT")
	await bot.change_presence(game=discord.Game(name='Big Brother'))
	print('-----------------------------------------------------------')
	print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
	print('-----------------------------------------------------------')

bot.loop.create_task(qotd_bg_task())
#bot.loop.create_task(twitch_task())
bot.run(IDs['Token'])
