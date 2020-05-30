import json
import os

version = "5.0.0"

def init():
    # Define Production variable
    global PROD
    if "prodbot" in os.path.dirname(os.path.realpath(__file__)):
        PROD = 1
    else:
        PROD = 0

    # Get Token
    global TOKEN
    token_data = json.load(open('tokens.json'))
    if PROD:
        TOKEN = token_data["ProdToken"]
    else:
        TOKEN = token_data["TestToken"]
