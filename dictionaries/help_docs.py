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
!help quote
	- Lists all quote commands
!help react
	- Lists all reaction commands
!help remindme
	- Lists commands for reminders
!hepl topic
	- [Admins Only] Allows user to change current channel's topic
!help wmark
	- Lists commands for adding watermarks to images
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
!drjesse
	- When the Doctor is in
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
!qotd
	- Displays Quote of the Day (Powered by quotes.rest)
!react X
	- See !help react
!remindme
	- Remind yourself Your Message in X minutes/hours/days/weeks... etc
!salt
	- Down here, salt is a way of life
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

!pubg rpg @person1 @p2 @p3 @p4
	Bot selects who will be DPS, Healer, Tank and Support

!pubg stats PUBG_USERNAME
	Uses the PUBG API to get data for up to the last 3 matches made by this person
	https://developer.playbattlegrounds.com
```'''

help_quote='''```
Immortalize what server members say
!quote save @person Something They Said
	- Saves their quote to the database
!quote show @person
	- Lists all quotes made by @person
!quote random @person
	- Displays random quote by @person
!quote remove @person NUMBER
	- Deletes a quote for @person, get NUMBER from "!quote show @person"
```'''

help_react='''```asciidoc
Bot will add reaction to the previous message

!react arguments:
boi
	- Take a deep breath
deletethis
	- Delete this, nephew
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

help_topic='''```
[Admins Only] Allows user to change/clear current channels' topic

Usage:
!topic "Enter topic text here"

!topic clear
	- Clears current channel's topic
```'''

help_wmark='''```
Post an image to a chat channel or DM the Bot and put the command in the "Add a comment"
!wmark LOGO

Available logos:
	brazzers
```'''
