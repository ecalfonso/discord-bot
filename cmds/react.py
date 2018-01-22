import asyncio
import discord
from discord.ext import commands
from dictionaries.help_docs import *

async def errMsg(self, ctx):
	await self.bot.say('Invalid Message ID')

async def getMsg(self, ctx, msg):
	try:
		return await self.bot.get_message(ctx.message.channel, msg)
	except:
		return None

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
		msg = await getMsg(self, ctx, args.split()[0])

		if msg != None:
			await self.bot.add_reaction(msg, 'boi:398682539155390465')
		else:
			await errMsg(self, ctx)
		
	@react.command(pass_context=True, no_pm=True)
	async def nsfl(self, ctx, args: str):
		''' N S F L '''
		msg = await getMsg(self, ctx, args.split()[0])

		if msg != None:
			await self.bot.add_reaction(msg, '🇳')
			await self.bot.add_reaction(msg, '🇸')
			await self.bot.add_reaction(msg, '🇫')
			await self.bot.add_reaction(msg, '🇱')
		else:
			await self.bot.say('Not a good msg id')

	@react.command(pass_context=True, no_pm=True)
	async def nsfw(self, ctx, args: str):
		''' N S F W '''
		msg = await getMsg(self, ctx, args.split()[0])

		if msg != None:
			await self.bot.add_reaction(msg, '🇳')
			await self.bot.add_reaction(msg, '🇸')
			await self.bot.add_reaction(msg, '🇫')
			await self.bot.add_reaction(msg, '🇼')
		else:
			await errMsg(self, ctx)

	@react.command(pass_context=True, no_pm=True)
	async def waiting(self, ctx, args: str):
		msg = await getMsg(self, ctx, args.split()[0])

		if msg != None:
			await self.bot.add_reaction(msg, 'waiting:398718247295516672')
		else:
			await errMsg(self, ctx)
