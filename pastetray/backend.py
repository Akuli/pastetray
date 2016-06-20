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

"""Load pastebins and take care of recent pastes."""

import collections
import importlib
import os

from pkg_resources import resource_listdir

from pastetray import filepaths


_RECENT_PASTES_PATH = os.path.join(filepaths.user_config_dir,
                                   'recent_pastes.txt')

pastebins = []
recent_pastes = collections.deque(maxlen=10)


def load():
    """Load pastebins and recent pastes."""
    pastebins.clear()
    for name in resource_listdir('pastetray', 'pastebins'):
        if name.startswith('__') or name.endswith('__'):
            # __init__.py, __pycache__ etc.
            continue
        name, ext = os.path.splitext(name)
        if ext != '.py' or not name.isidentifier():
            continue
        modulename = 'pastetray.pastebins.' + name
        module = importlib.import_module(modulename)
        if module.name in (pb.name for pb in pastebins):
            raise Exception("there are two pastebins named {!r}"
                            .format(module.name))
        pastebins.append(module)

    recent_pastes.clear()
    try:
        with open(_RECENT_PASTES_PATH, 'r') as f:
            recent_pastes.extend(line.strip() for line in f)
    except FileNotFoundError:
        # The file will be created when it's saved.
        pass


def save():
    """Save the list of recent pastes."""
    with open(_RECENT_PASTES_PATH, 'w') as f:
        for url in recent_pastes:
            print(url, file=f)
