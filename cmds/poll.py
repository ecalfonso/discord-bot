import aiohttp
import asyncio
import discord
import json
import re
from discord.ext import commands

class Poll:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def poll(self, ctx, *, args: str):
		poll_url = 'https://strawpoll.me/api/v2/polls'

		''' Post Poll '''

		if len(args.split()) > 1:
			poll_items = []
			for item in re.findall('"([^"]*)"', args):
				poll_items.append('{0}'.format(item))

				data = {
					"title": "Quick Poll",
					"options": poll_items
					}
			async with aiohttp.post(
				poll_url, 
				data=json.dumps(data), 
				headers={"Content-Type": "application/json"}) as post_resp:
				if post_resp.status == 200:
					poll_data = await post_resp.json()
					await self.bot.say('5-Minute Poll created for <@{0}>: http://www.strawpoll.me/{1}'.format(
						ctx.message.author.id, 
						poll_data['id']))
		else:
			await self.bot.say('Error: Not enough poll options')
			return

		''' Wait 5 minutes for people to vote '''
		await asyncio.sleep(5*60)

		''' Get final Poll data '''
		async with aiohttp.get('{0}/{1}'.format(poll_url, poll_data['id'])) as get_resp:
			if get_resp.status == 200:
				vote_data = await get_resp.json()
				max_votes = 0
				votes_index = 0
				i = 0
				for v in vote_data['votes']:
					if v > max_votes:
						max_votes = v
						votes_index = i
					i += 1
				
				await self.bot.say('"{0}" won the poll with {1} votes! <http://www.strawpoll.me/{2}/r>'.format(
					vote_data['options'][votes_index],
					max_votes,
					poll_data['id']))

	@poll.error
	async def poll_err(self, error, ctx):
		await self.bot.say('Usage: !poll "AA" "BB BB" ... "ZZZ"')
