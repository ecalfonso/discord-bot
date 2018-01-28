import asyncio
import discord
import random
from discord.ext import commands

class EmojiParty:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def emojiparty(self, ctx, args: str):
		msg_id = args.split()[0]

		try:
			m = await self.bot.get_message(ctx.message.channel, msg_id)
		except:
			await self.bot.say('Invalid Message ID')
			return

		emojis = ctx.message.server.emojis
		emoji_count = min(len(emojis), 20)

		random_emoji = random.sample(emojis, emoji_count)

		for e in random_emoji:
			await self.bot.add_reaction(m, '{0}:{1}'.format(e.name, e.id))

		await self.bot.delete(ctx.message)


	@emojiparty.error
	async def emojiparty_err(self, error, ctx):
		await self.bot.say('Invalid Message ID')
