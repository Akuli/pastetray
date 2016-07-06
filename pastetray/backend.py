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
import re
import threading

from pastetray import filepaths
from pastetray.filepaths import resource_listdir


pastebins = {}    # These are name: module pairs.
recent_pastes = collections.deque(maxlen=10)

_RECENT_PASTES_PATH = os.path.join(filepaths.user_config_dir,
                                   'recent_pastes.txt')


class PastebinError(Exception):
    """This is raised when a pastebin script is causing issues."""


def load():
    """Load pastebins and recent pastes."""
    pastebins.clear()
    for name in resource_listdir('pastetray', 'pastebins'):
        if not re.search(r'^[a-z][a-z_]*\.py$', name):
            # Not a valid PasteTray pastebin module name.
            continue
        modulename = 'pastetray.pastebins.' + os.path.splitext(name)[0]
        module = importlib.import_module(modulename)
        if module.name in pastebins:
            raise PastebinError("there are two pastebins named {!r}"
                                .format(module.name))
        pastebins[module.name] = module
    if not pastebins:
        raise PastebinError("no pastebins found")

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


class PastingThread(threading.Thread):
    """Thread for pasting.

    When the pasting is done the thread's .is_alive() method will return
    False and the thread will have two new attributes, success and
    response. success is True if the pasting succeeded and otherwise
    False, and response will be the paste's URL or an error message.
    """

    def __init__(self, pastebin, getters, **kwargs):
        """Initialize the thread.

        The getters argument should be a dictionary of possible pastebin
        paste_args and functions or methods for getting values for them.
        """
        threading.Thread.__init__(self, **kwargs)
        self._pastebin = pastebin
        self._kwargs = {arg: getters[arg]() for arg in pastebin.paste_args}

    def run(self):
        """Call the pastebin's .paste() method."""
        try:
            self.response = str(self._pastebin.paste(**self._kwargs))
            self.success = True
        except Exception as e:
            self.response = "{.__name__}: {}".format(type(e), e)
            self.success = False
