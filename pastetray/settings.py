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

"""Setting manager for PasteTray.

There's also Gio.Settings, but distributing an application that uses it
with Python's setuptools would be difficult.
"""

import configparser
import os

from gi.repository import Gtk, Gdk, Pango
from pkg_resources import resource_string

from pastetray import _, filepaths


_USER_CONFIG = os.path.join(filepaths.user_config_dir, 'pastetray.conf')


class _ConfigParser(configparser.ConfigParser):
    """Configuration file parser with more features.

    This is a separate class because configparser.ConfigParser doesn't
    take a converters keyword argument in Python versions older than
    3.5, and the converters keyword argument doesn't make setters.
    """

    def __init__(self, **kwargs):
        types = kwargs.pop('types', [])
        configparser.ConfigParser.__init__(self, **kwargs)
        for name, setter, getter in types:
            self._add_setter(name, setter)
            self._add_getter(name, getter)

    def _add_setter(self, name, converter):
        def setter(section, key, value):
            self[section][key] = str(converter(value))
        setattr(self, 'set_' + name, setter)

    def _add_getter(self, name, converter):
        def getter(section, key, **kwargs):
            try:
                return converter(self[section][key])
            except KeyError as e:
                if 'fallback' in kwargs.keys():
                    return kwargs['fallback']
                raise e
        setattr(self, 'get_' + name, getter)


def _bool_setter(boolean):
    """Set a Boolean value."""
    return repr(bool(boolean)).lower()


def _bool_getter(string):
    """Get a Boolean value."""
    return configparser.ConfigParser.BOOLEAN_STATES[string]


def _rgba_getter(string):
    """Get a Gdk.RGBA."""
    rgba = Gdk.RGBA()
    rgba.parse(string)
    return rgba


settings = _ConfigParser(
    dict_type=dict,         # No need for ordering.
    interpolation=None,     # Allow % in values.
    types=[
        # (name, setter, getter),
        ('string', str, str),
        ('bool', _bool_setter, _bool_getter),
        ('int', int, int),
        ('float', float, float),
        ('font', Pango.FontDescription.to_string, Pango.FontDescription),
        ('rgba', Gdk.RGBA.to_string, _rgba_getter),
    ]
)


def load():
    """Load configuration files."""
    defaults = resource_string('pastetray', 'default-settings.conf')
    settings.read_string(defaults.decode('utf-8'))
    settings.read([_USER_CONFIG])


def save():
    """Save to the user-wide configuration files."""
    with open(_USER_CONFIG, 'w') as f:
        print("# Configuartion file for PasteTray.", file=f)
        settings.write(f)


class _PairGrid(Gtk.Grid):
    """A grid for using pairs of items."""

    def __init__(self, **kwargs):
        """Initialize the grid."""
        Gtk.Grid.__init__(self, **kwargs)
        self._y = 0

    def add_single(self, item):
        """Add item to the grid."""
        self.attach(item, 0, self._y, 2, 1)

    def add_pair(self, label, item):
        """Add a label-item pair."""
        label = Gtk.Label(label)
        label.set_hexpand(True)
        self.attach(label, 0, self._y, 1, 1)
        self.attach(item, 1, self._y, 1, 1)
        self._y += 1


class SettingDialog(Gtk.Dialog):
    """Dialog for changing settings."""

    def __init__(self):
        """Initialize the setting dialog."""
        Gtk.Dialog.__init__(self, _("Preferences"))
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        grid = self._make_grid_in_frame(_("New paste window"))

        modes = (
            _("No wrapping"),           # Gtk.WrapMode.NONE == 0
            _("Characters"),            # Gtk.WrapMode.CHAR == 1
            _("Words"),                 # Gtk.WrapMode.WORD == 2
            _("Words and characters"),  # Gtk.WrapMode.WORD_CHAR == 3
        )
        combo = Gtk.ComboBoxText()
        for mode in modes:
            combo.append_text(mode)
        combo.set_active(settings.get_int('General', 'new_paste_wrap'))
        combo.connect('changed', self._on_wrap_changed)
        grid.add_pair(_("Text wrapping"), combo)

        button = Gtk.FontButton()
        button.set_font_name(settings.get_string('General', 'new_paste_font'))
        button.connect('font-set', self._on_font_changed)
        grid.add_pair(_("Font"), button)

        self.get_content_area().show_all()

    def _make_grid_in_frame(self, label):
        """Make and return a _PairGrid in a frame."""
        frame = Gtk.Frame()
        frame.set_label(label)
        self.get_content_area().add(frame)

        pairgrid = _PairGrid()
        frame.add(pairgrid)
        return pairgrid

    def _on_wrap_changed(self, combo):
        """Change wrap mode."""
        settings.set_int('General', 'new_paste_wrap', combo.get_active())

    def _on_font_changed(self, fontbutton):
        """Change font."""
        settings.set_string('General', 'new_paste_font',
                            fontbutton.get_font_name())
