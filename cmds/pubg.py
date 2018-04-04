import aiohttp
import asyncio
import discord
import json
import random
from discord.ext import commands
from dictionaries.help_docs import *
from dictionaries.pubg_lists import *
from dictionaries.IDs import *

class Pubg:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def pubg(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say(help_pubg)

	@pubg.command(pass_context=True, no_pm=True)
	async def map1(self, ctx):
		hot_items = {'High': 60, 'Mid-high': 25, 'Mid-low':12, 'Low': 3}
		hotness = random.choice([k for k in hot_items for dummy in range(hot_items[k])])
		drop = random.sample(erangel_locs[hotness], 1)[0]
		await self.bot.say('Drop: {0}'.format(str(drop)))

	@pubg.command(pass_context=True, no_pm=True)
	async def map2(self, ctx):
		hot_items = {'High': 75, 'Mid': 22, 'Low': 3}
		hotness = random.choice([k for k in hot_items for dummy in range(hot_items[k])])
		drop = random.sample(miramar_locs[hotness], 1)[0]
		await self.bot.say('Drop: {0}'.format(str(drop)))

	@pubg.command(pass_context=True, no_pm=True)
	async def rpg(self, ctx, *, args):
		classes = ['DPS', 'Healer', 'Tank', 'Hunter']
		msg = ""

		for p in args.split():
			if p.startswith('<@'):
				c = random.choice(classes)
				classes.remove(c)
				msg += '{0} is {1}\n'.format(
						p,
						c)
		await self.bot.say(msg)

	@pubg.command(pass_context=True, no_pm=True)
	async def stats(self, ctx, *, args):
		pubg_api_player_url = 'https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]='
		pubg_api_match_url = 'https://api.playbattlegrounds.com/shards/pc-na/matches/'

		json_headers = {
			"Authorization": Tokens['PUBG'],
			"Accept": "application/vnd.api+json",
			"Accept-Encoding": "gzip"
		}

		# Try to get stats for Username
		name = args.split()[0]

		async with aiohttp.get(
			pubg_api_player_url + name,
			headers=json_headers) as player_resp:
			if player_resp.status == 200:
				player = await player_resp.json()
				matches = player['data'][0]['relationships']['matches']['data']

				num_matches = min(3, len(matches))

				if num_matches == 0:
					await self.bot.say('{0} has no recent matches.'.format(name))
					return
			elif player_resp.status == 404:
				await self.bot.say('No PUBG player with that name exists!')
			elif player_resp.status == 429:
				await self.bot.say('Being rate-limited by PUBG API, wait a minute.')
			else:
				await self.bot.say('HTTP Error {0} while making request.'.format(player_resp.status))

		# Initial message
		msg = 'Last 3 PUBG matches for {0}:'.format(name)

		# Try to get matches
		for i in range(num_matches):
			async with aiohttp.get(
				pubg_api_match_url + matches[i]['id'],
				headers=json_headers) as match_resp:
				if match_resp.status == 200:
					match = await match_resp.json()
					msg += '\n\nMode: {0}\n'.format(match['data']['attributes']['gameMode'])

					# Extract specific player from list of all players in match
					for p in match['included']:
						if p['type'] == 'participant' and p['attributes']['stats']['name'].lower() == name.lower():
							msg += 'Rank: {0}\n'.format(p['attributes']['stats']['winPlace'])
							msg += 'Kills: {0}'.format(p['attributes']['stats']['kills'])
							break
				else:
					print('HTTP Error {0} on match loop itr {1}'.format(match_resp.status, i))
					break

		await self.bot.say(msg)
