import asyncio
import datetime
import discord
import global_vars
import json
from discord.ext import commands
from dictionaries.help_docs import *
from pathlib import Path

async def remindme_checker(bot):
	await bot.wait_until_ready()
	await asyncio.sleep(7)

	while(True):
		now = int(datetime.datetime.utcnow().timestamp())
		to_del = []

		''' Run through remindme database and see which ones need to be sent '''
		for r in global_vars.remindme_data:
			if global_vars.remindme_data[r][0] < now:
				await bot.send_message(await bot.get_user_info(global_vars.remindme_data[r][1]),
					'Reminder from {0}: {1}'.format(
						datetime.datetime.utcfromtimestamp(int(r)),
						global_vars.remindme_data[r][2]))
				to_del.append(r)

		''' Delete messages that were sent out '''
		for d in to_del:
			del global_vars.remindme_data[d]

		''' Writeback to database file '''
		with open(global_vars.remindme_file, 'w') as outfile:
			json.dump(global_vars.remindme_data, outfile)
			outfile.close()

		await asyncio.sleep(120)

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

	@commands.group(pass_context=True, no_pm=True)
	async def remindme(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say(help_remindme)

	@remindme.command(pass_context=True, no_pm=True)
	async def after(self, ctx, *, args: str):
		if len(args.split()) < 3:
			await self.bot.say(help_remindme)
			return

		amount = args.split()[0]
		modifier = args.split()[1].lower()

		if not amount.isdigit():
			await self.bot.say('Invalid amount')
		else:
			amount = int(amount)

		mins_amount = 0
		hours_amount = 0
		days_amount = 0
		weeks_amount = 0

		if modifier == 'minute' or modifier == 'minutes':
			mins_amount = amount
		elif modifier == 'hour' or modifier == 'hours':
			hours_amount = amount
		elif modifier == 'day' or modifier == 'days':
			days_amount = amount
		elif modifier == 'week' or modifier == 'weeks':
			weeks_amount = amount
		elif modifier == 'month' or modifier == 'months':
			weeks_amount = amount * 4
		elif modifier == 'year' or modifier == 'years':
			if amount > 2:
				await self.bot.say('I only support up to 2 years')
				return
			weeks_amount = amount * 52
		else:
			await self.bot.say('Invalid modifier (minutes|hours|days|weeks|months|years)')
			return

		msg = ""
		for p in range(2, len(args.split())):
			msg += '{0} '.format(args.split()[p])

		now = datetime.datetime.utcnow()
		end = now + datetime.timedelta(
			minutes=mins_amount,
			hours=hours_amount,
			days=days_amount,
			weeks=weeks_amount)
		
		global_vars.remindme_data[int(now.timestamp())] = [
			int(end.timestamp()),
			 ctx.message.author.id,
			 msg]

		with open(global_vars.remindme_file, 'w') as outfile:
			json.dump(global_vars.remindme_data, outfile)
			outfile.close()

		await self.bot.add_reaction(ctx.message, '☑')

	@remindme.command(pass_context=True, no_pm=True)
	async def showme(self, ctx):
		''' Run through remindme database and see which ones need to be sent '''
		for r in global_vars.remindme_data:
			if global_vars.remindme_data[r][1] == ctx.message.author.id:
				await self.bot.send_message(await self.bot.get_user_info(global_vars.remindme_data[r][1]),
					'I will remind you at {0}: {1}'.format(
					datetime.datetime.utcfromtimestamp(global_vars.remindme_data[r][0]),
					global_vars.remindme_data[r][2]))

