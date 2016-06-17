"""Write information about dpaste.com as json to stdout."""

import json
import sys

import requests

data = requests.get('http://dpaste.com/api/v2/syntax-choices/').json()
data = {value: key for key, value in data.items()}

json.dump(data, sys.stdout, indent=4)
print()
