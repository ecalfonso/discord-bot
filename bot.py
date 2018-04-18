import asyncio
import datetime
import global_vars
import json
import os
import random

import discord
from discord.ext import commands
from pathlib import Path

''' Import custom modules '''
from cmds.admin import *
from cmds.crypto import *
from cmds.decision import *
from cmds.emojiparty import *
from cmds.food import *
from cmds.help import *
from cmds.jesse import *
from cmds.lootbox import *
from cmds.misc import *
from cmds.music import *
from cmds.poll import *
from cmds.pubg import *
from cmds.quotes import *
from cmds.react import *
from cmds.reminders import *
from cmds.squidcoin import *
from cmds.twitch import *
from cmds.twitter import *
from cmds.wmark import *

''' Import Dictionaries '''
from dictionaries.IDs import *
from dictionaries.destiny_lists import *
from dictionaries.help_docs import *
from dictionaries.lists import *
from dictionaries.pubg_lists import *

''' Global Variables '''
global_vars.init()

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
bot.add_cog(Admin(bot))
bot.add_cog(Conch(bot))
bot.add_cog(Crypto(bot))
bot.add_cog(EmojiParty(bot))
bot.add_cog(Food(bot))
bot.add_cog(Help(bot))
bot.add_cog(Jesse(bot))
bot.add_cog(Lootbox(bot))
bot.add_cog(Magic8(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Music(bot))
bot.add_cog(Poll(bot))
bot.add_cog(Pubg(bot))
bot.add_cog(Qotd(bot))
bot.add_cog(Quote(bot))
bot.add_cog(React(bot))
bot.add_cog(RemindMe(bot))
bot.add_cog(SquidCoin(bot))
bot.add_cog(Timer(bot))
bot.add_cog(TwitchLive(bot))
bot.add_cog(Twitter(bot))
bot.add_cog(Wmark(bot))
bot.add_cog(Yesno(bot))

async def reactToMsg(msg, reactions):
	for r in reactions:
		await bot.add_reaction(msg, r)

@bot.event
async def on_member_update(b, a):
	''' Track nicknames used '''
	if a.nick != None and\
	a.nick != b.nick:
		if Path(global_vars.nicknames_file).is_file():
			''' Load data '''
			nicknames_data = json.load(open(global_vars.nicknames_file))

			data = (a.nick, datetime.datetime.now().timestamp())

			''' Write to data '''
			if a.id in nicknames_data:
				nicknames_data[a.id].append(data)
			else:
				nicknames_data[a.id] = [data]

			''' Write back to file '''
			with open(global_vars.nicknames_file, 'w') as outfile:
				json.dump(nicknames_data, outfile)
				outfile.close()
		else:
			print('Unable to load nicknames_file')

@bot.event
async def on_reaction_add(rx, user):
	# Log all reactions and the User who created them
	line = '{0};;{1}'.format(user, rx.emoji)
	print('Reaction: {0}'.format(line))

	# Ignore logging for Text Server
	if hasattr(user, 'server') and (user.server.id != IDs['BetaServer'] or user.server.id != IDs['AlphaServer']):
		f = open('../logs/emoji_history.log', 'a')
		f.write('\n{0}'.format(line))
		f.close()

	# Add reaction amount to squidcoin
	amount = random.randint(50,100)*0.001

	if user.id in global_vars.squidcoin_data:
		global_vars.squidcoin_data[user.id] += amount
	else:
		global_vars.squidcoin_data[user.id] = amount
	with open(global_vars.squidcoin_file, 'w') as outfile:
		json.dump(global_vars.squidcoin_data, outfile)
		outfile.close()

@bot.event
async def on_voice_state_update(b, a):
	'''
	b - before Member
	a - after Member
	'''

	# Ignore Bot
	if b.id == IDs['ProdBot'] or b.id == IDs['TestBot']:
		return

	# Joining voice channels generates 1 to 10 squidcoin
	if b.voice.voice_channel == None and\
		a.voice.voice_channel != None:
		amount = random.randint(1,10)
		
		if b.id in global_vars.squidcoin_data:
			global_vars.squidcoin_data[b.id] += amount
		else:
			global_vars.squidcoin_data[b.id] = amount
		with open(global_vars.squidcoin_file, 'w') as outfile:
			json.dump(global_vars.squidcoin_data, outfile)
			outfile.close()

	# Check if person left bot's voice channel
	# If last person left, have bot automatically leave
	for v in bot.voice_clients:
		if b.voice.voice_channel == v.channel:
			if len(v.channel.voice_members) == 1:
				await v.disconnect()
			return

@bot.event
async def on_message(msg):
	# Ignore Bot messages
	if msg.author.id == IDs['ProdBot'] or msg.author.id == IDs['TestBot']:
		return

	# When someone makes a messages, they're guaranteed up to .05 squidcoin
	amount = random.randint(1,100)*0.001

	# Output received message to Python console
	line = '{0};;{1}'.format(msg.author, msg.content)
	print('Chat: {0}'.format(line))

	# Log line - Ignore messages from Test Server
	if not msg.channel.is_private and (msg.server.id != IDs['BetaServer'] or msg.server.id != IDs['AlphaServer']):
		f = open('../logs/chat_history.log', 'a')
		f.write('\n{0}'.format(line))
		f.close()

	# Create lowercase version of msg
	m = msg.content.lower()

	#
	# Block of automated reactions based on message text
	#

	for b in m.split():
		if 'bet' == b:
			rx = ['🇧', '🇪', '🇹']
			await reactToMsg(msg, rx)
			amount += random.randint(1,20)*0.01
			break

	if 'brb' in m:
		if msg.author.id == IDs['Jesse'] or msg.author.id == IDs['Eduard']:
			pic_list = os.listdir('../images/jessebrb/')
			if len(pic_list) == 0:
				await bot.send_message(msg.channel, 'No more BRB images!')
			else:
				picture = random.choice(pic_list)
				await bot.send_file(msg.channel, '../images/jessebrb/{0}'.format(picture))
				''' Move picture out of dir '''
				os.rename('../images/jessebrb/{0}'.format(picture),
						'../images/jessebrb_used/{0}'.format(picture))
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
				'../images/HereLiesLeon.png',
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

	#
	# End automated reactions block
	#

	#
	# Add message amount to squidcoin
	#
	if msg.author.id in global_vars.squidcoin_data:
		global_vars.squidcoin_data[msg.author.id] += amount
	else:
		global_vars.squidcoin_data[msg.author.id] = amount
	with open(global_vars.squidcoin_file, 'w') as outfile:
		json.dump(global_vars.squidcoin_data, outfile)
		outfile.close()

	# Process ! commands
	await bot.process_commands(msg)

@bot.event
async def on_ready():
	await bot.change_presence(game=discord.Game(name='Big Brother {0}'.format(global_vars.version)))
	print('-----------------------------------------------------------')
	print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
	print('-----------------------------------------------------------')

bot.loop.create_task(remindme_checker(bot))
bot.loop.create_task(squidcoin_generator(bot))
bot.loop.create_task(squidcoin_voice_scan(bot))
bot.loop.create_task(wednesday_check(bot))
if global_vars.PROD:
	bot.run(Tokens['Prod'])
else:
	bot.run(Tokens['Test'])
