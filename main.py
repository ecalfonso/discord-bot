import discord
import global_vars
import json
import os

from commands.Admin import *
from commands.Menu import *
from commands.Quotes import *
from discord.ext import commands

''' Initialize global variables '''
global_vars.init()

bot = commands.Bot(command_prefix='!')

bot.add_cog(Admin(bot))
bot.add_cog(Menu(bot))
bot.add_cog(Quotes(bot))

@bot.event
async def on_message(msg):
    ''' Ignore Bot messages '''
    if msg.author.bot:
        return
    
    ''' Print message to console '''
    print('{0}\t | {1} | {2}'.format(msg.author.name, 
        msg.created_at.now(), msg.content))

    ''' Process !prefix commands '''
    await bot.process_commands(msg)

@bot.event
async def on_message_edit(before_msg, after_msg):
    ''' Ignore Bot messages '''
    if after_msg.author.bot:
        return
    
    ''' Print message to console '''
    print('{0}\t | {1} | {2}'.format(after_msg.author.name, 
        after_msg.created_at.now(), after_msg.content))

    ''' Process !prefix commands '''
    await bot.process_commands(after_msg)

@bot.event
async def on_ready():
    if global_vars.PROD:
        await bot.user.edit(username='Squidy Bot Reborn')
    else:
        await bot.user.edit(username='Test Bot Reborn')

    await bot.change_presence(status=discord.Status.online,
            activity=discord.Activity(name='v{0}'.format(version)))

    print('-----------------------------------------------------------')
    print('Bot "{0}:{1}" logged in'.format(bot.user.name, bot.user.id))
    print('-----------------------------------------------------------')

''' Start Bot '''
bot.run(global_vars.TOKEN)
