version = '3.5.11'

def init():
	global nicknames_file
	nicknames_file = '../data/nicknames.data'

	global quotes_file
	global quotes_data
	quotes_file = '../data/quotes.data'
	quotes_data = {}

	global remindme_file
	global remindme_data
	remindme_file = '../data/remindme.data'
	remindme_data = {}

	global squidcoin_data
	global squidcoin_file
	global squidcoin_ready
	squidcoin_data = {}
	squidcoin_file = '../data/squidcoin.base'
	squidcoin_ready = 1
