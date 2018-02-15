import aiohttp
import asyncio
import discord
import json
import random
import re
from discord.ext import commands
from pathlib import Path
from dictionaries.help_docs import *

quotes_file = '../quotes.data'
quotes_data = {}

quote_beginnings = [
'announced',
'has said',
'is famous for saying',
'once said',
'mentioned',
'is known for saying'
]

async def quotes_init(bot):
	await bot.wait_until_ready()

	global quotes_file
	global quotes_data

	if Path(quotes_file).is_file():
		quotes_data = json.load(open(quotes_file))
	else:
		print('Quotes.data file not found!')

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
	async def random(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		if person_id in quotes_data:
			await self.bot.say('<@{0}> {1}: {2}'.format(
				person_id,
				random.choice(quote_beginnings),
				random.choice(quotes_data[person_id])))
		else:
			await self.bot.say('No saved quotes for <@{0}>!'.format(person_id))

	@quote.command(pass_context=True, no_pm=True)
	async def show(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
		except AttributeError:
			tmp = await self.bot.say('First argument needs to be a server member')
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return

		if person_id in quotes_data:
			msg = ""
			itr = 1
			for q in quotes_data[person_id]:
				msg += '{0}. {1}\n'.format(itr, q)
				itr += 1

			await self.bot.say('<@{0}> {1}:\n{2}'.format(
				person_id,
				random.choice(quote_beginnings),
				msg))
		else:
			await self.bot.say('No saved quotes for <@{0}>!'.format(person_id))

	@quote.command(pass_context=True, no_pm=True)
	async def save(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
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

		''' Check to see if this user already exists in the db 
			Then add the quote to the db
		'''
		if person_id in quotes_data:
			quotes_data[person_id].append(msg)
		else:
			quotes_data[person_id] = [msg]

		with open(quotes_file, 'w') as outfile:
			json.dump(quotes_data, outfile)
			outfile.close()

		await self.bot.add_reaction(ctx.message, '☑')

	@quote.command(pass_context=True, no_pm=True)
	async def remove(self, ctx, *, args: str):
		try:
			person_id = re.search('<@(.+?)>|<@!(.+?)>', args.split()[0]).group(1)
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

		if int(number_to_remove) > len(quotes_data[person_id]):
			tmp = await self.bot.say('Value needs to be a number between 1 and {0}.'.format(len(quotes_data[person_id])))
			await asyncio.sleep(10)
			await self.bot.delete_message(tmp)
			await self.bot.delete_message(ctx.message)
			return
	
		if person_id in quotes_data:
			quotes_data[person_id].remove(quotes_data[person_id][int(number_to_remove)-1])

			with open(quotes_file, 'w') as outfile:
				json.dump(quotes_data, outfile)
				outfile.close()
			await self.bot.add_reaction(ctx.message, '☑')
		else:
			await self.bot.say('No saved quotes for <@{0}>!'.format(person_id))