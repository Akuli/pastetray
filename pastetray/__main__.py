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
import sys

from gi.repository import Gtk

from pastetray import _, backend, functions, lock, preferences, trayicon


def main(args=None):
    """Run the program."""
    parser = argparse.ArgumentParser()
    parser.parse_args(args)

    try:
        with lock.locked():
            preferences.load()
            backend.load()
            trayicon.load()
            functions.update_trayicon()
            Gtk.main()
    except lock.IsLocked:
        dialog = Gtk.MessageDialog(
            # Setting None as the parent is usually a bad idea, but
            # PasteTray has no parent window.
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            _("{} is already running.").format("PasteTray"),
        )
        dialog.set_title("PasteTray")
        dialog.run()
        dialog.destroy()
    finally:
        preferences.save()
        backend.save()

    # This function is not meant to be ran multiple times.
    sys.exit()


if __name__ == '__main__':
    main()
