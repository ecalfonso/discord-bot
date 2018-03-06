version = '3.5.11'

def init():
	global squidcoin_data
	global squidcoin_file
	global squidcoin_ready

	squidcoin_data = {}
	squidcoin_file = '../squidcoin.base'
	squidcoin_ready = 1

	global nicknames_file
	nicknames_file = '../data/nicknames.data'
