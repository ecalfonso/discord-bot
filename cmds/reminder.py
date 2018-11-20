import asyncio
import time
import discord

from discord.ext import commands
from functions import *

class Timer:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def timer(self, ctx, *, args: str):
        global timer_data

        if (len(args.split()) % 2) == 0:
            duration = 0
            op = 1
            for a in args.split():
                if op == 1:
                    if a.isdigit():
                        add_time = int(a)
                        op = 2
                    else:
                        await errMsg(self.bot, ctx, "Usage: !timer X hours Y minutes Z seconds")
                        return
                elif op == 2:
                    if a in ["hours", "hour", "hrs", "hr", "h"]:
                        duration += add_time * 3600
                    elif a in ["minutes", "minute", "mins", "min", "m"]:
                        duration += add_time * 60
                    elif a in ["seconds", "second", "secs", "sec", "s"]:
                        duration += add_time
                    else:
                        await errMsg(self.bot, ctx, "Incorrect time type, use hours/hour/hrs/hr/h, minutes/minute/mins/min/m, seconds/second/secs/sec/s")
                        return
                    op = 1
            await self.bot.add_reaction(ctx.message, "☑")
            await asyncio.sleep(duration)
            await self.bot.say("<@{}> {} timer is complete!".format(ctx.message.author.id, args))
        else:
            await errMsg(self.bot, ctx, "Usage: !timer X hours Y minutes Z seconds")
            return

    @timer.error
    async def timer_err(self, error, ctx):
        await errMsg(self.bot, ctx, "Usage: !timer X hours Y minutes Z seconds")
