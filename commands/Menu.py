import discord
import global_vars

from discord.ext import commands
from functions import *

menu_file = "../data/menu.data"

menu_header = "Squid Squad Restaurant Menu:\n\
-----------------------------------\n"

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = readJson(menu_file)

    def writeMenu(self):
        if global_vars.PROD:
            writeJson(menu_file, self.data)
        else:
            print("Skipping write to {} on TestBot".format(menu_file))

    @commands.group()
    async def menu(self, ctx):
        if ctx.invoked_subcommand is None:
            index = 1
            msg = menu_header
            for i in self.data["itemList"]:
                msg += "{0}. {1}\n".format(index, i)
                index += 1
            await ctx.send(msg)

    @menu.command()
    async def add(self, ctx, *, args: str):
        self.data["itemList"].append(args)

        self.writeMenu()

        await ctx.message.add_reaction("☑")

    @add.error
    async def add_err(self, error, ctx):
        await errMsg(self.bot, ctx, "Missing menu item to add!")

    @menu.command()
    async def remove(self, ctx, args: str):
        if not args.isdigit():
            await errMsg(self.bot, ctx, "Item to remove needs to be a number between 1 and {}".format(
                            len(self.data["itemList"])))
            return

        if int(args) > len(self.data["itemList"]):
            await errMsg(self.bot, ctx, "Item to remove needs to be a number between 1 and {}".format(
                            len(self.data["itemList"])))
            return

        self.data["itemList"].remove(self.data["itemList"][int(args)-1])

        self.writeMenu()
        await ctx.message.add_reaction("☑")

    @remove.error
    async def remove_err(self, error, ctx):
        await errMsg(self.bot, ctx, "Missing Item #!\nItem to remove needs to be a number between 1 and {}".format(
                            len(self.data["itemList"])))
