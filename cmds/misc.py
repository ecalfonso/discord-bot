import aiohttp
import asyncio
import discord
import global_vars
import json
import os
import random
import re
from datetime import datetime
from dictionaries.IDs import *
from discord.ext import commands
from pathlib import Path

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

async def monday_check(bot):
	await bot.wait_until_ready()

	while(1):
		await asyncio.sleep(60*60) # Poll every 60m

		# get current day in YYYY-MM-DD
		today = '{0.year}-{0.month:02d}-{0.day:02d}'.format(datetime.today())

		# get punday data
		url = 'https://mondaypunday.com/wp-json/wp/v2/posts'
		async with aiohttp.get(url) as resp:
			data = await resp.json()
			html = data[0]['content']['rendered']

		# If it's monday, and a new image is posted
		if today in data[0]['date']:
			# Check that we didn't already post
			img_dir = '../images/monday/'
			img_name = img_dir + today + '.jpg'
			if not Path(img_name).is_file():
				# Extract url
				img_url = re.findall('\ssrc="([^"]+)"', html)[0]

				# Set destination
				if global_vars.PROD == 1:
					dest = bot.get_channel(IDs['ProdServer'])
				else:
					dest = bot.get_channel(IDs['BetaServerGeneral'])

				# Create img file to denote we already posted
				async with aiohttp.get(img_url) as response:
					data = await response.read()
					with open(img_name, 'wb') as outfile:
						outfile.write(data)
						outfile.close()

				# Post img url
				await bot.send_message(
					dest,
					'Monday Punday for {0}!\n {1}'.format(today, img_url)
				)

async def postPics(bot, ctx, dir_name):
	# Check dir_name exists
	if os.path.isdir(dir_name):
		pics = os.listdir(dir_name)
		pic = random.choice(pics)
		await bot.send_file(ctx.message.channel, dir_name + pic)
	else:
		print(dir_name, " doesn't exist!")

class Misc:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def chris(self, ctx):
		await postPics(self.bot, ctx, '../images/yikes/')

	@commands.command(pass_context=True, no_pm=True)
	async def cough(self, ctx):
		await postPics(self.bot, ctx, '../images/cough/')

	@commands.command(pass_context=True, no_pm=True)
	async def cute(self, ctx):
		await postPics(self.bot, ctx, '../images/cute/')

	@commands.command(pass_context=True, no_pm=True)
	async def feet(self, ctx):
		await postPics(self.bot, ctx, '../images/feet/')

	@commands.command(pass_context=True, no_pm=True)
	async def here(self, ctx):
		await postPics(self.bot, ctx, '../images/ww@/')

	@commands.command(pass_context=True, no_pm=True)
	async def mean(self, ctx):
		await postPics(self.bot, ctx, '../images/mean/')
	
	@commands.command(pass_context=True, no_pm=True)
	async def salt(self, ctx):
		await postPics(self.bot, ctx, '../images/salt/')

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
		await postPics(self.bot, ctx, '../images/ugly/')

	@commands.command(pass_context=True, no_pm=True)
	async def yikes(self, ctx):
		await postPics(self.bot, ctx, '../images/yikes/')
