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

"""Make other icons from big.png using imagemagick."""

import os
import shutil
import subprocess
import sys

SIZES = [16, 22, 24, 32, 48, 64, 128, 256]


def main():
    """Run the script."""
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(here), 'pastetray', 'icons'))

    for size in SIZES:
        size = '{0}x{0}'.format(size)
        shutil.copy('big.png', size + '.png')
        subprocess.check_call(['mogrify', '-resize', size, size + '.png'])

    sys.exit()


if __name__ == '__main__':
    main()
