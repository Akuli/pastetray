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

"""The application indicator/tray icon."""

from gi.repository import Gtk, Gdk

from pastetray import trayicon_menu

try:
    from gi.repository import AppIndicator3     # NOQA
except ImportError:
    # Gtk.StatusIcon is deprecated in new versions of GTK+.
    if not hasattr(Gtk, 'StatusIcon'):
        raise ImportError("AppIndicator3 is not installed and Gtk.StatusIcon "
                          "is deprecated in the current version of GTK+")
    print("AppIndicator3 is not installed, Gtk.StatusIcon "
          "will be used instead.")
    AppIndicator3 = None

_menu = Gtk.Menu()


def _on_click(statusicon, button, time):
    """User clicks the statusicon."""
    _menu.popup(
        None, None, Gtk.StatusIcon.position_menu,
        statusicon, button, time or Gtk.get_current_event_time(),
    )


def update():
    """Update the menu."""
    for item in _menu.get_children():
        # For some reason, this makes weird error messages sometimes.
        _menu.remove(item)
    trayicon_menu.add_menu_content(_menu)
    _menu.show_all()


def load():
    """Load the trayicon."""
    global _trayicon
    if AppIndicator3 is None:
        _trayicon = Gtk.StatusIcon()
        _trayicon.set_from_icon_name(Gtk.STOCK_PASTE)
        _trayicon.connect('popup-menu', _on_click)
        _trayicon.connect('activate', _on_click, Gdk.BUTTON_PRIMARY, False)
    else:
        _trayicon = AppIndicator3.Indicator.new(
            'pastetray', Gtk.STOCK_PASTE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        _trayicon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        _trayicon.set_menu(_menu)
