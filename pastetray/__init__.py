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

"""Simple program for using online pastebins.

This file sets up many things, such as internationalization, GTK+,
threading and Ctrl+C interrupting.
"""

import gettext
import locale
import signal

import gi
from gi.repository import GObject
from pkg_resources import resource_stream


# Internationalization.
def _get_translation():
    """Return a gettext translation."""
    lang = locale.getdefaultlocale()[0]
    # Maybe LANG is C and lang is None?
    while lang is not None:
        try:
            path = 'locale/{}.mo'.format(lang)
            with resource_stream('pastetray', path) as fp:
                return gettext.GNUTranslations(fp)
        except OSError:
            if '_' in lang:
                # Remove the last part and keep going.
                lang = lang.rpartition('_')[0]
            else:
                # Give up.
                lang = None
    return gettext.NullTranslations()

_ = _get_translation().gettext
gi.require_version('Gtk', '3.0')
GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)


# Add your name here if you've helped with making this program but your
# name is not here yet.
AUTHORS = ["Akuli"]
TRANSLATORS = {
    _("Finnish"): "Akuli",
}

# General information. Only string literals are passed to _() to make
# sure pygettext will work properly.
SHORT_DESC = "a simple application for using online pastebins"
SHORT_DESC_TRANS = _("a simple application for using online pastebins")
LONG_DESC = _("This program displays a paste icon in the system tray. "
              "The tray icon can be clicked and new pastes to online "
              "pastebins can be easily made.")

URL = 'https://github.com/Akuli/pastetray/'
VERSION = '1.0-beta'
KEYWORDS = ["pastebin", "Gtk+3"]
USER_AGENT = "PasteTray/" + VERSION

# The setup.py needs to do other checks too because some dependencies
# cannot be installed with pip.
PIP_DEPENDS = ['appdirs', 'lockfile', 'requests']
# This list is more complete, but there's no python3-lockfile yet.
DEBIAN_DEPENDS = ['python3-appdirs', 'python3-lockfile',
                  'python3-pkg_resources', 'python3-requests', 'python3-gi',
                  'gir1.2-gtk-3.0', 'gir1.2-appindicator3-0.1']
