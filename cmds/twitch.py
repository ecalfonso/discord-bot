import asyncio
import discord
import global_vars
from discord.ext import commands
from dictionaries.IDs import *

class TwitchLive:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def twitchlive(self, ctx, *, args: str):
		if ctx.message.author.id == IDs['TwitchBot']:
			if args.split(';;;')[0] in twitchIDs:
				name = twitchIDs[args.split(';;;')[0]]
				game = args.split(';;;')[1]
				link = args.split(';;;')[2]

				if global_vars.PROD == 1:
					dest = self.bot.get_channel(IDs['ProdServer'])
				else:
					dest = self.bot.get_channel(IDs['BetaServer'])

				await self.bot.send_message(dest, '<@{0}> started playing {1} on Twitch! <{2}>'.format(
					name,
					game,
					link))
