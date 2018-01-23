import asyncio
import discord
import random
from discord.ext import commands
from dictionaries.destiny_lists import *

class Lootbox:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def lootbox(self, ctx):
		weapon_type = random.choice(list({'Kinetic', 'Energy', 'Power'}))
		if weapon_type == 'Kinetic':
			weapons = kinetic_weapons.copy()
		elif weapon_type == 'Energy':
			weapons = energy_weapons.copy()
		else:
			weapons = power_weapons.copy()

		rarity_items = {'Exotic': 5, 'Legendary': 95}
		rarity = random.choice([k for k in rarity_items for dummy in range(rarity_items[k])])

		category, weapons_list = random.choice(list(weapons[rarity].items()))
		await self.bot.say('<@{0}> rolled a {1} {2} weapon {3}: {4}'.format(
			ctx.message.author.id,
			rarity, 
			weapon_type, 
			category, 
			random.choice(list(weapons_list))))
