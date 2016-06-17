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

"""Miscellaneous functions."""

import contextlib
import functools
import os
import tempfile
from urllib.request import pathname2url
import webbrowser

from gi.repository import Gtk, GdkPixbuf
from pkg_resources import (resource_filename, resource_stream,
                           resource_string)

import pastetray
from pastetray import filepaths


def ignore_first(func):
    """Return a function that ignores the first argument and calls func.

    When called, the returned function will call the original func
    without the first argument and return the value it returns. An
    exception is raised when no arguments are given and there's nothing
    to ignore.
    """
    @functools.wraps(func)
    def wrapper(ign, *args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@contextlib.contextmanager
def disconnected(obj, signal, func, *user_data):
    """Disconnect a GObject signal temporarily."""
    obj.disconnect_by_func(func)
    yield
    obj.connect(signal, func, *user_data)


def show_help(widget=None):
    """Open the help page in the web browser."""
    try:
        filename = resource_filename('pastetray', 'help.html')
    except NotImplementedError:
        # Running from a zipfile.
        filename = os.path.join(tempfile.gettempdir(), 'pastetray-help.html')
        with resource_stream('pastetray', 'help.html') as src:
            with open(filename, 'wb') as dst:
                shutil.copyfileobj(src, dst)

    url = 'file://' + pathname2url(filename)

    # On X.Org, webbrowser.open() seems to use xdg-open by default
    # instead of x-www-browser, so HTML files don't always open in a WWW
    # browser. That's why x-www-browser is used when possible.
    try:
        webbrowser.get('x-www-browser').open(url)
    except webbrowser.Error:
        webbrowser.open(url)


def show_about(widget=None):
    """Display an about dialog."""
    license = resource_string('pastetray', 'LICENSE')
    logo = Gtk.IconTheme.get_default().lookup_icon(
        Gtk.STOCK_PASTE, 128,
        Gtk.IconLookupFlags.NO_SVG,
    )

    dialog = Gtk.AboutDialog()
    dialog.set_program_name("PasteTray")
    dialog.set_version(pastetray.VERSION)
    dialog.set_comments(pastetray.SHORT_DESC[0].upper() +
                        pastetray.SHORT_DESC[1:] + ".")
    dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(logo.get_filename()))
    dialog.set_license(license.decode('utf-8'))
    dialog.set_resizable(True)     # The license is a bit long.
    dialog.set_authors(pastetray.AUTHORS)
    dialog.set_translator_credits(
        '\n'.join(': '.join(item) for item in pastetray.TRANSLATORS.items())
    )
    dialog.run()
    dialog.destroy()
