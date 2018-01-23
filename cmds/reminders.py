import asyncio
import discord
from discord.ext import commands

class Timer:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def timer(self, ctx, args: str):
		t = args.split()[0]
		if t.isdigit():
			duration = min(int(t), 180)
			await self.bot.say('{0} minute timer set for <@{1}>'.format(duration, ctx.message.author.id))
			await asyncio.sleep(duration*60)
			await self.bot.say('<@{0}> {1} minute timer is done!'.format(ctx.message.author.id, duration))
		else:
			await self.bot.send_message(ctx.message.channel, 'Incorrect usage. Use a number for time.')
	
	@timer.error
	async def timer_err(self, error, ctx):
		await self.bot.say('Incorrect usage. use "!timer X" ')
