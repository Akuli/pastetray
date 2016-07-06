# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""This is a Paste ofCode file for PasteTray.

The API documentation is here:
  https://developer.github.com/v3/gists/#create-a-gist
"""

import json

import requests

name = 'GitHub Gist'
url = 'https://gist.github.com/'
expiry_days = [-1]

paste_args = ['content', 'title']


def paste(content, title):
    """Make a paste to GitHub Gist."""
    response = requests.post(
        'https://api.github.com/gists',
        data=json.dumps({
            'description': title,
            'public': False,
            'files': {'file.txt': {'content': content}},
        }),
    )
    response.raise_for_status()
    return response.json()['html_url']
