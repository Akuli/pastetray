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

"""Make a PasteTray zipfile.

PasteTray's source code should be in the parent directory, and the zip
will be placed there too.
"""

import os
import shutil
import tempfile
import zipfile

os.chdir(os.path.pardir)

for root, dirs, files in os.walk(os.path.curdir):
    for d in dirs:
        if d == '__pycache__':
            shutil.rmtree(os.path.join(root, d))

# TODO: Use os.walk and write directly to the final file instead of
# making a temporary zipfile and copying its content.
tempzip = os.path.join(tempfile.gettempdir(), 'pastetray-build.zip')
zipfile.main(['-c', tempzip, 'LICENSE', '__main__.py',
              'pastetray', 'README.md'])

with open('pastetray.pyz', 'wb') as dst:
    dst.write(b'#!/usr/bin/env python3\n')
    with open(tempzip, 'rb') as src:
        shutil.copyfileobj(src, dst)
