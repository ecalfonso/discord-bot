import asyncio
import time
import random
import discord
from discord.ext import commands

TOKEN = 'Mzk1MDc5Nzg4NTM0MTY5NjAw.DSN07A._Y5mfwy9vPe9wWSx66TK1LIxUWM'

description = '''Squid Squad Meme Lord

-I track brb's
-I emote (popular) games

Ask ealfonso for more features'''
bot = commands.Bot(command_prefix='?', description=description)

IDs = {}
IDs['PTR'] = '395093950345773077'
IDs['Bot'] = '395079788534169600'
IDs['Eduard'] = '269326001677271040'
IDs['Jesse'] = '65226686689452032'
IDs['Leon'] = '144614634824007680'

@bot.event
async def on_ready():
	await bot.edit_profile(username="Squid Squad BOT")
	await bot.change_presence(game=discord.Game(name='Big Brother'))
	print('------')
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
'''
@bot.event
async def on_member_update(mem_before, mem_after):
	global IDs

	""" If Jesse goes Idle. Call him out and post JesseBRB.png """
	if mem_after.id == IDs['Jesse'] and mem_after.status == discord.Status.idle and mem_before.status != discord.Status.idle:
		await bot.send_file(mem_after.server.default_channel, 'images/JesseBRB.jpg', content='<@{0}> BRB\'d <:JesseBRB:334162261922807808>'.format(IDs['Jesse']))
'''
@bot.event
async def on_reaction_add(reaction, user):
	""" Log all reactions and the User who reacted """
	global IDs

	line = "{0};{1}".format(user, reaction.emoji)
	print('rx:' + line)

	""" Ignore logging for PTR Server """
	if user.server.id != IDs['PTR']:
		f = open('logs/emoji_history.log', 'a')
		f.write('\n' + line)
		f.close()

@bot.event
async def on_voice_state_update(mem_before, mem_after):
	""" Listener to have BOT leave if left alone in a voice channel """
	if mem_before.id == IDs['Bot'] or not bot.is_voice_connected(mem_before.server):
		return

	for x in bot.voice_clients:
		if mem_before.voice.voice_channel == x.channel:
			if len(x.channel.voice_members) == 1:
				await x.disconnect()
			return

