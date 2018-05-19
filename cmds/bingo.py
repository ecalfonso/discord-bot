import aiohttp
import asyncio
import discord
from discord.ext import commands

class Bingo:
	def __init__(self, bot):
		self.bot = bot
		self.counter = 0
		self.entries = []
		self.players = []
		self.setup = 0
		self.started = 0

	@commands.group(pass_context=True,no_pm=True)
	async def bingo(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say("Bingo Help Message Placeholder")

	@bingo.command(pass_context=True, no_pm=True)
	async def create(self, ctx):
		if ctx.message.channel.name != "squidy-bingo":
			await self.bot.say("This command is only for the \"squidy-bingo\" channel")
			return
		''' Check that we're not already building Bingo '''
		if self.setup == 1:
			await self.bot.say("Error: Game setup in progress")
			return
		''' Check that another game isn't going on '''
		if self.started == 1:
			await self.bot.say("Error: Game has already begun")
			return
		''' Check that a bingo.txt was provided '''
		if not ctx.message.attachments:
			await self.bot.say('You need to attach a .txt for me to use')
			return
		''' Get URL for bingo.txt '''
		url = ctx.message.attachments[0]['url']
		if url.split('.')[-1] != 'txt':
			await self.bot.say('Attachment needs to be a .txt file!')
			return
		try:
			''' Try to build self.entries by downloading bingo.txt '''
			async with aiohttp.get(url) as r:
				read_data = await r.read()
				for e in read_data.split(b'\n'):
					self.entries.append(e.decode('utf-8').replace('\r', ''))
			''' Remove duplicate entries '''
			self.entries = list(set(self.entries))
			if len(self.entries) < 25:
				await self.bot.say("Not enough Bingo entries, need at least 25!")
				self.entries = []
				return
			''' We're done setting up, so set setup=1 so people can !bingo ready up'''
			self.setup = 1
			msg = "Bingo is setup! Players use '!bingo ready' to participate.\n\nEntries:\n"
			itr = 1
			for e in self.entries:
				msg += "{0}. {1}\n".format(str(itr).rjust(2), e)
				itr += 1
			msg += "\nUse !bingo start once all players are ready!"
			await self.bot.say(msg)
		except Exception as e:
			await self.bot.say('Error while parsing .txt: {}'.format(e))
			self.entries = []

	@bingo.command(pass_context=True, no_pm=True)
	async def ready(self, ctx):
		if ctx.message.channel.name != "squidy-bingo":
			await self.bot.say("This command is only for the \"squidy-bingo\" channel")
			return
		''' Check that we're in setup, accepting ready requests '''
		if self.setup == 0:
			await self.bot.say("Error: Game isn't setup yet")
			return
		''' Check that another game isn't going on '''
		if self.started == 1:
			await self.bot.say("Error: Game has already begun")
			return
		''' Add person to player list '''
		if not ctx.message.author.id in self.players:
			self.players.append(ctx.message.author.id)
			await self.bot.add_reaction(ctx.message, "☑")
		else:
			await self.bot.say("You are already ready")
		print(self.players)

	@bingo.command(pass_context=True, no_pm=True)
	async def reset(self, ctx):
		if ctx.message.channel.name != "squidy-bingo":
			await self.bot.say("This command is only for the \"squidy-bingo\" channel")
			return
		''' Check that we're in setup '''
		if self.setup == 0:
			await self.bot.say("Error: Game isn't setup yet")
			return
		self.setup = 0
		self.started = 0
		self.entries = []
		self.players = []
		await self.bot.add_reaction(ctx.message, "☑")

	@bingo.command(pass_context=True, no_pm=True)
	async def unready(self, ctx):
		if ctx.message.channel.name != "squidy-bingo":
			await self.bot.say("This command is only for the \"squidy-bingo\" channel")
			return
		''' Check that we're in setup, accepting ready requests '''
		if self.setup == 0:
			await self.bot.say("Error: Game isn't setup yet")
			return
		''' Check that another game isn't going on '''
		if self.started == 1:
			await self.bot.say("Error: Game has already begun")
			return
		''' Remove person from player list '''
		if ctx.message.author.id in self.players:
			self.players.remove(ctx.message.author.id)
			await self.bot.add_reaction(ctx.message, "☑")
		else:
			await self.bot.say("You weren't ready")
		print(self.players)
