"""This file downloads a language list from dpaste.com and writes it to
stdout"""

import json
import requests
import textwrap

data = requests.get('http://dpaste.com/api/v2/syntax-choices/').json()
result = {value: key for key, value in data.items()}

print("dpaste.com api languages:")
for item in sorted(result.items(), key=lambda s: str(s).lower()):
    print('"%s": "%s",' % item)
