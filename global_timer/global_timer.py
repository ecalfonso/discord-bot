import asyncio
import datetime
import discord

from discord.ext import commands
from functions import *
from global_vars import *

from global_timer.monday_punday import *
from global_timer.wednesday_check import *

async def global_timer(bot):
    await bot.wait_until_ready()
    await asyncio.sleep(10)

    while(True):
        now = datetime.datetime.now()

        # Monday Check
        if now.weekday() == 0 and \
                now.hour == 0 and \
                (now.minute == 0 or \
                now.minute == 1):
            await monday_punday(bot)

        # Wednesday check
        if now.weekday() == 2 and \
                now.hour == 0 and \
                (now.minute == 0 or \
                now.minute == 1):
            await wednesday_check(bot)

        # 2 Minute delay between polling
        await asyncio.sleep(120)
