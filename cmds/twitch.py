import asyncio
import discord
from discord.ext import commands
from dictionaries.IDs import *

class TwitchLive:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def twitchlive(self, ctx, *, args: str):
		if ctx.message.author.id == IDs['TwitchHookBot']:
			if args.split(';;;')[0] in twitchIDs:
				name = twitchIDs[args.split(';;;')[0]]
				game = args.split(';;;')[1]
				link = args.split(';;;')[2]
				await self.bot.send_message(self.bot.get_channel(IDs['Squid Squad General Channel']), '<@{0}> started playing {1} on Twitch! <{2}>'.format(
					name,
					game,
					link))
