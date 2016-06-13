"""Write information about dpaste.com as json to stdout."""

import requests

data = requests.get('http://dpaste.com/api/v2/syntax-choices/').json()
data = {value: key for key, value in data.items()}

print('{')
for key in sorted(data.keys(), key=str.lower):
    print('    ', end='')
    print(repr(key), repr(data[key]), sep=': ', end=',')
    print()
print('}')
