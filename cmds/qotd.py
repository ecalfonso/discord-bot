import aiohttp
import asyncio
import discord
import json
from discord.ext import commands

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

