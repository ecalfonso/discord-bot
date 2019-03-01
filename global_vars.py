import json
import os

from functions import *

version = "4.1.3"

def init():
    # Define Production variable
    global PROD
    if "prodbot" in os.path.dirname(os.path.realpath(__file__)):
        PROD = 1
    else:
        PROD = 0

    # Get Token
    global TOKEN
    token_data = readJson("tokens.json")
    if PROD:
        TOKEN = token_data["ProdToken"]
    else:
        TOKEN = token_data["TestToken"]
