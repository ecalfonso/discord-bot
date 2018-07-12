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

class Misc:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def chris(self, ctx):
		yikes_dir = '../images/yikes/'
		pics = os.listdir(yikes_dir)
		pic = random.choice(pics)
		await self.bot.send_file(
			ctx.message.channel,
			yikes_dir + pic)

	@commands.command(pass_context=True, no_pm=True)
	async def feet(self, ctx):
		feet_dir = '../images/feet/'
		pics = os.listdir(feet_dir)
		pic = random.choice(pics)
		await self.bot.send_file(
			ctx.message.channel,
			feet_dir + pic)

	@commands.command(pass_context=True, no_pm=True)
	async def mean(self, ctx):
		mean_dir = '../images/mean/'
		pics = os.listdir(mean_dir)
		pic = random.choice(pics)
		await self.bot.send_file(
			ctx.message.channel,
			mean_dir + pic)
	
	@commands.command(pass_context=True, no_pm=True)
	async def salt(self, ctx):
		salt_dir = '../images/salt/'
		pics = os.listdir(salt_dir)
		pic = random.choice(pics)
		await self.bot.send_file(
			ctx.message.channel,
			salt_dir + pic)

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

	@commands.command(pass_context=True, no_pm=True)
	async def yikes(self, ctx):
		yikes_dir = '../images/yikes/'
		pics = os.listdir(yikes_dir)
		pic = random.choice(pics)
		await self.bot.send_file(
			ctx.message.channel,
			yikes_dir + pic)
