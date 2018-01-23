import aiohttp
import asyncio
import json
import operator
import os
import random
import re

import discord
from discord.ext import commands
from pathlib import Path

''' Import custom modules '''
from cmds.carjesse import *
from cmds.cleanup import *
from cmds.crypto import *
from cmds.decision import *
from cmds.emojiparty import *
from cmds.help import *
from cmds.lootbox import *
from cmds.music import *
from cmds.misc import *
from cmds.poll import *
from cmds.pubg import *
from cmds.qotd import *
from cmds.react import *
from cmds.reminders import *
from cmds.twitch import *

''' Import Dictionaries '''
from dictionaries.IDs import IDs
from dictionaries.destiny_lists import *
from dictionaries.help_docs import *
from dictionaries.lists import *
from dictionaries.pubg_lists import *

''' Global Variables '''
if 'prodbot' in os.path.dirname(os.path.realpath(__file__)):
	PROD = 1
else:
	PROD = 0

squidcoin_base = {}
squidcoin_ready = 1
squidcoin_file = '/home/pi/squidcoin.base'
''' End Global Variables '''

''' Load Opus for Music Bot '''
if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
	discord.opus.load_opus('opus')

''' Create Bot '''
description = ''' Squid Squad Bot '''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')
bot.add_cog(CarJesse(bot))
bot.add_cog(Cleanup(bot))
bot.add_cog(Conch(bot))
bot.add_cog(Crypto(bot))
bot.add_cog(EmojiParty(bot))
bot.add_cog(Help(bot))
bot.add_cog(Lootbox(bot))
bot.add_cog(Magic8(bot))
bot.add_cog(Music(bot))
bot.add_cog(Poll(bot))
bot.add_cog(Pubg(bot))
bot.add_cog(Qotd(bot))
bot.add_cog(React(bot))
bot.add_cog(Timer(bot))
bot.add_cog(TwitchLive(bot))
bot.add_cog(Unfair(bot))
bot.add_cog(Yesno(bot))

async def reactToMsg(msg, reactions):
	for r in reactions:
		await bot.add_reaction(msg, r)

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
	global squidcoin_base
	global squidcoin_file

	# When someone makes a messages, they're guaranteed up to .05 squidcoin
	amount = random.randint(1,50)*0.001

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
		rx = ['🇧', '🇪', '🇹']
		await reactToMsg(msg, rx)
		amount += random.randint(1,20)*0.01

	if 'brb' in m:
		if msg.author.id == IDs['Jesse']:
			pictures = ['JesseBRB.jpg', 'JesseBRB2.jpg', 'JesseBRB3.jpg', 'JesseBRB4.jpg']
			picture = random.choice(pictures)
			await bot.send_file(msg.channel, 'images/{0}'.format(picture))
		elif 'jeremybrb' not in m and 'chrisbrb' not in m and 'vincebrb' not in m:
			await bot.add_reaction(msg, 'JesseBRB:334162261922807808')
		if not msg.author.voice_channel is None and m == 'brb':
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
			await bot.send_file(msg.channel,
				'images/HereLiesLeon.png',
				content='PSA by <@{0}>: AVOID TACO BRAVO'.format(IDs['Leon']))
		else:
			await bot.add_reaction(msg, '🌮')
		amount += random.randint(1,20)*0.01

	if 'tfti' in m:
		rx = ['tfti_t1:401227546504724491', 'tfti_f:401227559653867531', 
				'tfti_t2:401227576024104960', 'tfti_i:401227586039971840']
		await reactToMsg(msg, rx)
		amount += random.randint(1,35)*0.01

	if 'ww@' in m:
		rx = ['wwat_w_1:400486976454787083', 'wwat_w_2:400487029634498561',
				'wwat_at:400487716892180498']
		await reactToMsg(msg, rx)
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

	if ('pubg' in m or 'fortnite' in m) and\
		('!pubg' not in m):
		rx = ['🇵', '🇺', '🇧', '🇬', '❔']
		await reactToMsg(msg, rx)
		amount += random.randint(1,30)*0.01

	if 'raid' in m or 'prestige' in m:
		if 'lair' in m:
			rx = ['🇱', '🇦', '🇮', '🇷', '❔']
			await reactToMsg(msg, rx)
		else:
			rx = ['🇷', '🇦', '🇮', '🇩', '❔']
			await reactToMsg(msg, rx)
		amount += random.randint(1,60)*0.01

	if 'vr' in m and 'chat' in m:
		rx = ['🇻', '🇷', '🇨', '🇭', '🇦', '🇹']
		await reactToMsg(msg, rx)
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

	# Process ! commands
	await bot.process_commands(msg)

#
# Bot commands
#

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

	rank_msg = 'Squidcoin rankings:\n'
	for r in ranks:
		rank_msg += '<@{0}> : {1}\n'.format(r[0], r[1])
	tmp = await bot.send_message(ctx.message.channel, rank_msg)
	await asyncio.sleep(15)
	await bot.delete_message(tmp)
	await bot.delete_message(ctx.message)

@squidcoin.command(pass_context=True)
async def tip(ctx, *, args: str):
	global squidcoin_base
	global squidcoin_file

	# Try to extract the recipient's ID
	try:
		person_id = re.search('<@!(.+?)>', args.split()[0]).group(1)
	except AttributeError:
		tmp = await bot.say('First argument needs to be a server member')
		await asyncio.sleep(10)
		await bot.delete_message(tmp)
		await bot.delete_message(ctx.message)
		return
	
	# Make sure person doesn't tip themselves
	if person_id == ctx.message.author.id:
		tmp = await bot.say('You cannot tip yourself <@{0}>'.format(person_id))
		await asyncio.sleep(10)
		await bot.delete_message(tmp)
		await bot.delete_message(ctx.message)
		return

	# Search if member is in the server
	found = 0
	for m in ctx.message.server.members:
		if m.id == person_id:
			found = 1
			break
	if found == 0:
		tmp = await bot.say('That person does not exist in the server')
		await asyncio.sleep(10)
		await bot.delete_message(tmp)
		await bot.delete_message(ctx.message)
		return

	amount = args.split()[1]

	# Check that amount was vaid number
	if not amount.isdigit():
		tmp = await bot.say('Enter a number amount <@{0}>'.format(ctx.message.author.id))
		await asyncio.sleep(10)
		await bot.delete_message(tmp)
		await bot.delete_message(ctx.message)
		return
	
	# Check if member has that much
	print(int(amount))
	print(squidcoin_base[ctx.message.author.id])
	if int(amount) > squidcoin_base[ctx.message.author.id]:
		tmp = await bot.say('<@{0}> do not have {1} to tip'.format(ctx.message.author.id, amount))
		await asyncio.sleep(10)
		await bot.delete_message(tmp)
		await bot.delete_message(ctx.message)
		return

	# deduct amount from member in squidcoinbase
	squidcoin_base[ctx.message.author.id] -= int(amount)
	squidcoin_base[person_id] += int(amount)

	with open(squidcoin_file, 'w') as outfile:
		json.dump(squidcoin_base, outfile)
		outfile.close()

	await bot.say('<@{0}> tips {1} to <@{2}>'.format(ctx.message.author.id,
										amount,
										person_id))

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

@bot.event
async def on_ready():
	global PROD
	if PROD:
		await bot.change_presence(game=discord.Game(name='Big Brother 3.4.0'))
	else:
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
