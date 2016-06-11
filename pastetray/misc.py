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

"""Miscellaneous things."""

import contextlib
import functools
import webbrowser

from gi.repository import Gtk, GdkPixbuf
from pkg_resources import resource_filename, resource_string

import pastetray


def ignore_first(func):
    """Return a function that ignores the first argument and calls func.

    TypeError will be raised if no arguments are given.
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


def show_help():
    """Open the help page in the web browser."""
    # Here resource_filename must be used because web browsers open
    # URL's and filenames.
    webbrowser.open(resource_filename('pastetray', 'help.html'))


def show_about():
    """Display an about dialog."""
    # Load the license and paste icon.
    license = resource_string('pastetray', 'LICENSE')
    logo = Gtk.IconTheme.get_default().lookup_icon(
        Gtk.STOCK_PASTE, Gtk.IconSize.DIALOG,
        Gtk.IconLookupFlags.NO_SVG,
    )

    # Display a dialog.
    dialog = Gtk.AboutDialog()
    dialog.set_program_name("PasteTray")
    dialog.set_version(pastetray.VERSION)
    dialog.set_comments(pastetray.SHORT_DESC[0].upper() +
                        pastetray.SHORT_DESC[1:] + ".")
    dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(logo.get_filename()))
    dialog.set_license(license.decode('utf-8'))
    dialog.set_resizable(True)  # the license is a bit long
    dialog.set_authors(pastetray.AUTHORS)
    dialog.set_translator_credits(
        '\n'.join(': '.join(item) for item in pastetray.TRANSLATORS.items())
    )
    dialog.run()
    dialog.destroy()
