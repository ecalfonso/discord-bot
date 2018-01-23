import asyncio
import discord
from discord.ext import commands
from dictionaries.IDs import *

class Unfair:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def unfair(self, ctx):
		await self.bot.say("{0} is unfair\n<@{1}> is in there\nStandin' at the concession\nPlottin' his oppression\n#FreeMe -<@{2}>".format(
			ctx.message.server, 
			IDs['Jesse'], self.bot.user.id))
