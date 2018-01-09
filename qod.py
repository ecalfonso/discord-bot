import urllib.request
import json

qod_filename = 'qod.json'
url = 'http://quotes.rest/qod.json'
response = urllib.request.urlopen(url)
data = json.load(response)

outfile = open(qod_filename, 'w')
json.dump(data, outfile)
outfile.close()
