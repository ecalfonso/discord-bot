import asyncio
import discord
from discord.ext import commands
from dictionaries.IDs import IDs

class CarJesse:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def carjesse(self, ctx, args: str):
		await self.bot.send_file(
			ctx.message.channel,
			'../images/CarJesse.png',
			content='Car <@{0}> has arrived! Vroom vroom'.format(IDs['Jesse']),
			tts=((ctx.message.author.id == IDs['Eduard'] or ctx.message.author.id == IDs['Jesse']) and
				'tts' in args.lower())
			)

	@carjesse.error
	async def carjesse_err(self, error, ctx):
		await self.bot.send_file(
			ctx.message.channel,
			'../images/CarJesse.png',
			content='Car <@{0}> has arrived! Vroom vroom'.format(IDs['Jesse']),
			)
