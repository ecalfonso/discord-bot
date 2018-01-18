import aiohttp
import asyncio
import json
import operator
import random
import re

import discord
from discord.ext import commands
from pathlib import Path
from music_bot import *

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
	discord.opus.load_opus('opus')

description = ''' Squid Squad Bot '''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')
bot.add_cog(Music(bot))

''' Import Dictionaries '''
from dictionaries.IDs import IDs
from dictionaries.destiny_lists import *
from dictionaries.help_docs import *
from dictionaries.lists import *

''' Global Variables '''
PROD = 0
prev_msg = None

squidcoin_base = {}
squidcoin_ready = 1
squidcoin_file = '/home/pi/squidcoin.base'

async def squidcoin_generator():
	global squidcoin_ready

	while(1):
		# Make coins available after a random interval between 1 and 15 minutes
		mins = random.randint(1,15)
		await asyncio.sleep(60*mins)
		squidcoin_ready = 1

async def squidcoin_init():
	await bot.wait_until_ready()

	global squidcoin_base
	global squidcoin_ready
	global squidcoin_file

	if Path(squidcoin_file).is_file():
		squidcoin_base = json.load(open(squidcoin_file))
	else:
		print('Squidcoinbase file not found!')

@bot.event
async def on_reaction_add(rx, user):
	# Log all reactions and the User who created them
	line = '{0};;{1}'.format(user, rx.emoji)
	print('Reaction: {0}'.format(line))

	# Ignore logging for Text Server
	if user.server.id != IDs['TestServer']:
		f = open('logs/emoji_history.log', 'a')
		f.write('\n{0}'.format(line))
		f.close()

@bot.event
async def on_message(msg):
	global prev_msg
	global squidcoin_base
	global squidcoin_file

	# Ignore Bot messages
	if msg.author.id == IDs['ProdBot'] or msg.author.id == IDs['TestBot'] or \
		msg.author.id == IDs['TwitchBot'] or msg.author.id == IDs['GithubBot']:
		return

	# When someone makes a messages, they're guaranteed up to .05 squidcoin
	amount = random.randint(1,50)*0.001

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
		amount += random.randint(1,20)*0.01

	if 'brb' in m:
		if msg.author.id == IDs['Jesse']:
			pictures = ['JesseBRB.jpg', 'JesseBRB2.jpg', 'JesseBRB3.jpg', 'JesseBRB4.jpg']
			picture = random.choice(pictures)
			await bot.send_file(msg.channel, 'images/{0}'.format(picture))
		elif 'jeremybrb' not in m and 'chrisbrb' not in m and 'vincebrb' not in m:
			await bot.add_reaction(msg, 'JesseBRB:334162261922807808')
		if not msg.author.voice_channel is None:
			await bot.move_member(msg.author, msg.server.afk_channel)
		amount += random.randint(1,35)*0.01

	if 'mock' in m:
		mock_str = ""
		flip = 0
		for l in m:
			if l.isalpha():
				if flip == 0:
					mock_str += l
					flip = 1
				else:
					mock_str += l.upper()
					flip = 0
			else:
				mock_str += l
		print(mock_str)
		await bot.send_message(msg.channel, '<@{0}>: {1}'.format(msg.author.id, mock_str))
		amount += random.randint(1,20)*0.01

	if 'snow' in m or 'tahoe' in m:
		await bot.add_reaction(msg, '❄')
		amount += random.randint(1,40)*0.01

	if 'taco' in m:
		if 'bravo' in m:
			await bot.add_reaction(msg, '🚫')
			await bot.send_message(msg.channel, 'PSA by <@{0}>: AVOID TACO BRAVO'.format(IDs['Leon']))
			await bot.send_file(msg.channel, 'images/HereLiesLeon.png')
		else:
			await bot.add_reaction(msg, '🌮')
		amount += random.randint(1,20)*0.01

	if 'tfti' in m:
		await bot.add_reaction(msg, 'tfti_t1:401227546504724491')
		await bot.add_reaction(msg, 'tfti_f:401227559653867531')
		await bot.add_reaction(msg, 'tfti_t2:401227576024104960')
		await bot.add_reaction(msg, 'tfti_i:401227586039971840')
		amount += random.randint(1,35)*0.01

	if 'ww@' in m:
		await bot.add_reaction(msg, 'wwat_w_1:400486976454787083')
		await bot.add_reaction(msg, 'wwat_w_2:400487029634498561')
		await bot.add_reaction(msg, 'wwat_at:400487716892180498')
		amount += random.randint(1,30)*0.01

	if '(╯°□°）╯︵ ┻━┻' in m:
		await bot.send_message(msg.channel, '┬─┬ ノ( ゜-゜ノ) - Calm down <@{0}>'.format(msg.author.id))
		amount += random.randint(1,100)*0.01

	#
	# Reactions based on game titles
	#

	if ('aram' in m or 'destiny' in m or 'overwatch' in m) or\
		('league' in m and 'rocket' not in m):
		await bot.add_reaction(msg, '💩')
		amount += random.randint(1,40)*0.01

	if 'pubg' in m or 'fortnite' in m:
		await bot.add_reaction(msg, '🇵')
		await bot.add_reaction(msg, '🇺')
		await bot.add_reaction(msg, '🇧')
		await bot.add_reaction(msg, '🇬')
		await bot.add_reaction(msg, '❔')
		amount += random.randint(1,30)*0.01

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
		amount += random.randint(1,60)*0.01

	if 'vr' in m and 'chat' in m:
		await bot.add_reaction(msg, '🇻')
		await bot.add_reaction(msg, '🇷')
		await bot.add_reaction(msg, '🇨')
		await bot.add_reaction(msg, '🇭')
		await bot.add_reaction(msg, '🇦')
		await bot.add_reaction(msg, '🇹')
		amount += random.randint(1,70)*0.01

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
		amount += random.randint(1,20)*0.01

	#
	# End automated reactions block
	#

	#
	# Add message amount to squidcoin
	#
	if msg.author.id in squidcoin_base:
		squidcoin_base[msg.author.id] += amount
	else:
		squidcoin_base[msg.author.id] = amount
	with open(squidcoin_file, 'w') as outfile:
		json.dump(squidcoin_base, outfile)
		outfile.close()

	if not m.startswith('!'):
		prev_msg = msg

	# Process ! commands
	await bot.process_commands(msg)

