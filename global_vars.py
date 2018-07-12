import json
import os
from pathlib import Path

version = '3.8.16'

def init():
	global PROD
	if 'prodbot' in os.path.dirname(os.path.realpath(__file__)):
		PROD = 1
	else:
		PROD = 0

	global nicknames_file
	nicknames_file = '../data/nicknames.data'

	global quotes_file
	global quotes_data
	quotes_file = '../data/quotes.data'
	if Path(quotes_file).is_file():
		quotes_data = json.load(open(quotes_file))
	else:
		print('Unable to load quotes_file!')

	global remindme_file
	global remindme_data
	remindme_file = '../data/remindme.data'
	if Path(remindme_file).is_file():
		remindme_data = json.load(open(remindme_file))
	else:
		print('Unable to load quotes_file!')
