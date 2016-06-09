"""Information about this program."""
from gettext import gettext as _

# Information about authors. Add your name here if you've helped with
# making this program but your name is not here yet.
AUTHORS = ["Akuli"]
TRANSLATORS = {
    _("Finnish"): "Akuli",
}

# General information.
SHORT_DESC = _("a simple application for using online pastebins")
LONG_DESC = _("This program displays a paste icon in the system tray. \
The tray icon can be clicked and new pastes to online pastebins can be \
easily made.")
VERSION = '1.0-beta'
KEYWORDS = ["pastebin", "Gtk+3"]

# The setup.py needs to do other checks too, because not all
# dependencies can be installed with pip.
PIP_DEPENDS = ['appdirs', 'psutil', 'requests']
# This list is more complete.
DEBIAN_DEPENDS = ['gir1.2-gtk-3.0', 'gir1.2-appindicator3-0.1',
                  'python3-gi', 'python3-appdirs', 'python3-psutil',
                  'python3-requests']
