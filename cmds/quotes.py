import datetime
import discord
import global_vars
import operator
import random
import re

from discord.ext import commands
from functions import *
from global_vars import *

quote_beginnings = [
    "announced",
    "has said",
    "is famous for saying",
    "once said",
    "mentioned",
    "is known for saying"
]

quotes_file = "../data/quotes.data"

class Quotes:
    def __init__(self, bot):
        self.bot = bot
        self.data = readJson(quotes_file)

    def writeQuotes(self):
        if global_vars.PROD:
            writeJson(quotes_file, self.data)
        else:
            print("Skipping write to {} on TestBot".format(quotes_file))

    @commands.group(pass_context=True)
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            await errMsg(self.bot, ctx, "!quote... leaderboard, random, remove, save, show")

    @quote.command(pass_context=True)
    async def leaderboard(self, ctx):
        l = {}
        for p in self.data:
            l[p] = len(self.data[p])

        l = sorted(l.items(), key=operator.itemgetter(1), reverse=True)
        msg = "Quote leaderboard:\n"

        itr = 1
        for p in l:
            try:
                await self.bot.send_typing(ctx.message.channel)
                user = await self.bot.get_user_info(p[0])
            except:
                continue

            msg += "{0}. {1} with {2}\n".format(itr, user.display_name, p[1])
            itr += 1

        await self.bot.send_message(ctx.message.channel, msg)

    @quote.command(pass_context=True)
    async def random(self, ctx, *, args: str):
        try:
            person_id = re.search("<@(.+?)>|<@!(.+?)>", args.split()[0]).group(1)
            
            if person_id.startswith("!"):
                person_id = person_id[1:]
        except AttributeError:
            await errMsg(self.bot, ctx, "First argument needs to be a server member")
            return

        if person_id in self.data:
            await self.bot.say("<@{0}> {1}: {2}".format(
                person_id,
                random.choice(quote_beginnings),
                random.choice(self.data[person_id])))
        else:
            await self.bot.say("No saved quotes for <@{0}>!".format(person_id))

    @random.error
    async def random_err(self, error, ctx):
        await errMsg(self.bot, ctx, "First argument needs to be a server member")

    @quote.command(pass_context=True)
    async def remove(self, ctx, *, args: str):
        try:
            person_id = re.search("<@(.+?)>|<@!(.+?)>", args.split()[0]).group(1)
            if person_id.startswith("!"):
                person_id = person_id[1:]
        except AttributeError:
            await errMsg(self.bot, ctx, "First argument needs to be a server member")
            return

        number_to_remove = args.split()[1]
        if not number_to_remove.isdigit():
            await errMsg(self.bot, ctx, "Argument needs to be a Number. Use !quote show @person to get Numbers")
            return

        if int(number_to_remove) > len(self.data[person_id]):
            await errMsg(self.bot, ctx, "Value needs to be a number between 1 and {0}".format(
                                            len(self.data[person_id])))
            return

        if person_id in self.data:
            self.data[person_id].remove(self.data[person_id][int(number_to_remove)-1])

            self.writeQuotes()
            await self.bot.add_reaction(ctx.message, "☑")
        else:
            await self.bot.say("No saved quotes for <@{0}>!".format(person_id))

    @remove.error
    async def remove_err(self, error, ctx):
        await errMsg(self.bot, ctx, "First argument needs to be a server member")

    @quote.command(pass_context=True)
    async def save(self, ctx, *, args: str):
        if len(args.split()) == 1:
            await errMsg(self.bot, ctx, "No quote was entered.")
            return

        try:
            person_id = re.search("<@(.+?)>|<@!(.+?)>", args.split()[0]).group(1)

            if person_id.startswith("!"):
                person_id = person_id[1:]
        except AttributeError:
            await errMsg(self.bot, ctx, "First argument needs to be a server member")
            return
        
        ''' Construct Quote in var msg '''
        msg = ""
        for m in range(1, len(args.split())):
            msg += "{0} ".format(args.split()[m])

        ''' Generate timestamp '''
        now = datetime.datetime.today()
        msg += "at {0}:{1} {2}/{3}/{4}".format(
                now.hour,
                now.minute,
                now.month,
                now.day,
                now.year)

        ''' Check to see if this user already exists in the db 
            Then add the quote to the db
        '''
        if person_id in self.data:
            self.data[person_id].append(msg)
        else:
            self.data[person_id] = [msg]

        self.writeQuotes()

        await self.bot.add_reaction(ctx.message, "☑")

    @save.error
    async def save_err(self, error, ctx):
        await errMsg(self.bot, ctx, "First argument needs to be a server member")

    @quote.command(pass_context=True)
    async def show(self, ctx, *, args: str):
        try:
            person_id = re.search("<@(.+?)>|<@!(.+?)>", args.split()[0]).group(1)
            if person_id.startswith("!"):
                person_id = person_id[1:]
        except AttributeError:
            await errMsg(self.bot, ctx, "First argument needs to be a server member")
            return

        if person_id in self.data:
            # Extract specified quote #
            if len(args.split()) == 2:
                num_to_get = args.split()[1]
                if not num_to_get.isdigit():
                    await errMsg(self.bot, ctx, "Enter a valid number to get an exact quote.")
                    return

                if int(num_to_get) > len(self.data[person_id]):
                    await errMsg(self.bot, ctx, "Value needs to be a number between 1 and {0}.".format(
                                                len(self.data[person_id])))
                    return

                msg = "<@{0}> {1}: {2}".format(
                        person_id,
                        random.choice(quote_beginnings),
                        self.data[person_id][int(num_to_get)-1])

            # Build message from entire quote list
            else:
                itr = 1
                msg = "<@{0}> {1}:\n".format(person_id, random.choice(quote_beginnings))
                for q in self.data[person_id]:
                    # Dump message once Discord's 2000 char limit is reached
                    if (len(msg) + len(q) + 5) > 2000:
                        await self.bot.say("{0}".format(msg))
                        msg = ""
                    msg += "{0}. {1}\n".format(itr, q)
                    itr += 1

            await self.bot.say("{0}".format(msg))
        else:
            await self.bot.say("No saved quotes for <@{0}>!".format(person_id))

    #@show.error
    #async def show_err(self, error, ctx):
        #await errMsg(self.bot, ctx, "First argument needs to be a server member")
