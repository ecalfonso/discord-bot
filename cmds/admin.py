import asyncio
import discord
from discord.ext import commands
from dictionaries.IDs import IDs
from dictionaries.help_docs import *

def is_admin(u):
	if u == IDs['Eduard'] or\
	u == IDs['Jesse'] or\
	u == IDs['Nick'] or\
	u == IDs['Justin'] or\
	u == IDs['Jeremy']:
		return True
	else:
		return False
	

class Admin:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def cleanup(self, ctx):
		def is_me(m):
			return m.author == self.bot.user

		def is_cmd(m):
			return m.content.startswith('!')

		del_cmd_msgs = await self.bot.purge_from(
			ctx.message.channel,
			limit=50,
			check=is_cmd)

		del_bot_msgs = await self.bot.purge_from(
			ctx.message.channel,
			limit=50,
			check=is_me)

		await self.bot.say('Deleted {0} User commands and {1} Bot messages.'.format(
			len(del_cmd_msgs), len(del_bot_msgs)))

	@commands.command(pass_context=True, no_pm=True)
	async def topic(self, ctx, *, args: str):
		if is_admin(ctx.message.author.id):
			if len(args.split()) == 1 and args.lower() == 'clear':
				await self.bot.edit_channel(
					ctx.message.channel,
					topic='')
			else:
				await self.bot.edit_channel(
                                        ctx.message.channel,
                                        topic=args)
		else:
			await self.bot.say('You are not an admin')

	@topic.error
	async def topic_err(self, ctx, error):
		await self.bot.say(help_topic)
