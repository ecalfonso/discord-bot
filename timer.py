import asyncio
import datetime
import discord

from discord.ext import commands

async def global_timer(bot):
    await bot.wait_until_ready()
    await asyncio.sleep(10)

    while(True):
        

        await asyncio.sleep(10)
