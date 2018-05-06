import asyncio
import discord
import global_vars
import os
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

	@commands.command(pass_context=True, no_pm=True)
	async def spoilers(self, ctx):
		role = discord.utils.get(ctx.message.server.roles, name='Spoilerinos')
		try:
			await self.bot.add_roles(ctx.message.author, role)
			await self.bot.add_reaction(ctx.message, '☑')
		except:
			print('Unable to give role')

	@commands.command(pass_context=True, no_pm=True)
	async def nospoilers(self, ctx):
		role = discord.utils.get(ctx.message.server.roles, name='Spoilerinos')
		try:
			await self.bot.remove_roles(ctx.message.author, role)
			await self.bot.add_reaction(ctx.message, '☑')
		except:
			print('Unable to give role')

	@commands.command(pass_context=True, no_pm=True)
	async def ugly(self, ctx):
		pic_dir = '../images/ugly/'
		pics = os.listdir(pic_dir)
		pic = random.choice(pics)
		await self.bot.send_file(
			ctx.message.channel,
			pic_dir + pic,
			content="I'm ugly and I'm proud!"
		)
