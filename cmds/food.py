import aiohttp
import asyncio
import discord
import json
from discord.ext import commands

class Food:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True, no_pm=True)
	async def food(self, ctx):
		url = 'http://www.themealdb.com/api/json/v1/1/random.php'

		async with aiohttp.get(url) as response:
			if response.status == 200:
				data = await response.json()

				mealName = data['meals'][0]['strMeal']
				mealURL = data['meals'][0]['strSource']

				await self.bot.say('<@{0}> should cook "{1}". The recipe is: {2}'.format(
					ctx.message.author.id,
					mealName,
					mealURL
					))

			else:
				print('HTTP Get Err')
