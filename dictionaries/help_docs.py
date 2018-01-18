from .IDs import *

help_default='''```asciidoc
Official Squid Squad Bot
Help Commands:
!help
	- Displays this message
!help auto
	- Lists all automatic tasks 
!help cmds
	- Lists all Bot commands
!help music
	- Lists all music commands
!help react
	- Lists all reaction commands
!help squidcoins
	- Lists commands for our crypto currency
```'''

help_auto='''```asciidoc
Bot listens for these words in all messages:
bet
	- B.E.T
brb
	- Reacts with :JesseBRB:
do you know the way
	- The path of the devil
mock
	- dOn'T mOcK mE
snow | tahoe
	- You little snowflake
taco
	- Reacts with taco
taco bravo
	- Gives urgent PSA warning
ww@
	- Try asking again

Bot listens for game names/phrases and reacts with proper emote(s):
aram
destiny
league
overwatch
pubg
raid | prestige | lair
vr chat
```'''

help_commands='''```asciidoc
!carjesse
	- Use it when Car Jesse appears
!conch
	- All Hail the Magic Conch!
!crypto X
	- Ride the crypto coaster (Powered by coinmarketcap)
!emojiparty
	- Reacts with up to 20 random emotes
!lootbox
	- Open a Destiny 2 Legendary Engram and roll a weapon
!magic8
	- Ask the Magic 8-ball anything
!poll "A" "B" "C" ... "Z"
	- Create a quick strawpoll (Powered by StrawPoll)
!qotd
	-Displays Quote of the Day (Powered by quotes.rest)
!timer
	- Say "timer X" for an X minute timer up to 60m
!unfair
	- Let Jesse know he's unfair!
!yesno
	- Yes or No
```'''

help_music='''```asciidoc
!music <command>

Command list:
join <channel>
	- Makes the Bot join a specific voice channel
joinme
	- Makes the Bot join your current voice channel
play <URL>
	- Adds a song to the Queue, accepts YouTube URLs
volume <amount>
	- Set the Bot's volume, out of 100
pause
	- Pauses music
resume
	- Resumes music
stop
	- Kicks Bot out of Voice Channel and clears Queue
skip
	- Skips current song, needs 3 votes to skip
playing
	- Shows info about current song
```'''

help_react='''```asciidoc
Bot will add reaction to the previous message

!react arguments:
ls
	- Shows this list
boi
	- Take a deep breath
nsfl/nsfw
	- Rule 34 or something
waiting
	- RIP Net Neutrality
```'''

help_squidcoin='''```asciidoc
Bot keeps track of the Squidcoin currency!

1) 1 squidcoin is available at a time
2) Coins are claimed through !squidcoin getcoin
3) The next Squidcoin is generated 1 - 15 minutes after the previous coin was claimed

!squidcoin arguments:
getcoin:
	- Adds 1 coin to your wallet if 1 coin is available
ranking:
	- Displays how many coins everyone on the server has
wallet:
	- Shows how many Squidcoins you own

```'''
