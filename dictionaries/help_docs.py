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
!help remindme
	- Lists commands for reminders
!help squidcoin
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
tfti
	- Thanks
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
!cleanup
	- Deletes last 50 Bot messages and 50 User commands
!conch
	- All Hail the Magic Conch!
!crypto X
	- Ride the crypto coaster (Powered by coinmarketcap)
!emojiparty X
	- Specify a Message ID 'X' and bot will add up to 20 random server emotes
!food
	- Bot recommends a random food recipe for you
!lootbox
	- Open a Destiny 2 Legendary Engram and roll a weapon
!magic8
	- Ask the Magic 8-ball anything
!music
	- See !help music
!poll "A" "B" "C" ... "Z"
	- Create a quick strawpoll (Powered by StrawPoll)
!qotd
	- Displays Quote of the Day (Powered by quotes.rest)
!react X
	- See !help react
!remindme
	- Remind yourself Your Message in X minutes/hours/days/weeks... etc
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

help_pubg='''```asciidoc
Tells you where to drop for the requested map
!pubg map1|map2

map1 - Erangel
map2 - Miramar
```'''

help_react='''```asciidoc
Bot will add reaction to the previous message

!react arguments:
boi
	- Take a deep breath
nsfl/nsfw
	- Rule 34 or something
waiting
	- RIP Net Neutrality
```'''

help_remindme='''```asciidoc
Bot will PM you a scheduled message

!remindme arguments:
after AMOUNT MODIFIER The Rest of the Message
	AMOUNT
		- A reasonable number
	MODIFIER
		- minutes|hours|days|months|years
		- Use !timer for reminders in minutes

showme
	- bot PMs you a list of all your scheduled messages

example:
!remindme after 2 days Hey did you remember to forget?

Everything past the first 2 arguments is part of your reminder message
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
tip @person X:
	- Tips X coins from your balance to @person
wallet:
	- Shows how many Squidcoins you own

```'''
