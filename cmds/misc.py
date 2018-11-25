import asyncio
import discord
import random

from discord.ext import commands
from functions import *

from cmds.fortnite import dance

howdy_msg = "⠀ ⠀ :cowboy:\n\
   :flag_us::flag_us::flag_us:\n\
 :flag_us:   :flag_us:  :flag_us:\n\
:point_down::skin-tone-3: :flag_us::flag_us::point_down::skin-tone-3:\n\
      :flag_us: :flag_us:\n\
　:flag_us:    :flag_us:\n\
　:boot:　 :boot:"

mean_quotes = [
("63520170265550848", 48),
("63520170265550848", 81),
("65930387506855936", 61),
("65930387506855936", 130),
("63522168096436224", 52),
("63522168096436224", 79),
("100850844991262720", 11),
("95437153479168000", 2),
]

class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def chris(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/yikes/")

    @commands.command(pass_context=True)
    async def cough(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/cough/")

    @commands.command(pass_context=True)
    async def cute(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/cute/")

    @commands.command(pass_context=True)
    async def dance(self, ctx):
        m = await self.bot.say(dance[0])
        for d in dance:
            await self.bot.edit_message(m, d)
            await asyncio.sleep(1)
        await asyncio.sleep(5)
        await self.bot.delete_message(m)   
        await self.bot.delete_message(ctx.message)   

    @commands.command(pass_context=True)
    async def feet(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/feet/")

    @commands.command(pass_context=True, no_pm=True)
    async def friends(self, ctx):
        friends_list = ['Chris', 'Jeremy', 'Justin', 'Tammy', 'Vince', 'Eddie', 'Joseph', 'Jesse', 'Leon', 'Chad', 'Brad', 'Luke']
        for e in ctx.message.server.emojis:
            for f in friends_list:
                if f.lower() in e.name.lower():
                    await self.bot.add_reaction(ctx.message, "{}:{}".format(e.name, e.id))

    @commands.command(pass_context=True)
    async def here(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/here/")

    @commands.command(pass_context=True)
    async def howdy(self, ctx):
        if random.randint(0,1) == 1:
            await postRandomPic(self.bot, ctx.message, "../images/howdy/")
        else:
            await self.bot.say(howdy_msg)

    @commands.command(pass_context=True)
    async def mean(self, ctx):
        # If Chris, post a mean quote about him
        if ctx.message.author == discord.utils.get(ctx.message.server.members, name="clopezpe"):
            mem, i = random.choice(mean_quotes)
            quote_data = readJson("../data/quotes.data")
            mem_obj = await self.bot.get_user_info(mem)
            await self.bot.say("{}: {}".format(
                    mem_obj.display_name, 
                    quote_data[mem][i]))
        else:
            await postRandomPic(self.bot, ctx.message, "../images/mean/")

    @commands.command(pass_context=True)
    async def salt(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/salt/")

    @commands.command(pass_context=True)
    async def sleep(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/sleep/")

    @commands.command(pass_context=True)
    async def ugly(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/ugly/")

    @commands.command(pass_context=True)
    async def yikes(self, ctx):
        await postRandomPic(self.bot, ctx.message, "../images/yikes/")

    @commands.command(pass_context=True)
    async def unfair(self, ctx):
        await self.bot.say("{0} is unfair\n<@{1}> is in there\nStandin' at the concession\nPlottin' his oppression\n#FreeMe -<@{2}>".format(
            ctx.message.server, 
            ctx.message.server.owner.id,
            self.bot.user.id))