#
# Bot commands
#

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

@help.command(pass_context=True)
async def react(ctx):
	await bot.send_message(ctx.message.channel, help_react)

@help.command(pass_context=True)
async def squidcoin(ctx):
	await bot.send_message(ctx.message.channel, help_squidcoin)

@bot.command(pass_context=True)
async def carjesse(ctx, args: str):
	await bot.send_file(ctx.message.channel, 
						'images/CarJesse.png',
						content="Car <@{0}> has arrived! Vroom vroom".format(IDs['Jesse']),
						tts=((ctx.message.author.id == IDs['Eduard'] or ctx.message.author.id == IDs['Jesse']) and
								'tts' in args.lower())
						)

@carjesse.error
async def carjesse_err(error, ctx):
	await bot.send_file(ctx.message.channel,
						'images/CarJesse.png',
						content="Car <@{0}> has arrived! Vroom vroom".format(IDs['Jesse']),
						)

@bot.command(pass_context=True)
async def cleanup(ctx):
	def is_me(m):
		return m.author == bot.user

	deleted = await bot.purge_from(ctx.message.channel, limit=50, check=is_me)
	await bot.send_message(ctx.message.channel, 'Deleted {0} messages.'.format(len(deleted)))
	await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def conch(ctx):
	await bot.send_message(ctx.message.channel, 'Conch: {0}'.format(
									random.choice([k for k in conch_items for dummy in range(conch_items[k])])))

@bot.command(pass_context=True)
async def crypto(ctx, symbol: str):
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
async def magic8(ctx):
	await bot.send_message(ctx.message.channel, 'Magic 8-ball says: {0}'.format(random.sample(magic_8ball_items, 1)[0]))

@bot.command(pass_context=True)
async def poll(ctx, *, opts: str):
	if len(opts.split()) > 1:
		poll_items = []
		for item in re.findall('"([^"]*)"', opts):
			poll_items.append('{0}'.format(item))

		poll_url = 'https://strawpoll.me/api/v2/polls'
		data = {
			"title": "Quick Poll",
			"options": poll_items
		}

		async with aiohttp.post(poll_url, data=json.dumps(data), headers={"Content-Type": "application/json"}) as response:
			if response.status == 200:
				poll_data = await response.json()
				await bot.send_message(ctx.message.channel, 'Poll created for <@{0}>: http://www.strawpoll.me/{1}'.format(
												ctx.message.author.id, poll_data['id']))
	else:
		await bot.send_message(ctx.message.channel, 'Error: Not enough poll options')

@poll.error
async def poll_err(error, ctx):
	await bot.send_message(ctx.message.channel, 'Usage: !poll "AA" "BB BB" ... "ZZZ"')

@bot.command(pass_context=True)
async def qotd(ctx):
	url = 'http://quotes.rest/qod.json'
	async with aiohttp.get(url) as response:
		if response.status == 200:
			data = await response.json()
			await bot.send_message(ctx.message.channel, '''```asciidoc\nQuote of the Day for {0}\n\n"{1}"\n\n-{2}```'''.format(
									data['contents']['quotes'][0]['date'],
									data['contents']['quotes'][0]['quote'],
									data['contents']['quotes'][0]['author']))
		else:
			print('QOTD GET failed with error: {0}'.format(response.status))
			await bot.say('QOTD Request failed!')
			return

@bot.group(pass_context=True)
async def squidcoin(ctx):
	global squidcoin_base
	
	if ctx.invoked_subcommand is None:
		msg = await bot.send_message(ctx.message.channel, help_squidcoin)
		await asyncio.sleep(30)
		await bot.delete_message(msg)
		await bot.delete_message(ctx.message)

