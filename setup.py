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

# flake8: noqa

import sys

import pastetray


class Check:
    """Abort if an exception occurs.

    Use the instances as context managers.
    """

    def __init__(self, lib, custom_msg=False):
        self._lib = lib
        self._custom_msg = custom_msg

    def __enter__(self):
        pass

    def __exit__(self, *args):
        if args != (None, None, None):
            if self._custom_msg:
                sys.exit(self._custom_msg)
            sys.exit("{} is not installed".format(self._lib))


with Check("This program requires Python 3.2 or newer.", custom_msg=True):
    assert sys.version_info[:2] >= (3, 2)

with Check("setuptools"):
    from setuptools import setup

with Check("gi"):
    import gi

with Check("GTK+ for gi"):
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk

with Check("AppIndicator3 or GTK+ with GtkStatusIcon"):
    if not hasattr(Gtk, 'StatusIcon'):
        from gi.repository import AppIndicator3


setup(
    name='pastetray',
    version=pastetray.VERSION,
    description=pastetray.SHORT_DESC,
    long_description=pastetray.LONG_DESC,
    url=pastetray.URL,
    author=', '.join(pastetray.AUTHORS),
    license='MIT',
    keywords=' '.join(i.replace(' ', '') for i in pastetray.KEYWORDS),
    zip_safe=True,
    install_requires=pastetray.PIP_DEPENDS,
    packages=['pastetray', 'pastetray.pastebins'],
    package_data={'pastetray': ['LICENSE', 'default_settings.conf',
                                '*.glade', 'locale/*.mo', 'doc/*']},
    entry_points={'gui_scripts': ['pastetray = pastetray.__main__:main']},
)
