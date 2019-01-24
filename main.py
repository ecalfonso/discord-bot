import discord
import global_vars

from discord.ext import commands

''' Import Custom Modules '''
from message_handlers import *
from cmds.admin import *
from cmds.decisions import *
from cmds.menu import *
from cmds.misc import *
from cmds.music import *
from cmds.quotes import *
from cmds.reminder import *
from global_timer.global_timer import *

''' Global Variables '''
global_vars.init()

''' Load Opus for Music Bot '''
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

''' Create Bot '''
description = ''' Squid Squad Bot '''
bot = commands.Bot(command_prefix='!', description=description)
bot.add_cog(Admin(bot))
bot.add_cog(Decisions(bot))
bot.add_cog(Menu(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Music(bot))
bot.add_cog(Quotes(bot))
bot.add_cog(Timer(bot))

''' Bot Events '''
@bot.event
async def on_member_update(b_mem, a_mem):
    # Ignore Bot messages
    if a_mem.bot:
        return

    # Log member nickname change
    if b_mem.nick != a_mem.nick:
        log(b_mem, a_mem)

        ''' Load data '''
        nicknames_data = readJson("../data/nicknames.data")
        in_data = (a_mem.nick, datetime.datetime.now().timestamp())

        ''' Write to data '''
        if a_mem.id in nicknames_data:
            nicknames_data[a_mem.id].append(in_data)
        else:
            nicknames_data[a_mem.id] = [in_data]

        ''' Write back to file '''
        writeJson("../data/nicknames.data", nicknames_data)

@bot.event
async def on_message_edit(b_msg, a_msg):
    # Ignore Bot messages
    if a_msg.author.bot:
        return

    # Log message
    log(a_msg)

    # Process ! commands
    await bot.process_commands(a_msg)

    # Parse/Process message contents
    await msg_react(bot, a_msg)

@bot.event
async def on_message(msg):
    # Ignore Bot messages
    if msg.author.bot:
        return

    # Log message
    log(msg)

    # Process ! commands
    await bot.process_commands(msg)

    # Parse/Process message contents
    await msg_react(bot, msg)

@bot.event
async def on_reaction_add(rx, user):
    # Ignore Bots
    if user.bot:
        return

    # Log reaction
    log(rx)

@bot.event
async def on_ready():
    if global_vars.PROD:
        await bot.edit_profile(username="Squidy Bot")
    else:
        await bot.edit_profile(username="Test Bot")
    await bot.change_presence(game=discord.Game(name="Big Brother {0}".format(global_vars.version)))
    print('-----------------------------------------------------------')
    print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
    print('-----------------------------------------------------------')
    bot.loop.create_task(global_timer(bot))

''' Start Bot '''
while True:
    try:
        bot.run(global_vars.TOKEN)
    except KeyboardInterrupt:
        bot.close()
        print("CTRL+C Interrupt: Closing Bot...")
        break
    except ConnectionResetError:
        print("Discord disconnected us... Try to reconnect")
        continue
