import aiohttp
import asyncio
import datetime
import discord
import global_vars
import json
import operator
import random
import re
from discord.ext import commands
from pathlib import Path
from dictionaries.help_docs import *

quote_beginnings = [
'announced',
'has said',
'is famous for saying',
'once said',
'mentioned',
'is known for saying'
]

class Qotd:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def qotd(self, ctx):
		url = 'http://quotes.rest/qod.json'

		async with aiohttp.get(url) as response:
			if response.status == 200:
				data = await response.json()
				await self.bot.say('''```asciidoc\nQuote of the Day for {0}\n\n"{1}"\n\n-{2}```'''.format(
					data['contents']['quotes'][0]['date'],
					data['contents']['quotes'][0]['quote'],
					data['contents']['quotes'][0]['author']))
			else:
				print('QOTD GET failed with error: {0}'.format(response.status))
				await self.bot.say('QOTD Request failed!')

class Quote:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def quote(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say(help_quote)

	@quote.command(pass_context=True, no_pm=True)
	async def leaderboard(self, ctx):
		l = {}
		for p in global_vars.quotes_data:
			l[p] = len(global_vars.quotes_data[p])

		l = sorted(l.items(), key=operator.itemgetter(1), reverse=True)
		msg = 'Quote leaderboard:\n'

		itr = 1
		for p in l:
			try:
				await self.bot.send_typing(ctx.message.channel)
				user = await self.bot.get_user_info(p[0])
			except:
				continue

			msg += '{0}. {1} with {2}\n'.format(itr, user.display_name, p[1])

			itr += 1

		await self.bot.send_message(ctx.message.channel, msg)

	@quote.command(pass_context=True, no_pm=True)
	async def random(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
			
			if person_id.startswith('!'):
				person_id = person_id[1:]
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		if person_id in global_vars.quotes_data:
			await self.bot.say('<@{0}> {1}: {2}'.format(
				person_id,
				random.choice(quote_beginnings),
				random.choice(global_vars.quotes_data[person_id])))
		else:
			await self.bot.say('No saved quotes for <@{0}>!'.format(person_id))

	@quote.command(pass_context=True, no_pm=True)
	async def remove(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
			if person_id.startswith('!'):
				person_id = person_id[1:]
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		number_to_remove = args.split()[1]
		if not number_to_remove.isdigit():
			tmp = await self.bot.say('Argument needs to be a Number. Use !quote show @person to get Numbers')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		if int(number_to_remove) > len(global_vars.quotes_data[person_id]):
			tmp = await self.bot.say('Value needs to be a number between 1 and {0}.'.format(len(global_vars.quotes_data[person_id])))
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		if person_id in global_vars.quotes_data:
			global_vars.quotes_data[person_id].remove(global_vars.quotes_data[person_id][int(number_to_remove)-1])

			with open(global_vars.quotes_file, 'w') as outfile:
				json.dump(global_vars.quotes_data, outfile)
				outfile.close()
			await self.bot.add_reaction(ctx.message, '☑')
		else:
			await self.bot.say('No saved quotes for <@{0}>!'.format(person_id))

	@quote.command(pass_context=True, no_pm=True)
	async def save(self, ctx, *, args: str):
		if len(args.split()) == 1:
			tmp = await self.bot.say('No quote was entered.')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)

			if person_id.startswith('!'):
				person_id = person_id[1:]
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return
		
		''' Construct Quote in var msg '''
		msg = ""
		for m in range(1, len(args.split())):
			msg += '{0} '.format(args.split()[m])

		''' Generate timestamp '''
		now = datetime.datetime.today()

		msg += 'at {0}:{1} {2}/{3}/{4}'.format(
				now.hour%12,
				now.minute,
				now.month,
				now.day,
				now.year)

		''' Check to see if this user already exists in the db 
			Then add the quote to the db
		'''
		if person_id in global_vars.quotes_data:
			global_vars.quotes_data[person_id].append(msg)
		else:
			global_vars.quotes_data[person_id] = [msg]

		with open(global_vars.quotes_file, 'w') as outfile:
			json.dump(global_vars.quotes_data, outfile)
			outfile.close()

		await self.bot.add_reaction(ctx.message, '☑')

	@quote.command(pass_context=True, no_pm=True)
	async def show(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
			if person_id.startswith('!'):
				person_id = person_id[1:]
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		if person_id in global_vars.quotes_data:
			itr = 1

			# Extract specified quote #
			if len(args.split()) == 2:
				num_to_get = args.split()[1]
				if not num_to_get.isdigit():
					tmp = await self.bot.say('Enter a valid number to get an exact quote.')
					await asyncio.sleep(10)
					await self.bot.delete_message(tmp)
					await self.bot.delete_message(ctx.message)
					return

				if int(num_to_get) > len(global_vars.quotes_data[person_id]):
					tmp = await self.bot.say('Value needs to be a number between 1 and {0}.'.format(len(global_vars.quotes_data[person_id])))
					await asyncio.sleep(10)
					await self.bot.delete_message(tmp)
					await self.bot.delete_message(ctx.message)
					return

				msg = '<@{0}> {1}: {2}'.format(
						person_id,
						random.choice(quote_beginnings),
						global_vars.quotes_data[person_id][int(num_to_get)-1])

			# Build message from entire quote list
			else:
				msg = '<@{0}> {1}:\n'.format(person_id, random.choice(quote_beginnings))
				for q in global_vars.quotes_data[person_id]:
					msg += '{0}. {1}\n'.format(itr, q)
					itr += 1

					# Dump message once 10 quotes reached, due to Discord's 2000 char limit
					if itr % 10 == 0:
						await self.bot.say('{0}'.format(msg))
						msg = ''

			await self.bot.say('{0}'.format(msg))
		else:
			await self.bot.say('No saved quotes for <@{0}>!'.format(person_id))
