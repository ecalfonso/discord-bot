import asyncio
import discord
import random
from discord.ext import commands
from dictionaries.lists import *

class Decision:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def conch(self, ctx):
		await self.bot.say(
			'Conch: {0}'.format(
				random.choice([k for k in conch_items for dummy in range(conch_items[k])])
			)
		)

	@commands.command(pass_context=True, no_pm=True)
	async def magic8(self, ctx):
		await self.bot.say('Magic 8-ball says: {0}'.format(random.sample(magic_8ball_items, 1)[0]))

	@commands.command(pass_context=True, no_pm=True)
	async def shuffle(self, ctx, *, args: str):
		num = 1
		l = args.split()
		if args.split()[0].isdigit():
			num = l[0]
			if int(num) > len(l):
				await self.bot.say('Choice must be below {}'.format(len(l)-1))
			l.pop(0)
		msg = 'Here are your {} choices: '.format(num)
		for x in random.sample(l, int(num)):
			msg += ' {}'.format(x)
		await self.bot.say(msg)

	@commands.command(pass_context=True, no_pm=True)
	async def yesno(self, ctx):
		await self.bot.say(random.choice([k for k in yesno_items for dummy in range(yesno_items[k])]))
