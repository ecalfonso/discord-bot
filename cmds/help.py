import asyncio
import discord
from discord.ext import commands
from dictionaries.help_docs import *

class Help:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def help(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say(help_default)
		await self.bot.delete_message(ctx.message)

	@help.command(pass_context=True, no_pm=True)
	async def auto(self, ctx):
		await self.bot.say(help_auto)

	@help.command(pass_context=True, no_pm=True)
	async def cmds(self, ctx):
		await self.bot.say(help_commands)

	@help.command(pass_context=True, no_pm=True)
	async def music(self, ctx):
		await self.bot.say(help_music)

	@help.command(pass_context=True, no_pm=True)
	async def pubg(self, ctx):
		await self.bot.say(help_pubg)
	
	@help.command(pass_context=True, no_pm=True)
	async def react(self, ctx):
		await self.bot.say(help_react)

	@help.command(pass_context=True, no_pm=True)
	async def quote(self, ctx):
		await self.bot.say(help_quote)

	@help.command(pass_context=True, no_pm=True)
	async def remindme(self, ctx):
		await self.bot.say(help_remindme)
	
	@help.command(pass_context=True, no_pm=True)
	async def squidcoin(self, ctx):
		await self.bot.say(help_squidcoin)
