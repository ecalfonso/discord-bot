'''
Definitions for prasing/processing incoming Discord messages
'''
import aiohttp

from functions import *

async def msg_react(bot, msg):
    message = msg.content.lower().split()
    for i, m in enumerate(message):
        if "bet" == m:
            rx = ["🇧", "🇪", "🇹"]
            await reactToMsg(bot, msg, rx)

        if "brb" in m and not m.startswith(":"):
            if msg.author.id == msg.server.owner.id:
                await postRandomPic(bot, msg, "../images/jessebrb/")
            else:
                await bot.add_reaction(msg, "JesseBRB:334162261922807808")

        if "mock" in m:
            mock_str = ""
            flip = 0
            for l in msg.content.lower():
                if l.isalpha():
                    if flip == 0:
                        mock_str += l
                        flip = 1
                    else:
                        mock_str += l.upper()
                        flip = 0
                else:
                    mock_str += l
            print(mock_str)
            await bot.send_message(msg.channel, "<@{0}>: {1}".format(msg.author.id, mock_str))

        if "snow" in m or "tahoe" == m:
            await bot.add_reaction(msg, "❄")

        if "squid" in m:
            await bot.add_reaction(msg, "🦑")

        if "taco" in m:
            if i < len(message) - 1:
                if "bravo" == message[i + 1]:
                    await bot.add_reaction(msg, "🚫")
                    await bot.send_file(msg.channel,
                        "../images/HereLiesLeon.png",
                        content="PSA by <@{0}>: AVOID TACO BRAVO".format(IDs["Leon"]))
            else:
                await bot.add_reaction(msg, "🌮")

        if "tfti" in m:
            rx = ["tfti_t1:401227546504724491", "tfti_f:401227559653867531", 
                    "tfti_t2:401227576024104960", "tfti_i:401227586039971840"]
            await reactToMsg(bot, msg, rx)

        if "ww@" in m:
            rx = ["wwat_w_1:400486976454787083", "wwat_w_2:400487029634498561",
                    "wwat_at:400487716892180498"]
            await reactToMsg(bot, msg, rx)
            if msg.author.id == IDs["Chris"] or msg.author.id == IDs["Eduard"]:
                print("DBG: In ww@\n")
                if random.randint(1,256) == 1:
                    await bot.send_file(msg.channel, "../images/here/ww@.jpg")
                

        if "(╯°□°）╯︵ ┻━┻" in m:
            await bot.send_message(msg.channel, "┬─┬ ノ( ゜-゜ノ) - Calm down <@{0}>".format(msg.author.id))

        #
        # Reactions based on game titles
        #
        if "city" in m:
            await reactToMsg(bot, msg, "🏙")

        if "cowboy" in m or "howdy" in m:
            rx = ["🇭","🇴","🇼","🇩","🇾"]
            await reactToMsg(bot, msg, rx)

        if "fortnite" in m or "forknite" in m or "fortknife" in m or "forkknife" in m:
            await reactToMsg(bot, msg, "🍴")

        if "halo" in m:
            rx = ["🇭","🇦","🇱","🇴"]
            await reactToMsg(bot, msg, rx)

        if "noon" in m:
            await reactToMsg(bot, msg, "🕛")

        if "pubg" in m:
            rx = ["🇵", "🇺", "🇧", "🇬", "❔"]
            await reactToMsg(bot, msg, rx)

        if "slap" in m:
            await reactToMsg(bot, msg, "🖐")

        if "spoon" in m:
            await reactToMsg(bot, msg, "🥄")

        if 'store.steampowered.com' in m and 'agecheck' not in m:
            await humblebundle_check(bot, msg, m)

async def humblebundle_check(bot, msg, m):
    humble_url = 'https://www.humblebundle.com/store/'
    if m[-1] == '/':
        game = m.split('/')[-2].replace('_', '-')
    else:
        game = m.split('/')[-1].replace('_', '-')

    # Check to see that Humble Bundle link doesn't 404
    async with aiohttp.get(humble_url + game) as resp:
        if resp.status == 200:
            await bot.send_message(msg.channel, 'Consider getting this game through Humble Bundle!\n{}'.format(
                humble_url + game))
