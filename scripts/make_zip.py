#!/usr/bin/env python3

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

"""Make a PasteTray zipfile."""

import os
import shutil
import tempfile
import zipfile

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(here))

for root, dirs, files in os.walk(os.path.curdir):
    for d in dirs:
        if d == '__pycache__':
            shutil.rmtree(os.path.join(root, d))

# TODO: Use os.walk and write directly to the final file instead of
# making a temporary zipfile and copying its content.
tempzip = tempfile.NamedTemporaryFile('rb')
try:
    zipfile.main(['-c', tempzip.name, 'LICENSE', '__main__.py',
                  'pastetray', 'README.md', 'WRITING_PASTEBINS.md'])
except SystemExit:
    pass

with open('pastetray.pyz', 'wb') as result:
    result.write(b'#!/usr/bin/env python3\n')
    with tempzip:
        shutil.copyfileobj(tempzip, result)
