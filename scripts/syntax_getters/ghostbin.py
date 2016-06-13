"""Write information about ghostbin.com as json to stdout."""

import requests

data = {}
for section in requests.get('https://ghostbin.com/languages.json').json():
    for language in section['languages']:
        data[language['name']] = language['id']

print('{')
for key in sorted(data.keys(), key=str.lower):
    print('    ', end='')
    print(repr(key), repr(data[key]), sep=': ', end=',')
    print()
print('}')
