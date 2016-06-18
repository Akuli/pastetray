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

"""Utilities for managing trayicon_backend.py.

This file also contains the menuitems and some of the commands they run.
"""

import shutil
import tempfile
from urllib.request import pathname2url
import webbrowser

from gi.repository import Gtk, GdkPixbuf
from pkg_resources import resource_filename, resource_stream, resource_string

import pastetray
from pastetray import (_, backend, new_paste, preference_editor,
                       trayicon_backend)


def clear_recent_pastes(widget=None):
    """Clear the recent paste list."""
    dialog = Gtk.MessageDialog(
        # Setting None as the transient parent is not recommended, but
        # this application has no main window.
        None, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO,
        _("Are you sure you want to clear the recent paste list?"),
    )
    dialog.set_title(_("Clear recent pastes"))
    dialog.format_secondary_text(_("This cannot be undone."))
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.YES:
        backend.recent_pastes.clear()
        update()


def show_help(widget=None):
    """Open the help page in the web browser."""
    try:
        filename = resource_filename('pastetray', 'help.html')
    except NotImplementedError:
        # Running from a zipfile.
        with resource_stream('pastetray', 'help.html') as src:
            with tempfile.NamedTemporaryFile('wb') as dst:
                filename = dst.name
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


load = trayicon_backend.load


# By making the menuitems now they don't need to be remade every time
# the menu is updated.
def _menuitems():
    data = [
        (Gtk.STOCK_NEW, _("New paste"), new_paste.new_paste),
        (Gtk.STOCK_CLEAR, _("Clear recent pastes"), clear_recent_pastes),
        (Gtk.STOCK_PREFERENCES, _("Preferences"), preference_editor.run),
        (Gtk.STOCK_HELP, _("Help"), show_help),
        (Gtk.STOCK_ABOUT, _("About"), show_about),
        (Gtk.STOCK_QUIT, _("Quit"), Gtk.main_quit),
    ]

    # Check if Gtk.ImageMenuItem is deprecated.
    not_deprecated = hasattr(Gtk, 'ImageMenuItem')

    for stock, label, command in data:
        if not_deprecated:
            image = Gtk.Image.new_from_icon_name(stock, Gtk.IconSize.MENU)
            item = Gtk.ImageMenuItem(label)
            item.set_image(image)
        else:
            item = Gtk.MenuItem(label)
        item.connect('activate', command)
        yield stock, item

_menuitems = dict(_menuitems())


def _on_pasteitem_clicked(widget, url):
    """Open url."""
    webbrowser.open(url)


def update():
    """Update the trayicon."""
    menu = trayicon_backend.menu
    for item in menu.get_children():
        # For some reason, sometimes this makes weird error messages.
        menu.remove(item)

    menu.add(_menuitems[Gtk.STOCK_NEW])
    menu.add(Gtk.SeparatorMenuItem())
    if backend.recent_pastes:
        for number, url in enumerate(backend.recent_pastes, start=1):
            item = Gtk.MenuItem('{}. {}'.format(number, url))
            item.connect('activate', _on_pasteitem_clicked, url)
            menu.add(item)
    else:
        item = Gtk.MenuItem(_("(no pastes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        menu.add(item)
    menu.add(Gtk.SeparatorMenuItem())
    menu.add(_menuitems[Gtk.STOCK_CLEAR])
    menu.add(_menuitems[Gtk.STOCK_PREFERENCES])
    menu.add(_menuitems[Gtk.STOCK_HELP])
    menu.add(_menuitems[Gtk.STOCK_ABOUT])
    menu.add(_menuitems[Gtk.STOCK_QUIT])

    menu.show_all()
