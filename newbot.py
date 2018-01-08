import asyncio
import aiohttp
import json
import random
import re
import time
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
bot = commands.Bot(command_prefix='?', description=description)

prev_message = None

async def qotd_bg_task():
	await bot.wait_until_ready()
	qod_filename = 'qod.json'
	while True:
		try:
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
				else:
					print('HTTP Error: {0}'.format(response.status))
		except asyncio.CancelledError:
			print('Got asyncio.CancelledError')
			pass

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
	global prev_message
	
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
		qod_filename = 'qod.json'
		if Path(qod_filename).is_file():
			print('File exists')
			qod_data = json.load(open(qod_filename))
			print(qod_data['contents']['quotes'][0]['quote'])
			await bot.send_message(message.channel, '''```asciidoc\nQuote of the Day for {0}\n"{1}"\n-{2}```'''.format(
										qod_data['contents']['quotes'][0]['date'],
										qod_data['contents']['quotes'][0]['quote'], 
										qod_data['contents']['quotes'][0]['author']))
		else:
			print('Missing qod file')
			async with aiohttp.get("http://quotes.rest/qod.json") as response:
				data = await response.json()
				print(data)
				with open(qod_filename, 'w') as outfile:
					json.dump(data, outfile)
					outfile.close()
		return

	''' 
	
	Bot commands list 
	
	'''
	if msg.startswith('!'):
		if '!help' in msg:
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

		elif '!8ball' in msg:
			await bot.send_message(message.channel, 'Magic 8-ball says: {0}'.format(random.sample(magic_8ball_items, 1)[0]))
		
		elif '!conch' in msg:
			await bot.send_message(message.channel, "Conch: " + random.choice([k for k in conch_items for dummy in range(conch_items[k])]))

		elif '!cleanup' in msg and message.author.id == IDs['Eduard']:
			def is_me(m):
				return m.author == bot.user

			deleted = await bot.purge_from(message.channel, limit=50, check=is_me)
			await bot.send_message(message.channel, 'Deleted {0} messages.'.format(len(deleted)))

		elif '!crypto' in msg:
			if len(msg.split()) == 2:
				url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
				async with aiohttp.get(url) as crypto_response:
					if crypto_response.status == 200:
						crypto_data = await crypto_response.json()
						for c in crypto_data:
							if c['symbol'].lower() == message.content.split()[1].lower():
								await bot.send_message(message.channel, '{0} is at ${1} USD'.format(c['name'], c['price_usd']))
								return
						await bot.send_message(message.channel, '{0} is not a known cryptocurrency'.format(message.content.split()[1].upper()))
					else:
						print('HTTP Error: {0} {1}'.format(crypto_response.status, crypto_response.text))
			else:
				await bot.send_message(message.channel, 'Incorrect usage. Use "!crypto XYZ, where XYZ is the symbol of the currency."')

		elif '!emojiparty' in msg:
			emoji_count = len(message.server.emojis)
			if emoji_count > 20:
				emoji_count = 20
			random_emojis = random.sample(message.server.emojis, emoji_count)
			for e in random_emojis:
				await bot.add_reaction(message, "{0}:{1}".format(e.name, e.id))

		elif '!lootbox' in msg:
			weapon_type = random.choice(list({'Kinetic', 'Energy', 'Power'}))
			if weapon_type == 'Kinetic':
				weapons = kinetic_weapons.copy()
			elif weapon_type == 'Energy':
				weapons = energy_weapons.copy()
			else:
				weapons = power_weapons.copy()
			lootbox_roll = random.randint(1,100)
			if lootbox_roll > 95:
				rarity = 'Exotic'
			else:
				rarity = 'Legendary'
			category, weapon_list = random.choice(list(weapons[rarity].items()))
			await bot.send_message(message.channel, "<@{0}> rolled a {1} {2} weapon {3}: {4}".format(
													message.author.id, rarity, weapon_type, category, random.choice(list(weapon_list))))

		elif '!poll' in msg:
			if len(msg.split()) > 3:
				poll_items = []
				for item in re.findall('"([^"]*)"', message.content):
					poll_items.append('{0}'.format(item))
				if len(poll_items) < 2:
					await bot.send_message(message.channel, 'Error: Not enough poll options')
					return
				else:
					poll_url = 'https://strawpoll.me/api/v2/polls'
					data = {
						"title": "Quick Poll",
						"options": poll_items
					}
					req = await aiohttp.post(poll_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
					if req.status == 200:
						poll_data = await req.json()
						await bot.send_message(message.channel, 'Poll created for <@{0}>: http://www.strawpoll.me/{1}'.format(
																		message.author.id, poll_data['id']))
			else:
				await bot.send_message(message.channel, 'Usage: !poll "AA" "BB BB" ... "ZZZ"')

		elif '!qotd' in msg or '!quote' in msg:
			qod_filename = 'qod.json'
			if not Path(qod_filename).is_file():
				print('QOTD file missing during command, getting new qotd')
				async with aiohttp.get('http://quotes.rest/qod.json') as response:
					if response.status == 200:
						data = await response.json()
						with open(qod_filename, 'w') as outfile:
							json.dump(data, outfile)
							outfile.close()
					else:
						print('QOTD GET failed with error: {0}'.format(response.status))
						return
			qod_data = json.load(open(qod_filename))
			await bot.send_message(message.channel, '''```asciidoc\nQuote of the Day for {0}\n\n"{1}"\n\n-{2}```'''.format(
									qod_data['contents']['quotes'][0]['date'],
									qod_data['contents']['quotes'][0]['quote'],
									qod_data['contents']['quotes'][0]['author']))

		elif '!timer' in msg:
			if len(msg.split()) == 2:
				if msg.split()[1].isdigit():
					duration = int(msg.split()[1])
					if duration > 60:
						duration = 60
					await bot.send_message(message.channel, '{0} minute timer set for <@{1}>'.format(int(duration), message.author.id))
					await asyncio.sleep(int(duration)*60)
					await bot.send_message(message.channel, '<@{0}> {1} minute timer is done!'.format(message.author.id, int(duration)))
				else:
					await bot.send_message(message.channel, 'Incorrect usage. Use a number for time.')
			else:
				await bot.send_message(message.channel, 'Incorrect usage. use "!timer X" ')

		elif '!unfair' in msg:
			await bot.send_message(message.channel, "{0} is unfair\n<@{1}> is in there\nStandin' at the concession\nPlottin' his oppression\n#FreeMe -<@{2}>".format(
																		message.server, IDs['Jesse'], bot.user.id))

		elif '!yesno' in msg:
			await bot.send_message(message.channel, random.choice([k for k in yesno_items for dummy in range(yesno_items[k])]))

		else:
			tmp_msg = await bot.send_message(message.channel, 'Unknown command! Cleaning up in 5s...')
			await asyncio.sleep(5)
			await bot.delete_message(message)
			await bot.delete_message(tmp_msg)

		return

	'''

	Reaction commands

	'''
	if msg.startswith('%') and prev_message != None:
		if '%list' in msg:
			#e_list = ""
			for e in message.server.emojis:
				#e_list += str('{0}\n'.format(e))
				print(e)
				#await bot.send_message(message.channel, e)
			#await bot.send_message(message.channel, 'All available emojis in this server:\n{0}'.format(e_list))

		elif '%bm' in msg:
			if message.author.id == IDs['Eduard']:
				tmp = await bot.get_message(message.channel, msg.split()[1])
				await bot.add_reaction(tmp, 'bee1:398954477199163432')
				await bot.add_reaction(tmp, 'bee2:398954523353153536')
				await bot.add_reaction(tmp, 'bee3:398954519595319296')
				await bot.add_reaction(tmp, 'bee4:398954518244622338')
				await bot.add_reaction(tmp, 'bee5:398954526364663809')
				await bot.add_reaction(tmp, 'bee6:398954519675011072')
				await bot.delete_message(message)

			else:
				await bot.delete_message(message)
				await bot.send_message(message.channel, 'Only <@{0}> can use that command.'.format(IDs['Eduard']))

		elif '%boi' in msg:
			await bot.add_reaction(prev_message, 'boi:398682539155390465')
			await bot.delete_message(message)

		elif '%waiting' in msg:
			await bot.add_reaction(prev_message, 'waiting:398718247295516672')
			await bot.delete_message(message)

		else:
			await bot.send_message(message.channel, 'Unknown reaction command.')

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

	if 'snowflake' in msg:
		await bot.add_reaction(message, '❄')

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
		await bot.send_message(message.channel, '┬─┬ ノ( ゜-゜ノ) - Calm down <@{0}>'.format(message.author.id))

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

	uganda1 = ['do', 'due', 'du', 'dyu']
	uganda2 = ['you', 'u', 'yu', 'yo', 'ue']
	uganda3 = ['know', 'kno', 'no', 'knw']
	uganda4 = ['the', 'teh', 'de', 'da']
	uganda5 = ['way', 'wai', 'weigh', 'whey', 'wei', 'wae']
	'''
	if any(u1 in msg for u1 in uganda1):
		if any(u2 in msg for u2 in uganda2):
			if any(u3 in msg for u3 in uganda3):
				if any(u4 in msg for u4 in uganda4):
					if any(u5 in msg for u5 in uganda5):
						await bot.add_reaction(message, 'UgandanWarrior:398354889346121738')
	'''
	if (
		any(u1 in msg for u1 in uganda1) and
		any(u2 in msg for u2 in uganda2) and
		any(u3 in msg for u3 in uganda3) and
		any(u4 in msg for u4 in uganda4) and
		any(u5 in msg for u5 in uganda5)
		) or (
		'uganda' in msg) or (
		'devil' in msg):
		await bot.add_reaction(message, 'UgandanWarrior:398354889346121738')

	prev_message = message

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
