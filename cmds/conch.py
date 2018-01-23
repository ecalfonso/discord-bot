import asyncio
import discord
import random
from discord.ext import commands
from dictionaries.lists import *

class Conch:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def conch(self, ctx):
		await self.bot.say(
			'Conch: {0}'.format(
				random.choice([k for k in conch_items for dummy in range(conch_items[k])])
			)
		)
