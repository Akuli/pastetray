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

"""Preference manager for PasteTray.

There's also Gio.Settings, but distributing an application that uses it
with Python's setuptools would be difficult.
"""

import configparser
import os
import textwrap

from pkg_resources import resource_string

from pastetray import filepaths

_USER_CONFIG = os.path.join(filepaths.user_config_dir, 'settings.conf')

_config = configparser.ConfigParser()


def set_value(section, key, value):
    """Set a value to the configuration."""
    if isinstance(value, str):
        _config[section][key] = value
    # Booleans must be checked first because bool is a subclass of int,
    # but int is not a subclass of bool.
    elif isinstance(value, bool):
        _config[section][key] = 'true' if value else 'false'
    elif isinstance(value, int):
        _config[section][key] = str(value)
    else:
        raise TypeError("unknown value_type {.__name__}".format(type(value)))


def get_value_with_type(section, key, value_type):
    """Return a value of type value_type from the configuration."""
    if value_type is str:
        return _config.get(section, key)
    if value_type is int:
        return _config.getint(section, key)
    if value_type is bool:
        return _config.getboolean(section, key)
    raise TypeError("unknown value type {.__name__}".format(value_type))


def connect_property(widget, prop, section, key, value_type):
    """Make the settings change automatically, and set default value.

    This will read the current setting from the configuration, set the
    widget's property to it and connect a notify signal, so the settings
    will be automatically updated when the value of the property
    changes.
    """
    # This is a function inside a function because otherwise this
    # function would need to take a lot of parameters.
    def on_notify(widget, gparam):
        value = widget.get_property(prop)
        set_value(section, key, value, )
    current_value = _config.get_with_type(section, key, value_type)
    widget.set_property(prop, current_value)
    widget.connect('notify::'+prop, _on_notify, prop, section, key, value_type)


def _on_notify(widget, gparam, prop, *args):
    """Change settings when a GObject property's value is changed."""
    value = widget.get_property(prop)
    set_with_type(*args)


def load():
    """Load configuration files."""
    default_conf = resource_string('pastetray', 'default_settings.conf')
    _config.read_string(default_conf.decode('utf-8'))
    _config.read([_USER_CONFIG])


def save():
    """Save the user-wide configuration file."""
    comments = ("This is a configuartion file for PasteTray. To modify "
                "the preferences you can edit this file manually or "
                "run PasteTray and use the preferences option.")
    with open(_USER_CONFIG, 'w') as f:
        for line in textwrap.wrap(comments, 70):
            print('#', line, file=f)
        f.write('\n')
        _config.write(f)
