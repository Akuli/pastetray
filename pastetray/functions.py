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

"""Functions for the trayicon."""

import os
import shutil
import tempfile
from urllib.request import pathname2url
import webbrowser

from gi.repository import Gtk, GdkPixbuf
from pkg_resources import (resource_filename, resource_listdir,
                           resource_stream, resource_string)

import pastetray
from pastetray import _, backend, new_paste, preference_editor, trayicon


def make_new_paste(widget=None):
    """Make a new paste."""
    paster = new_paste.Paster(backend.recent_pastes.appendleft,
                              update_trayicon)
    new_paste.pasters.append(paster)


def change_preferences(widget=None):
    """Open window for editing preferences."""
    window = preference_editor.PreferenceWindow()
    window.show_all()


def clear_recent_pastes(widget=None):
    """Clear the recent paste list."""
    if backend.recent_pastes:
        dialog = Gtk.MessageDialog(
            # Setting None as the transient parent is not recommended, but
            # this application has no main window.
            None, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _("Are you sure you want to clear the recent paste list?"),
        )
        dialog.format_secondary_text(_("This cannot be undone."))
    else:
        dialog = Gtk.MessageDialog(
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            _("There are no recent pastes to clear."),
        )
    dialog.set_title(_("Clear recent pastes"))
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.YES:
        backend.recent_pastes.clear()
        update_trayicon()


def show_help_dialog(widget=None):
    """Open the help page in the web browser."""
    try:
        filename = resource_filename('pastetray', 'doc/index.html')
    except NotImplementedError:
        # Running from a zipfile. The whole doc directory needs to be
        # extracted.
        tempdir = os.path.join(tempfile.gettempdir(), 'pastetray-doc')
        if not os.path.isdir(tempdir):
            os.mkdir(tempdir)

        for fname in resource_listdir('pastetray', 'doc'):
            if not fname:
                # Sometimes the list returned by resource_listdir
                # contains empty strings for some reason.
                continue

            dstfile = os.path.join(tempdir, fname)
            if os.path.isfile(dstfile):
                # The help has already been viewed and there's no need
                # to rewrite the file.
                continue

            with resource_stream('pastetray', 'doc/{}'.format(fname)) as src:
                with open(dstfile, 'wb') as dst:
                    shutil.copyfileobj(src, dst)

        filename = os.path.join(tempdir, 'index.html')

    # On X.Org, webbrowser.open() seems to use xdg-open by default
    # instead of x-www-browser, so HTML files don't always open in a WWW
    # browser. That's why x-www-browser is used when possible.
    url = 'file://' + pathname2url(filename)
    try:
        webbrowser.get('x-www-browser').open(url)
    except webbrowser.Error:
        webbrowser.open(url)


# The license is loaded here, because this way PasteTray cannot run
# without being able to display the license.
_license = resource_string('pastetray', 'doc/LICENSE').decode('utf-8')


def show_about_dialog(widget=None):
    """Display an about dialog."""
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
    dialog.set_license(_license)
    dialog.set_resizable(True)     # The license is a bit long.
    dialog.set_authors(pastetray.AUTHORS)
    dialog.set_translator_credits(
        '\n'.join(': '.join(item) for item in pastetray.TRANSLATORS.items())
    )
    dialog.run()
    dialog.destroy()


# By making the menuitems now they don't need to be remade every time
# the menu is updated.
def _menuitems():
    data = [
        (Gtk.STOCK_NEW, _("New paste"), make_new_paste),
        (Gtk.STOCK_CLEAR, _("Clear recent pastes"), clear_recent_pastes),
        (Gtk.STOCK_PREFERENCES, _("Preferences"), change_preferences),
        (Gtk.STOCK_HELP, _("Help"), show_help_dialog),
        (Gtk.STOCK_ABOUT, _("About"), show_about_dialog),
        (Gtk.STOCK_QUIT, _("Quit"), Gtk.main_quit),
    ]

    # Check if Gtk.ImageMenuItem is deprecated.
    not_deprecated = hasattr(Gtk, 'ImageMenuItem')

    for stock, label, func in data:
        if not_deprecated:
            image = Gtk.Image.new_from_icon_name(stock, Gtk.IconSize.MENU)
            item = Gtk.ImageMenuItem(label)
            item.set_image(image)
        else:
            item = Gtk.MenuItem(label)
        item.connect('activate', func)
        yield stock, item

_menuitems = dict(_menuitems())


def update_trayicon(widget=None):
    """Update the trayicon's content."""
    for item in trayicon.menu.get_children():
        # For some reason, sometimes this makes weird error messages.
        trayicon.menu.remove(item)

    trayicon.menu.add(_menuitems[Gtk.STOCK_NEW])
    trayicon.menu.add(Gtk.SeparatorMenuItem())

    if backend.recent_pastes:
        for number, url in enumerate(backend.recent_pastes, start=1):
            item = Gtk.MenuItem('{}. {}'.format(number, url))
            item.connect('activate', lambda i, url=url: webbrowser.open(url))
            trayicon.menu.add(item)
    else:
        item = Gtk.MenuItem(_("(no pastes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        trayicon.menu.add(item)
    trayicon.menu.add(Gtk.SeparatorMenuItem())

    trayicon.menu.add(_menuitems[Gtk.STOCK_CLEAR])
    trayicon.menu.add(_menuitems[Gtk.STOCK_PREFERENCES])
    trayicon.menu.add(_menuitems[Gtk.STOCK_HELP])
    trayicon.menu.add(_menuitems[Gtk.STOCK_ABOUT])
    trayicon.menu.add(_menuitems[Gtk.STOCK_QUIT])

    trayicon.menu.show_all()
