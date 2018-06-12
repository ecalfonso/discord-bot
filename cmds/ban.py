import discord
from discord.ext import commands

class Ban:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def ban(self, ctx):
		if ctx.invoked_subcommand is None:
			print('banlist')

	@ban.command(pass_context=True, no_pm=True)
	async def remove(self, ctx, *, args: str):
		print('remove')

	@ban.command(pass_context=True, no_pm=True)
	async def save(self, ctx, *, args: str):
		print('save')

	@ban.command(pass_context=True, no_pm=True)
	async def show(self, ctx, *, args: str):
		print('show')
