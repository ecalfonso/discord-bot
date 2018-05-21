import asyncio
import discord
import global_vars
import json
from discord.ext import commands
from dictionaries.IDs import IDs
from dictionaries.help_docs import *
from pathlib import Path

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

	@commands.group(pass_context=True, no_pm=True)
	async def showme(self, ctx):


		if ctx.invoked_subcommand is None:
			await self.bot.say('roles, ')

	@showme.command(pass_context=True, no_pm=True)
	async def roles(self, ctx):
		if global_vars.PROD == 1:
			server = self.bot.get_server(IDs['ProdServer'])
		else:
			server = self.bot.get_server(IDs['BetaServer'])
		msg = ""
		for r in server.roles:
			msg += "{0.position} {0.name}\n".format(r)
		await self.bot.say(msg)

	@commands.command(pass_context=True, no_pm=True)
	async def topic(self, ctx, *, args: str):
		if ctx.message.author.top_role.permissions.manage_channels == True:
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

	@commands.command(pass_context=True, no_pm=True)
	async def nicknameFetch(self, ctx):
		if not is_admin(ctx.message.author.id):
			await self.bot.say('You are not an admin')
			return

		''' Get Server members '''
		if global_vars.PROD == 1:
			server = self.bot.get_server(IDs['ProdServer'])
		else:
			server = self.bot.get_server(IDs['BetaServer'])

		''' Load db '''		
		if Path(global_vars.nicknames_file).is_file():
			nicknames_data = json.load(open(global_vars.nicknames_file))

		''' Add new nickname data '''
		for m in server.members:
			if m.nick != None:
				if m.id in nicknames_data:
					if not m.nick in nicknames_data[m.id]:
						nicknames_data[m.id].append(m.nick)
				else:
					nicknames_data[m.id] = [m.nick]

		''' Writeback db '''
		with open(global_vars.nicknames_file, 'w') as outfile:
			json.dump(nicknames_data, outfile)
			outfile.close()
