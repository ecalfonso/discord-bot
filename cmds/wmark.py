import aiohttp
import asyncio
import discord
import json
import os
from discord.ext import commands
from dictionaries.help_docs import *
from dictionaries.IDs import IDs
from PIL import Image

class Wmark:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def wmark(self, ctx, *, args: str):
		''' Check if DM or not '''
		if ctx.message.channel.is_private:
			dest = self.bot.get_channel(IDs['Squid Squad Server'])
			if dest == None:
				await self.bot.say('I do not have access to that channel')
				return
		else:
			dest = ctx.message.channel

		''' Parse logo to be used '''
		logo = args.split()[0]
		supp_logo = ['test', 'brazzers']
		if not logo in supp_logo:
			await self.bot.say('Not a supported logo')
			return

		logo_fname = '../images/logos/{0}.png'.format(logo)

		''' Check for attachments '''
		if not ctx.message.attachments:
			await self.bot.say('You need to attach a photo for me to meme')
			return
		url = ctx.message.attachments[0]['url']
		img_fname = 'tmp.{0}'.format(url.split('.')[-1])

		''' Try to download user's image '''
		async with aiohttp.get(url) as response:
			data = await response.read()
			with open(img_fname, 'wb') as outfile:
				outfile.write(data)

		''' Add logo '''
		mimage = Image.open(img_fname)
		limage = Image.open(logo_fname)

		# resize logo
		wsize = int(min(mimage.size[0], mimage.size[1]) * 0.75)
		wpercent = (wsize / float(limage.size[0]))
		hsize = int((float(limage.size[1]) * float(wpercent)))

		simage = limage.resize((wsize, hsize))
		mbox = mimage.getbbox()
		sbox = simage.getbbox()

		# right bottom corner
		box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
		mimage.paste(simage, box)
		mimage.save(img_fname)
	
		''' Delete user uploaded img if not a DM '''
		if not ctx.message.channel.is_private:
			await self.bot.delete_message(ctx.message)
	
		''' Post to channel '''
		await self.bot.send_file(
			dest,
			img_fname
			)

		''' Cleanup file '''
		os.remove(img_fname)

'''
	@wmark.error
	async def wmark_err(self, error, ctx):
		await self.bot.say(help_wmark)
'''
