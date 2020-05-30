import asyncio
import discord

from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cleanup(self, ctx):
        def is_me(m):
            return m.author == self.bot.user

        def is_cmd(m):
            return m.content.startswith("!")

        del_cmd_msgs = await ctx.message.channel.purge(
            limit=20,
            check=is_cmd,
            bulk=True)

        del_bot_msgs = await ctx.message.channel.purge(
            limit=20,
            check=is_me,
            bulk=True)

        await ctx.send("Deleted {0} User commands and {1} Bot messages.".format(
            len(del_cmd_msgs), len(del_bot_msgs)))

    @commands.command()
    async def topic(self, ctx, *, args: str):
        if len(args.split()) == 1 and args.lower() == "clear":
            await ctx.message.channel.edit(topic="")
        else:
            await ctx.message.channel.edit(topic=args)

    @topic.error
    async def topic_err(self, ctx, err):
        await ctx.send("!topic rest of topic..., !topic clear")
