import asyncio
import discord
import random
from discord.ext import commands

urls = [
'https://www.youtube.com/watch?v=3KquFZYi6L0'
]

class Misc:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True, no_pm=True)
	async def salt(self, ctx):
		await self.bot.say('{0}'.format(random.choice(urls)))	