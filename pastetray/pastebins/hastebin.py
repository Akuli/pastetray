# Copyright (c) 2016 Akuli, SquishyStrawberry

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

"""This is a hastebin file for PasteTray.

Thanks to SquishyStrawberry <https://github.com/SquishyStrawberry/> for
making the original pasting script. This file is my (Akuli's) version of it.
"""

import requests

name = 'hastebin'
url = 'http://hastebin.com/'
expiry_days = [30]

paste_args = ['content', 'expiry_days']


def paste(content, expiry_days):
    """Make a paste to hastebin.com."""
    response = requests.post('http://hastebin.com/documents/', data=content)
    response.raise_for_status()
    return 'http://hastebin.com/' + response.json()['key']
