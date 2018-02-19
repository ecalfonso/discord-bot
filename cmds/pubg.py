import asyncio
import discord
import random
from discord.ext import commands
from dictionaries.help_docs import *
from dictionaries.pubg_lists import *

class Pubg:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def pubg(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say(help_pubg)

	@pubg.command(pass_context=True, no_pm=True)
	async def map1(self, ctx):
		hot_items = {'High': 60, 'Mid-high': 25, 'Mid-low':12, 'Low': 3}
		hotness = random.choice([k for k in hot_items for dummy in range(hot_items[k])])
		drop = random.sample(erangel_locs[hotness], 1)[0]
		await self.bot.say('Drop: {0}'.format(str(drop)))

	@pubg.command(pass_context=True, no_pm=True)
	async def map2(self, ctx):
		hot_items = {'High': 75, 'Mid': 22, 'Low': 3}
		hotness = random.choice([k for k in hot_items for dummy in range(hot_items[k])])
		drop = random.sample(miramar_locs[hotness], 1)[0]
		await self.bot.say('Drop: {0}'.format(str(drop)))

	@pubg.command(pass_context=True, no_pm=True)
	async def rpg(self, ctx, *, args):
		classes = ['DPS', 'Healer', 'Tank', 'Hunter']
		msg = ""

		for p in args.split():
			if p.startswith('<@'):
				c = random.choice(classes)
				classes.remove(c)
				msg += '{0} is {1}\n'.format(
						p,
						c)
		await self.bot.say(msg)
