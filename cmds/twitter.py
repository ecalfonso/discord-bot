import asyncio
import discord
import global_vars
import os
import random
from discord.ext import commands
from dictionaries.IDs import *

dev_names = [
'PUBG Tech Support',
'PUBG Lemurs',
'Lemur Squad',
'Lead Lemur Dev'
]

class Twitter:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def readtweet(self, ctx, *, args: str):
		if ctx.message.author.id == IDs['TwitterBot']:
			name = args.split(';;;')[0]
			tweet = args.split(';;;')[1]
			link = args.split(';;;')[2]

			''' Skip if @ because it's a mention not a tweet '''
			if tweet.startswith('@'):
				return

			''' Skip if non-maintenance tweet '''
			if 'maintenance' not in tweet.lower():
				return

			if global_vars.PROD == 1:
				dest = self.bot.get_channel(IDs['ProdServer'])
			else:
				dest = self.bot.get_channel(IDs['BetaServerGeneral'])

			''' Get random lemur image '''
			pic_list = os.listdir('../images/lemurs/')
			
			if len(pic_list) == 0:
				''' No lemur images, just post the tweet '''
				await self.bot.send_message(dest, '{0} on Twitter: {1}'.format(
					random.choice(dev_names),
					tweet))
			else:
				''' Lemur images exist, pick random one and move it to used folder '''
				pic = random.choice(pic_list)
				await self.bot.send_file(
					dest,
					'../images/lemurs/{0}'.format(pic),
					content='{0} on Twitter: {1}'.format(
						random.choice(dev_names),
						tweet))
				''' Move lemur pic to used folder '''
				os.rename('../images/lemurs/{0}'.format(pic),
						'../images/lemurs_used/{0}'.format(pic))
