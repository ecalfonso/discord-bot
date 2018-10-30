import asyncio
import random

import discord
from discord.ext import commands

magic_8ball_items = {
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most Likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful",
    "No"
}

yesno_items = {
    "Decision: Yes": 48,
    "Decision: No": 48,
    "Try again later": 2
}

conch_items = {
    "Maybe someday": 5,
    "Nothing": 5,
    "Neither": 5,
    "I don't think so": 5,
    "No": 7,
    "Try asking again": 3,
    "Yes": 1
}

class Decisions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def conch(self, ctx):
        await self.bot.say(
            "The conch says: {}. All Hail the Magic Conch!".format(
                random.choice([k for k in conch_items for dummy in range(conch_items[k])])
            )
        )

    @commands.command(pass_context=True)
    async def magic8(self, ctx):
        await self.bot.say("Magic 8-ball says: {0}".format(random.sample(magic_8ball_items, 1)[0]))

    @commands.command(pass_context=True)
    async def shuffle(self, ctx, *, args: str):
        num = 1
        l = args.split()
        if args.split()[0].isdigit():
            num = l[0]
            if int(num) > len(l):
                await self.bot.say("Choice must be below {}".format(len(l)-1))
            l.pop(0)
        msg = "Here are your {} choices: ".format(num)
        for x in random.sample(l, int(num)):
            msg += " {}".format(x)
        await self.bot.say(msg)

    @shuffle.error
    async def shuffle_err(self, ctx, err):
        await self.bot.say("Usage: !shuffle A B ... Z or !shuffle NUMBER A B ... Z")

    @commands.command(pass_context=True)
    async def yesno(self, ctx):
        await self.bot.say(random.choice([k for k in yesno_items for dummy in range(yesno_items[k])]))
