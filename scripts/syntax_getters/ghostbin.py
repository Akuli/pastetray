"""Write information about ghostbin.com as json to stdout."""

import json
import sys

import requests

data = {}
for section in requests.get('https://ghostbin.com/languages.json').json():
    for language in section['languages']:
        data[language['name']] = language['id']

json.dump(data, sys.stdout, indent=4)
print()
