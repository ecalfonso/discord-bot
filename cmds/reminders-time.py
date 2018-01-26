import asyncio
import discord
import json
import time
from discord.ext import commands
from dictionaries.help_docs import *
from pathlib import Path

remindme_file = '/home/pi/remindme.data'
remindme_data = {}
remindme_itr = 0

days_of_week = {
	'monday': 0,
	'tuesday': 1,
	'wednesday': 2,
	'thursday': 3,
	'friday': 4,
	'saturday': 5,
	'sunday': 6
	}

in_seconds = {
	'hour': 60*60,
	'hours': 60*60,
	'day': 24*60*60,
	'days': 24*60*60,
	'month': 30*24*60*60,
	'months': 30*24*60*60,
	'year': 12*30*24*60*60,
	'years': 12*30*24*60*60
	}

async def remindme_init():
	await bot.wait_until_ready()

	global remindme_file
	global remindme_data
	global remindme_itr

	if Path(remindme_file).is_file():
		remindme_data = json.load(open(remindme_file))
	else:
		print('Remindme.data file not found!')

	remindme_itr = len(remindme_data)

async def remindme_checker():
	global remindme_data

class Timer:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def timer(self, ctx, args: str):
		t = args.split()[0]
		if t.isdigit():
			duration = min(int(t), 180)
			await self.bot.say('{0} minute timer set for <@{1}>'.format(duration, ctx.message.author.id))
			await asyncio.sleep(duration*60)
			await self.bot.say('<@{0}> {1} minute timer is done!'.format(ctx.message.author.id, duration))
		else:
			await self.bot.send_message(ctx.message.channel, 'Incorrect usage. Use a number for time.')
	
	@timer.error
	async def timer_err(self, error, ctx):
		await self.bot.say('Incorrect usage. use "!timer X" ')

class RemindMe:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def remindme(self, ctx, *, args: str):
		global remindme_data
		global remindme_file
		global remindme_itr

		if len(args.split()) < 3:
			await self.bot.say(help_remindme)

		amount = args.split()[0]
		modifier = args.split()[1].lower()

		valid_args = ['hour', 'hours', 'day', 'days', 'month', 'months', 'year', 'years']
		if amount.isdigit() and any(a in modifier for a in valid_args):
			if int(amount) > 300:
				await self.bot.say('Enter a value under 300')
				return

			now = int(time.time())
			then = now + int(amount)*in_seconds[modifier]

			msg = ""
			for p in range(2, len(args.split())):
				msg += '{0} '.format(args.split()[p])
			'''
			await self.bot.say('It is {0}, on {1} I wil remind you: {2}'.format(
				time.ctime(now),
				time.ctime(then),
				msg))
			'''
			remindme_data[now] = [then, ctx.message.author.id, msg]

			with open(remindme_file, 'w') as outfile:
				json.dump(remindme_data, outfile)
				outfile.close()
		
		else:
			await self.bot.say(help_remindme)

	@commands.command(pass_context=True, no_pm=True)
	async def remindmelist(self, ctx):
		global remindme_data
		for r in remindme_data:
			if remindme_data[r][1] == ctx.message.author.id:
				await self.bot.say('On {0} I will remind <@{1}>: {2}'.format(
					time.ctime(remindme_data[r][0]),
					ctx.message.author.id,
					remindme_data[r][2]))
				return
		await self.bot.say('<@{0}> has no scheduled reminders'.format(ctx.message.author.id))
'''
	@remindme.error
	async def remindme_err(self, error, ctx):
		await self.bot.say(help_remindme)
'''
