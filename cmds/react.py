import asyncio
import discord
from discord.ext import commands
from dictionaries.help_docs import *

async def processMsg(self, ctx, msg, reactions):
	try:
		m = await self.bot.get_message(ctx.message.channel, msg)
		for r in reactions:
			await self.bot.add_reaction(m, r)
	except:
		await self.bot.say('Invalid Message ID')

class React:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def react(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say(help_react)
		await self.bot.delete_message(ctx.message)

	@react.command(pass_context=True, no_pm=True)
	async def showme(self, ctx):
		''' Internal debug command
			Displays all server's names and ids
		'''
		for e in ctx.message.server.emojis:
			print('{0} : {1}'.format(e.name, e.id))

	@react.command(pass_context=True, no_pm=True)
	async def boi(self, ctx, args: str):
		''' Chopping hand emote '''
		rx = ['boi:398682539155390465']
		await processMsg(self, ctx, args.split()[0], rx)
		
	@react.command(pass_context=True, no_pm=True)
	async def chad(self, ctx, args: str):
		''' chad_boi '''
		rx = ['chad_boi:499386940722774016']
		await processMsg(self, ctx, args.split()[0], rx)


	@react.command(pass_context=True, no_pm=True)
	async def deletethis(self, ctx, args: str):
		''' D E L E T E T H I S '''
		rx = ['delete_this:417889336210620416']
		await processMsg(self, ctx, args.split()[0], rx)

	@react.command(pass_context=True, no_pm=True)
	async def nsfl(self, ctx, args: str):
		''' N S F L '''
		rx = ['🇳', '🇸', '🇫', '🇱']
		await processMsg(self, ctx, args.split()[0], rx)

	@react.command(pass_context=True, no_pm=True)
	async def nsfw(self, ctx, args: str):
		''' N S F W '''
		rx = ['🇳', '🇸', '🇫', '🇼']
		await processMsg(self, ctx, args.split()[0], rx)

	@react.command(pass_context=True, no_pm=True)
	async def waiting(self, ctx, args: str):
		rx = ['waiting:398718247295516672']
		await processMsg(self, ctx, args.split()[0], rx)
