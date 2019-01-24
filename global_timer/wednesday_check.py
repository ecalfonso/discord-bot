import aiohttp
import datetime
import discord
import global_vars
import json
import re

from discord.ext import commands
from pathlib import Path

async def wednesday_check(bot):
    if global_vars.PROD:
        dest = discord.utils.get(bot.get_all_channels(),
                server__name="くコ:彡Squid Squad くコ:", 
                name="general")
    else:
        dest = discord.utils.get(bot.get_all_channels(),
                server__name="くコ:彡Squid Squad くコ: test", 
                name="general")

    await bot.send_file(dest,
            '../images/wednesday/w1.jpg')
