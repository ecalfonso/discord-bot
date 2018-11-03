import asyncio
import datetime
import discord
import global_vars
import json
import os
import random

from pathlib import Path

''' Async functions '''
async def errMsg(bot, ctx, msg):
    tmp = await bot.say(msg)
    await asyncio.sleep(10)
    await bot.delete_message(tmp)
    await bot.delete_message(ctx.message)

async def postPic(bot, ctx, f_name, msg=""):
    if Path(f_name).is_file():
        await bot.send_file(
            ctx.message.channel,
            f_name,
            content=msg)
    else:
        print("{} doesn't exist".format(f_name))

async def postRandomPic(bot, msg, dir_name):
    if os.path.isdir(dir_name):
        pics = os.listdir(dir_name)
        pic = random.choice(pics)
        await bot.send_file(msg.channel, dir_name + pic)
    else:
        print("{} doesn't exist!".format(dir_name))

async def reactToMsg(bot, msg, reactions):
    for r in reactions:
        await bot.add_reaction(msg, r)

''' Regular Functions '''
def log(obj, obj2=None):
    now = datetime.datetime.now()
    cur_time = "{0}-{1:02d}-{2:02d} {3:02d}:{4:02d}".format(
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute)

    if type(obj) == discord.message.Message:
        f_name = "../logs/chat_history.log"
        line = "{0};;{1};;{2};;{3};;{4}".format(
            cur_time,
            obj.author.id,
            obj.author,
            obj.id,
            obj.content)
    elif type(obj) == discord.reaction.Reaction:
        f_name = "../logs/emoji_history.log"
        line = "{0};;{1};;{2};;{3};;{4}".format(
            cur_time,
            obj.message.author.id,
            obj.message.author,
            obj.message.id,
            obj.emoji)
    elif type(obj) == discord.member.Member:
        f_name = ""
        line = "{0};;{1};;{2};;{3} -> {4}".format(
            cur_time,
            obj.id,
            obj,
            obj.nick,
            obj2.nick)

    # Write to log file
    if global_vars.PROD:
        if Path(f_name).is_file():
            f = open(f_name, 'a')
            f.write('\n{0}'.format(line))
            f.close()
        else:
            print("Log file {} doesn't exist!".format(f_name))
    else:
        print("Skipping writing to {}".format(f_name))

    # Output to console
    print(line)

def readJson(f_name):
    if not Path(f_name).is_file():
        print("Error: \"{}\" does not exist!".format(f_name))
    else:
        return json.load(open(f_name))

def writeJson(f_name, data):
    with open(f_name, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()

