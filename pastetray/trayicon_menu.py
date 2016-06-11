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

"""A menu for trayicon.py.

This is in a separate file because new_paste.py imports trayicon.py, and
otherwise trayicon.py would need to import new_paste.py also.
"""

import webbrowser

from gi.repository import Gtk

from pastetray import _, backend, misc, new_paste, preference_editor


def add_menu_content(menu):
    """Add the content to a trayicon menu."""
    if hasattr(Gtk, 'ImageMenuItem'):
        # Gtk.ImageMenuItem is not deprecated.
        new_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_NEW)
        pref_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PREFERENCES)
        help_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_HELP)
        about_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT)
        quit_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT)
    else:
        new_item = Gtk.MenuItem(_("New paste"))
        pref_item = Gtk.MenuItem(_("Preferences"))
        help_item = Gtk.MenuItem(_("Help"))
        about_item = Gtk.MenuItem(_("About"))
        quit_item = Gtk.MenuItem(_("Quit"))
    new_item.connect('activate', misc.ignore_first(new_paste.new_paste))
    pref_item.connect('activate', misc.ignore_first(preference_editor.run))
    help_item.connect('activate', misc.ignore_first(misc.show_help))
    about_item.connect('activate', misc.ignore_first(misc.show_about))
    quit_item.connect('activate', Gtk.main_quit)

    menu.add(new_item)
    menu.add(Gtk.SeparatorMenuItem())
    if backend.recent_pastes:
        for number, url in enumerate(backend.recent_pastes, start=1):
            item = Gtk.MenuItem('{}. {}'.format(number, url))
            item.connect('activate', misc.ignore_first(webbrowser.open), url)
            menu.add(item)
    else:
        item = Gtk.MenuItem(_("(no pastes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        menu.add(item)
    menu.add(Gtk.SeparatorMenuItem())
    menu.add(pref_item)
    menu.add(help_item)
    menu.add(about_item)
    menu.add(quit_item)
