"""This file downloads a language list from ghostbin.com and writes it
to stdout"""

import json
import requests
import textwrap

data = requests.get('https://ghostbin.com/languages.json').json()
result = {}
for section in data:
    for language in section['languages']:
        result[language['name']] = language['id']

print("ghostbin.com api languages:")
for item in sorted(result.items(), key=lambda s: str(s).lower()):
    print('"%s": "%s",' % item)