@bot.event
async def on_message(msg):
	""" Listen to all messages and respond appropriately """
	global IDs

	if msg.author.id == IDs['Bot']:
		return

	line = "{0};{1}".format(msg.author, msg.content.lower())
	print('chat:' + line)

	""" Ignore logging for PTR Server """
	if msg.server.id != IDs['PTR']:
		f = open('logs/text_history.log', 'a')
		f.write('\n' + line)
		f.close()

	""" Test block """
	if msg.author.id == IDs['Eduard'] and msg.content.lower() == 'test':
		print(msg.channel.position)
		return	

	""" Commands """
	if msg.content.lower().startswith('!help'):
		await bot.send_message(msg.channel, """```asciidoc
Official Squid Squad Bot
Commands:
!help	
	- Displays this message
!carjesse
	- Use when Car Jesse arrives
!decision
	- Gives you a Yes or a No
!conch
	- All hail the magic conch!
!8ball
	- Ask the magic 8-ball anything
!lootbox
	- Rolls Legendary or Exotic Destiny 2 Power Weapons
!emojiparty
	- Bot reacts with up to 20 random server emotes
!timer
	- Say !timer X for a timer up to 60 minutes

Automation:
brb
	- Reacts with :JesseBRB:
pubg|league|aram|overwatch|raid|lair
	- Reacts with appropriate emoji
taco
	- Reacts with taco
taco bravo
	- Gives user warning
ww@
	- Maybe you should try again
delete this
	- Delete this Nephew
```""")
		return

	if msg.content.startswith('!decision'):
		decision_items = {"Decision: Yes": 48, "Decision: No": 48, "Try again later": 2}
		await bot.send_message(msg.channel, random.choice([k for k in decision_items for dummy in range(decision_items[k])]))
		return

	if msg.content.startswith('!conch'):
		conch_items = {"Maybe someday": 5, "Nothing": 5, "Neither": 5, "I don't think so": 5, "No": 5, "Try asking again": 3, "Yes": 1}
		await bot.send_message(msg.channel, "Conch: " + random.choice([k for k in conch_items for dummy in range(conch_items[k])]))
		return

	if msg.content.startswith('!8ball'):
		magic_8ball_items = ["It is certain","It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it, yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Cannot predict now","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
		await bot.send_message(msg.channel, "Magic 8-ball: " + magic_8ball_items[random.randint(0, len(magic_8ball_items)-1)])
		return

	if msg.content.startswith('!carjesse'):
		await bot.send_message(msg.channel, "Car <@{0}> has arrived! Vroom vroom".format(IDs['Jesse']), tts=(msg.author.id == IDs['Eduard'] or msg.author.id == IDs['Jesse']))
		await bot.send_file(msg.channel, 'images/CarJesse.png')
		return

	if msg.content.startswith('!emojiparty'):
		emoji_count = len(msg.server.emojis)
		if emoji_count > 20:
			emoji_count = 20
		random_emojis = random.sample(msg.server.emojis, emoji_count)
		for i in random_emojis:
			await bot.add_reaction(msg, "{0}:{1}".format(i.name, i.id))
		return

	if msg.content.lower().startswith('!lootbox'):
		power_weapons = {
			"Exotic": {
				"Fusion Rifle": {
					"Merciless",
					"Telesto"
					},
				"Sniper Rifle": {
					"Borealis",
					"D.A.R.C.I"
					},
				"Shotgun": {
					"Legend of Acrius",
					"Tractor Cannon"
					},
				"Rocket Launcher": {
					"The Wardcliff Coil"
					},
				"Grenade Launcher": {
					"The Colony",
					"The Prospector"
					},
				"Swords": {
					"<@{0}>'s Cock".format(IDs['Jesse'])
					}
				},
			"Legendary": {
				"Fusion Rifle": {
					"Cartesian Coordinate",
					"Conjecture TSc",
					"Critical Sass",
					"Crooked Fang-4fr",
					"Dead-Ender",
					"Elatha FR4",
					"Erentil FR4",
					"Main Ingredient",
					"Man o' War",
					"Nox Echo III",
					"Nox Veneris II",
					"Shock and Awe",
					"Tarantula",
					"The Wizened Rebuke",
					"Timelins' Vertex"
					},
				"Sniper Rifle": {
					"Alone as a god",
					"A Single Clap",
					"Belfry Bounty",
					"Copperhead-4sn",
					"Distant Tumulus",
					"Elegy-49",
					"Eye of Foresight",
					"Gentleman Vagabond",
					"Maestro-46",
					"Maxim XI",
					"Persuader",
					"Shepherd's Watch",
					"Show of force",
					"The Domino",
					"The Long Walk",
					"The Mornin' Comes",
					"Veleda-D",
					"Widow's Bite"
					},
				"Shotgun": {
					"A Sudden Death",
					"Baligant",
					"Deadpan Delivery",
					"First In, Last Out",
					"Good Bone Structure",
					"Gravity Slingshot",
					"Gunnora's Axe",
					"Hawthorne's Field-Forged Shotgun",
					"Perfect Paradox",
					"Quitclaim Shotgun III",
					"Retrofuturist",
					"Somerled-D",
					"The Decide",
					"Unifaction VIII",
					"Zenith of Your Kind"
					},
				"Rocket Launcher": {
					"Blue Shift",
					"Classical-42",
					"Countless SA/2",
					"Curtain Call",
					"Hoosegow",
					"Morrigan-D",
					"Mos Epoch III",
					"Pentatonic-48",
					"Sins of the Past",
					"Tiebreaker",
					"Zenobia-D"
					},
				"Grenade Launcher": {
					"Acantha-D",
					"Berenger's Memory",
					"Bushwhacker",
					"Flash and Thunder",
					"I Am Alive",
					"Inteference VI",
					"Memory Interdict",
					"Orewing's Maul",
					"Orthrus",
					"Play of the Game",
					"Sunrise GL4",
					"The Day's Fury",
					"Truthteller",
					"Wicked Sister"
					},
				"Sword": {
					"Complex Solution",
					"Crown-Splitter",
					"Double-Edged Answer",
					"Eternity's Edge",
					"Future Safe 10",
					"Honor's Edge",
					"It Stared Back",
					"Negative Space",
					"Quickfang",
					"Steel Sybil Z-14",
					"Traitor's Fate",
					"Unspoken Promise",
					"Zephyr"
					}
				}
		} 

		roll = random.randint(1, 100)
		if roll > 95:
			rarity = "Exotic"
		else:
			rarity = "Legendary"
		category, weap_list = random.choice(list(power_weapons[rarity].items()))
		#print("Category: {0}, Weapon: {1}".format(category, random.choice(list(weap_list))))
		await bot.send_message(msg.channel, "<@{0}> rolled the {1} {2}: {3}".format(msg.author.id, rarity, category, random.choice(list(weap_list))))
		return

		"""
		lootbox_items_d2 = { "Basic": 3, "Uncommon": 4, "Rare": 5, "Legendary": 2, "Exotic": 1}
		lootbox_items_ow = { "Common": 5, "Rare": 6, "Epic": 2, "Legendary": 1}
		results = {}
		if "ow" in msg.content.lower() or "overwatch" in msg.content.lower():
			for i in range(4):
				results[i] = random.choice([k for k in lootbox_items_ow for dummy in range(lootbox_items_ow[k])])
		else:
			for i in range(4):
				results[i] = random.choice([k for k in lootbox_items_d2 for dummy in range(lootbox_items_d2[k])])
		await bot.send_message(msg.channel, "<@{0}> rolled: {1}, {2}, {3} and {4}!".format(
										msg.author.id, results[0], results[1], results[2], results[3]))
		"""
		return

	if msg.content.lower().startswith('!timer'):
		for i in msg.content.split():
			if i.isdigit():
				if int(i) > 60:
					i = 60
				await bot.send_message(msg.channel, "{0} minute timer set for <@{1}>".format(int(i), msg.author.id))
				await asyncio.sleep(int(i)*60)
				await bot.send_message(msg.channel, "<@{0}> {1} minute timer is done!".format(msg.author.id, int(i)))
				return
		return
	
	if msg.content.lower().startswith('!unfair'):
		await bot.send_message(msg.channel, "{0} is unfair\n<@{1}> is in there\nStandin' at the concession\nPlottin' his oppression\n#FreeMe -<@{2}>".format(
																	msg.server, IDs['Jesse'], IDs['Bot']))
		return

	""" Music Code """
	if msg.content.lower().startswith('$joinme'):
		if msg.author.voice.voice_channel != None:
			if bot.is_voice_connected(msg.server):
				for x in bot.voice_clients:
					return await x.move_to(msg.author.voice.voice_channel)
			else:
				await bot.join_voice_channel(msg.author.voice.voice_channel)
			await bot.delete_message(msg)
		else:
			await bot.send_message(msg.channel, "{0} is not in a voice channel".format(msg.author))
		return
	
	if msg.content.lower().startswith('$leave'):
		if bot.is_voice_connected(msg.server):
			for x in bot.voice_clients:
				await x.disconnect()
				await bot.delete_message(msg)
				return
		else:
			await bot.send_message(msg.channel, "I am not in a voice channel")
		return

	to_play = None
	if msg.content.lower().startswith('$money'):
		to_play = 'money.mp3'
	elif msg.content.lower().startswith('$wadu'):
		to_play = 'waduhek.mp3'
	elif msg.content.lower().startswith('$english'):
		to_play = 'english.mp3'
	elif msg.content.lower().startswith('$no'):
		to_play = 'no.mp3'
	elif msg.content.lower().startswith('$gotcha'):
		to_play = 'gotcha.mp3'
	elif msg.content.lower().startswith('$ultra'):
		to_play = 'ultra.mp3'
	if to_play != None:
		if bot.is_voice_connected(msg.server):
			for x in bot.voice_clients:
				try:
					player = x.create_ffmpeg_player('sounds/{0}'.format(to_play))
					player.start()
				except:
					await bot.send_message(msg.channel, "I crashed :(")
			return await bot.delete_message(msg)

	""" Reaction Code """
	if "brb" in msg.content.lower():
		if msg.author.id == IDs['Jesse']:
			await bot.send_file(msg.channel, 'images/JesseBRB.jpg')
		else:
			await bot.add_reaction(msg, 'JesseBRB:334162261922807808')
		await bot.move_member(msg.author, msg.server.afk_channel)

	if "raid" in msg.content.lower():
		if "lair" in msg.content.lower():
			await bot.add_reaction(msg, '🇱')
			await bot.add_reaction(msg, '🇦')
			await bot.add_reaction(msg, '🇮')
			await bot.add_reaction(msg, '🇷')
			await bot.add_reaction(msg, '❔')
		else:
			await bot.add_reaction(msg, '🇷')
			await bot.add_reaction(msg, '🇦')
			await bot.add_reaction(msg, '🇮')
			await bot.add_reaction(msg, '🇩')
			await bot.add_reaction(msg, '❔')
	if (
		"pubg" in msg.content.lower() or
		"fortnite" in msg.content.lower()
			):
		await bot.add_reaction(msg, '🇵')
		await bot.add_reaction(msg, '🇺')
		await bot.add_reaction(msg, '🇧')
		await bot.add_reaction(msg, '🇬')
		await bot.add_reaction(msg, '❔')
	if ( 
		"league" in msg.content.lower() or
		"overwatch" in msg.content.lower() or
		"destiny" in msg.content.lower() or
		"aram" in msg.content.lower()
		   ):
		await bot.add_reaction(msg, '💩')

	if "ww@" in msg.content.lower():
		await bot.add_reaction(msg, 'TryAskingAgain:355216367324233730')

	if "taco" in msg.content.lower():
		if "bravo" in msg.content.lower():
			await bot.add_reaction(msg, '🚫')
			await bot.send_message(msg.channel, "PSA by <@{0}>: AVOID TACO BRAVO".format(IDs['Leon']))
			await bot.send_file(msg.channel, 'images/HereLiesLeon.png')
		else:
			await bot.add_reaction(msg, '🌮')

	if "delete this" in msg.content.lower():
		await bot.add_reaction(msg, '🇩')
		await bot.add_reaction(msg, '🇪')
		await bot.add_reaction(msg, '🇱')
		await bot.add_reaction(msg, '3⃣')
		await bot.add_reaction(msg, '🇹')

	if "bet" in msg.content.lower():
		await bot.add_reaction(msg, '🇧')
		await bot.add_reaction(msg, '🇪')
		await bot.add_reaction(msg, '🇹')

	if "monika" in msg.content:
		print(msg.content.replace("monika", "M̢o̶͟͞ń͞i̡̛͘k̢̕a̸̡"))
		await bot.send_message(msg.channel, "<@{0}>: {1}".format(msg.author.id, msg.content.replace("monika", "M̢o̶͟ń͞i̛͘k̢̕a̸̡")))
		await bot.delete_message(msg)

	if "Monika" in msg.content:
		print(msg.content.replace("Monika", "M̢o̶͟͞ń͞i̡̛͘k̢̕a̸̡"))
		await bot.send_message(msg.channel, "<@{0}>: {1}".format(msg.author.id, msg.content.replace("Monika", "M̢o̶͟ń͞i̛͘k̢̕a̸̡")))
		await bot.delete_message(msg)

bot.run(TOKEN)
