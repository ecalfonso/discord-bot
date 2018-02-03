import asyncio
import discord
import global_vars
import json
import operator
import re
import random
from dictionaries.help_docs import *
from dictionaries.IDs import IDs
from discord.ext import commands
from pathlib import Path

async def squidcoin_init(bot):
	await bot.wait_until_ready()

	if Path(global_vars.squidcoin_file).is_file():
		global_vars.squidcoin_data = json.load(open(global_vars.squidcoin_file))
	else:
		print('Squidcoinbase file not found!')

async def squidcoin_generator(bot):
	await bot.wait_until_ready()

	while(1):
		''' Make coins available after a random interval between 1 and 15 minutes
		'''
		mins = random.randint(1,15)
		await asyncio.sleep(60*mins)
		await bot.change_presence(
			game=discord.Game(name='Big Brother {0}'.format(global_vars.version)),
			status=discord.Status('online'))
		global_vars.squidcoin_ready = 1

async def squidcoin_voice_scan(bot):
	''' Scan Squidsquad voice channels hourly
		Reward active users 2-5 Squidcoin
	'''
	await bot.wait_until_ready()
	await asyncio.sleep(15)

	server = bot.get_server(IDs['Squid Squad Server'])

	if server == None:
		print('Unable to access Squid Squad server for squidcoin_voice_scan(bot)')
		return

	while(1):
		for channel in server.channels:
			for m in channel.voice_members:
				amount = random.randint(3,5)
	
				if m.id in global_vars.squidcoin_data:
					global_vars.squidcoin_data[m.id] += amount
				else:
					global_vars.squidcoin_data[m.id] = amount
				with open(global_vars.squidcoin_file, 'w') as outfile:
					json.dump(global_vars.squidcoin_data, outfile)
					outfile.close()
		await asyncio.sleep(60*60)

class SquidCoin:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def squidcoin(self, ctx):
		if ctx.invoked_subcommand is None:
			msg = await self.bot.say(help_squidcoin)
			await asyncio.sleep(30)
			await self.bot.delete_message(msg)
			await self.bot.delete_message(ctx.message)

	@squidcoin.command(pass_context=True, no_pm=True)
	async def getcoin(self, ctx):
		if global_vars.squidcoin_ready == 1:
			''' Reset squidcoin_ready '''
			await self.bot.change_presence(
				game=discord.Game(name='Big Brother {0}'.format(global_vars.version)),
				status=discord.Status('idle'))
			global_vars.squidcoin_ready = 0

			''' Calcualte squidcoin amount '''
			coin_probability = [0] * 5 + [1] * 85 + [2] * 9 + [3] * 1
			amount = random.choice(coin_probability)

			''' Add amount to wallet'''
			await self.bot.say('<@{0}> claimed {1} squidcoin!'.format(
				ctx.message.author.id,
				amount))
			if ctx.message.author.id in global_vars.squidcoin_data:
				global_vars.squidcoin_data[ctx.message.author.id] += amount
			else:
				global_vars.squidcoin_data[ctx.message.author.id] = amount 
			with open(global_vars.squidcoin_file, 'w') as outfile:
				json.dump(global_vars.squidcoin_data, outfile)
				outfile.close()
		else:
			msg = await self.bot.say('Coin not available yet')
			await asyncio.sleep(10)
			await self.bot.delete_message(msg)
			await self.bot.delete_message(ctx.message)

	@squidcoin.command(pass_context=True, no_pm=True)
	async def ranking(self, ctx):
		ranks = sorted(global_vars.squidcoin_data.items(), key=operator.itemgetter(1), reverse=True)

		rank_msg = 'Squidcoin rankings:\n'
		for r in ranks:
			try:
				user = await self.bot.get_user_info(r[0])
			except:
				continue
			rank_msg += '{0} : {1}\n'.format(user.name, r[1])
		tmp = await self.bot.send_message(ctx.message.channel, rank_msg)
		await asyncio.sleep(30)
		await self.bot.delete_message(tmp)
		await self.bot.delete_message(ctx.message)

	@squidcoin.command(pass_context=True, no_pm=True)
	async def tip(self, ctx, *, args: str):
		# Try to extract the recipient's ID
		try:
			person_id = re.search('<@!(.+?)>', args.split()[0]).group(1)
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return
																		
		# Make sure person doesn't tip themselves
		if person_id == ctx.message.author.id:
			tmp = await self.bot.say('You cannot tip yourself <@{0}>'.format(person_id))
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		# Search if member is in the server
		found = 0
		for m in ctx.message.server.members:
			if m.id == person_id:
				found = 1
				break
		if found == 0:
			tmp = await self.bot.say('That person does not exist in the server')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		amount = args.split()[1]

		# Check that amount was vaid number
		if not amount.isdigit():
			tmp = await self.bot.say('Enter a number amount <@{0}>'.format(ctx.message.author.id))
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		# Check if member has that much
		if int(amount) > global_vars.squidcoin_data[ctx.message.author.id]:
			tmp = await self.bot.say('<@{0}> do not have {1} to tip'.format(ctx.message.author.id, amount))
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		# deduct amount from member in squidcoinbase
		global_vars.squidcoin_data[ctx.message.author.id] -= int(amount)
		global_vars.squidcoin_data[person_id] += int(amount)

		with open(global_vars.squidcoin_file, 'w') as outfile:
			json.dump(global_vars.squidcoin_data, outfile)
			outfile.close()

		await self.bot.say('<@{0}> tips {1} to <@{2}>'.format(
			ctx.message.author.id,
			amount,
			person_id))

	@squidcoin.command(pass_context=True, no_pm=True)
	async def wallet(self, ctx):
		if ctx.message.author.id in global_vars.squidcoin_data:
			msg = await self.bot.say('<@{0}> has {1} squidcoin!'.format(
				ctx.message.author.id, 
				global_vars.squidcoin_data[ctx.message.author.id]))
		else:
			msg = await self.bot.say('<@{0}> has no squidcoin.'.format(ctx.message.author.id))
		await asyncio.sleep(10)
		await self.bot.delete_message(msg)
		await self.bot.delete_message(ctx.message)
