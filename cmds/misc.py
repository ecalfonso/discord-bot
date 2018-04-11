import asyncio
import discord
import global_vars
import random
from datetime import datetime
from dictionaries.IDs import *
from discord.ext import commands

async def wednesday_check(bot):
	await bot.wait_until_ready()

	while(1):
		await asyncio.sleep(60*15) # Poll every 15m

		if datetime.today().weekday() == 2:
			if datetime.today().hour == 0 and datetime.today().minute < 16:
				if global_vars.PROD == 1:
					dest = bot.get_channel(IDs['ProdServer'])
				else:
					dest = bot.get_channel(IDs['BetaServerGeneral'])

				await bot.send_file(
					dest,
					'../images/wednesday/w1.jpg'
				)

class Misc:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True, no_pm=True)
	async def salt(self, ctx):
		urls = [
			'https://www.youtube.com/watch?v=3KquFZYi6L0'
		]
		await self.bot.say('{0}'.format(random.choice(urls)))	