@squidcoin.command(pass_context=True)
async def getcoin(ctx):
	global squidcoin_base
	global squidcoin_file
	global squidcoin_ready

	if squidcoin_ready == 1:
		squidcoin_ready = 0
		await bot.say('<@{0}> claimed a squidcoin!'.format(ctx.message.author.id))
		if ctx.message.author.id in squidcoin_base:
			squidcoin_base[ctx.message.author.id] += 1
		else:
			squidcoin_base[ctx.message.author.id] = 1
		with open(squidcoin_file, 'w') as outfile:
			json.dump(squidcoin_base, outfile)
			outfile.close()
	else:
		msg = await bot.say('Coin not available yet')
		await asyncio.sleep(10)
		await bot.delete_message(msg)
		await bot.delete_message(ctx.message)

@squidcoin.command(pass_context=True)
async def ranking(ctx):
	global squidcoin_base

	ranks = sorted(squidcoin_base.items(), key=operator.itemgetter(1), reverse=True)
	print(ranks)

	rank_msg = 'Squidcoin rankings:\n'
	for r in ranks:
		rank_msg += '<@{0}> : {1}\n'.format(r[0], r[1])
	tmp = await bot.send_message(ctx.message.channel, rank_msg)
	await asyncio.sleep(15)
	await bot.delete_message(tmp)

@squidcoin.command(pass_context=True)
async def wallet(ctx):
	global squidcoin_base
	if ctx.message.author.id in squidcoin_base:
		msg = await bot.say('<@{0}> has {1} squidcoin!'.format(ctx.message.author.id, squidcoin_base[ctx.message.author.id]))
	else:
		msg = await bot.say('<@{0}> has no squidcoin.'.format(ctx.message.author.id))
	await asyncio.sleep(10)
	await bot.delete_message(msg)
	await bot.delete_message(ctx.message)

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

@bot.command(pass_context=True)
async def twitchlive(ctx, *, data: str):
	if ctx.message.author.id == IDs['TwitchHookBot']:
		if data.split(';;;')[0] in twitchIDs:
			name = twitchIDs[data.split(';;;')[0]]
			game = data.split(';;;')[1]
			link = data.split(';;;')[2]
			await bot.send_message(bot.get_channel(IDs['Squid Squad General Channel']), '<@{0}> started playing {1} on Twitch! <{2}>'.format(
																		name, game, link))

@bot.command(pass_context=True)
async def unfair(ctx):
	await bot.send_message(ctx.message.channel, "{0} is unfair\n<@{1}> is in there\nStandin' at the concession\nPlottin' his oppression\n#FreeMe -<@{2}>".format(
																									ctx.message.server, IDs['Jesse'], bot.user.id))

@bot.command(pass_context=True)
async def yesno(ctx):
	await bot.send_message(ctx.message.channel, random.choice([k for k in yesno_items for dummy in range(yesno_items[k])]))

#
# Reaction commands
#

@bot.group(pass_context=True)
async def react(ctx):
	if ctx.invoked_subcommand is None:
		await bot.send_message(ctx.message.channel, 'Incorrect usage: "!react <emote>". Use "!react list" to display all emojis')

@react.command(pass_context=True)
async def showme(ctx):
	await bot.delete_message(ctx.message)
	for e in ctx.message.server.emojis:
		print('{0} : {1}'.format(e.name, e.id))

@react.command(pass_context=True)
async def ls(ctx):
	await bot.send_message(ctx.message.channel, help_react)

@react.command(pass_context=True)
async def boi(ctx):
	global prev_msg
	await bot.add_reaction(prev_msg, 'boi:398682539155390465')
	await bot.delete_message(ctx.message)

@react.command(pass_context=True)
async def nsfl(ctx):
	global prev_msg
	await bot.add_reaction(prev_msg, '🇳')
	await bot.add_reaction(prev_msg, '🇸')
	await bot.add_reaction(prev_msg, '🇫')
	await bot.add_reaction(prev_msg, '🇱')
	await bot.delete_message(ctx.message)

@react.command(pass_context=True)
async def nsfw(ctx):
	await bot.add_reaction(prev_msg, '🇳')
	await bot.add_reaction(prev_msg, '🇸')
	await bot.add_reaction(prev_msg, '🇫')
	await bot.add_reaction(prev_msg, '🇼')
	await bot.delete_message(ctx.message)

@react.command(pass_context=True)
async def waiting(ctx):
	global prev_msg
	await bot.add_reaction(prev_msg, 'waiting:398718247295516672')
	await bot.delete_message(ctx.message)

#
# End Reaction commands
#

@bot.event
async def on_ready():
	global PROD
	if PROD:
		await bot.edit_profile(username="Squid Squad BOT")
		await bot.change_presence(game=discord.Game(name='Big Brother 3.2.0'))
	else:
		await bot.edit_profile(username="Test BOT")
		await bot.change_presence(game=discord.Game(name='Testing Sim'))
	print('-----------------------------------------------------------')
	print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
	print('-----------------------------------------------------------')
	await squidcoin_init()

bot.loop.create_task(squidcoin_generator())
if PROD:
	bot.run(IDs['ProdToken'])
else:
	bot.run(IDs['TestToken'])
