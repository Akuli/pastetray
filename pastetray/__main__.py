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

"""Run the program."""

import argparse
import os
import sys

import filelock
from gi.repository import Gtk

from pastetray import backend, filepaths, preferences, trayicon


def main(args=None):
    """Run the program."""
    parser = argparse.ArgumentParser()
    parser.parse_args(args)

    lock = filelock.FileLock(os.path.join(filepaths.user_cache_dir, 'lock'))
    try:
        with lock.acquire(timeout=0):
            preferences.load()
            backend.load()
            trayicon.load()
            trayicon.update()
            Gtk.main()
    except filelock.Timeout:
        dialog = Gtk.MessageDialog(
            # Setting None as the parent is usually a bad idea, but in
            # this case there is no parent window.
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            _("{} is already running.").format("PasteTray"),
            title="PasteTray",
        )
        dialog.run()
        dialog.destroy()
    finally:
        preferences.save()
        backend.unload()

    # This function is not meant to be ran multiple times.
    sys.exit()


if __name__ == '__main__':
    main()
