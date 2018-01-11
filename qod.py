import urllib.request
import json

qod_filename = '/home/pi/prodbot/qod.json'
url = 'http://quotes.rest/qod.json'
response = urllib.request.urlopen(url)
data = json.load(response)

outfile = open(qod_filename, 'w')
json.dump(data, outfile)
outfile.close()
