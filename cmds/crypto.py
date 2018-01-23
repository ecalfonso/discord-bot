import aiohttp
import asyncio
import discord
import json
from discord.ext import commands

class Crypto:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def crypto(self, ctx, args: str):
		url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'

		requested_coin = args.split()[0]

		async with aiohttp.get(url) as response:
			if response.status == 200:
				data = await response.json()
				for coin in data:
					if coin['symbol'].lower() == requested_coin.lower():
						await self.bot.say('{0} is at ${1} USD'.format(coin['name'], coin['price_usd']))
						return
				await self.bot.say('{0} is not a known cryptocurrency symbol'.format(requested_coin.upper()))
			else:
				print('HTTP Error: {0} {1}'.format(response.status, response.text))

	@crypto.error
	async def crypto_err(self, error, ctx):
		await self.bot.say('<@{0}> No Cryptocurrency Symbol entered! Try "!crypto XRB"'.format(ctx.message.author.id))
