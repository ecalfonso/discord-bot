import discord
import json

from pathlib import Path


''' Async functions '''
async def errMsg(bot, ctx, msg):
    tmp = await ctx.send(msg)
    await tmp.delete(delay=10)
    await ctx.message.delete(delay=10)

def readJson(f_name):
    if not Path(f_name).is_file():
        print("Error: \"{}\" does not exist!".format(f_name))
    else:
        return json.load(open(f_name))

def writeJson(f_name, data):
    with open(f_name, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()
