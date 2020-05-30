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

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = readJson(quotes_file)

    def writeQuotes(self):
        if global_vars.PROD:
            writeJson(quotes_file, self.data)
        else:
            print("Skipping write to {} on TestBot".format(quotes_file))

    @commands.group()
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            await errMsg(self.bot, ctx, "!quote... leaderboard, random, remove, save, show")

    @quote.command()
    async def leaderboard(self, ctx):
        l = {}
        for p in self.data:
            l[p] = len(self.data[p])

        async with ctx.channel.typing():
            l = sorted(l.items(), key=operator.itemgetter(1), reverse=True)
            msg = "Quote leaderboard:\n"

            itr = 1
            for p in l:
                try:
                    user = await self.bot.fetch_user(p[0])
                except:
                    continue

                msg += "{0}. {1} with {2}\n".format(itr, user.display_name, p[1])
                itr += 1

            await ctx.send(msg)

    @quote.command()
    async def random(self, ctx, *, args: str):
        try:
            person_id = re.search("<@(.+?)>|<@!(.+?)>", args.split()[0]).group(1)

            if person_id.startswith("!"):
                person_id = person_id[1:]
        except AttributeError:
            await errMsg(self.bot, ctx, "First argument needs to be a server member")
            return

        if person_id in self.data:
            await ctx.send("<@{0}> {1}: {2}".format(
                person_id,
                random.choice(quote_beginnings),
                random.choice(self.data[person_id])))
        else:
            await ctx.send("No saved quotes for <@{0}>!".format(person_id))

    @random.error
    async def random_err(self, error, ctx):
        await errMsg(self.bot, ctx, "First argument needs to be a server member")

    @quote.command()
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

        if person_id not in self.data:
            await errMsg(self.bot, ctx, "<@{0}> does not have quotes!".format(person_id))
            return

        if int(number_to_remove) > len(self.data[person_id]):
            await errMsg(self.bot, ctx, "Value needs to be a number between 1 and {0}".format(
                len(self.data[person_id])))
            return

        if person_id in self.data:
            self.data[person_id].remove(self.data[person_id][int(number_to_remove)-1])

            self.writeQuotes()
            await ctx.message.add_reaction("☑")
        else:
            await ctx.send("No saved quotes for <@{0}>!".format(person_id))

    @remove.error
    async def remove_err(self, error, ctx):
        await errMsg(self.bot, ctx, "First argument needs to be a server member")

    @quote.command()
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
        msg += "at {0:02d}:{1:02d} {2:02d}/{3:02d}/{4}".format(
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

        await ctx.message.add_reaction("☑")

    @save.error
    async def save_err(self, error, ctx):
        #await errMsg(self.bot, ctx, "First argument needs to be a server member")
        await ctx.send("First argument needs to be a server member")

    @quote.command()
    async def search(self, ctx, *, args: str):
        if len(args.split()) < 2:
            await errMsg(self.bot, ctx, "Enter a server member and a search term")
            return

        try:
            person_id = re.search("<@(.+?)>|<@!(.+?)>", args.split()[0]).group(1)
            if person_id.startswith("!"):
                person_id = person_id[1:]
        except AttributeError:
            await errMsg(self.bot, ctx, "First argument needs to be a server member")
            return

        search_arg = args.split()[1:]
        search_term = ""
        for s in search_arg:
            search_term += "{} ".format(s.replace('"',""))
        search_term = search_term[:-1]

        if person_id in self.data:
            quote_list = ""
            itr = 0
            for q in self.data[person_id]:
                itr += 1
                if search_term.lower() in q.lower():
                    quote_list += "{}. {}\n".format(itr, q)
            if not quote_list:
                msg = "<@{}> has not mentioned \"{}\" in their quotes.".format(person_id, search_term)
            else:
                msg = "<@{}> said \"{}\" in these quotes:\n".format(person_id, search_term) + quote_list
            await ctx.send("{0}".format(msg))
        else:
            await ctx.send("No saved quotes for <@{0}>!".format(person_id))

    @quote.command()
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
                        await ctx.send("{0}".format(msg))
                        msg = ""
                    msg += "{0}. {1}\n".format(itr, q)
                    itr += 1

            await ctx.send("{0}".format(msg))
        else:
            await ctx.send("No saved quotes for <@{0}>!".format(person_id))
