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

"""Handy utilities."""

import contextlib
import functools

from gi.repository import Gtk


class EntryCompletion:
    """Simple entry autocompletion."""

    def __init__(self, entry, image, invalid_choice_tooltip):
        """Set up the autocompletion.

        The entry should be a Gtk.Entry, and image should be a Gtk.Image
        next to it. The image will be changed depending on wether the
        text in the entry is in the completions, and the tooltip will be
        set to invalid_choice_tooltip if it's not.
        """
        self._entry = entry
        self._image = image
        self._tooltip = invalid_choice_tooltip

        self._model = Gtk.ListStore(str)
        self._completion = Gtk.EntryCompletion()
        self._completion.set_model(self._model)
        self._completion.set_text_column(0)
        self._completion.set_match_func(self._match)
        entry.set_completion(self._completion)
        self.on_entry_changed()

    def _match(self, completion, char, tree_iter):
        """Check if the completion should be displayed."""
        entry_text = self._entry.get_text()
        match_text = self._model[tree_iter][0]
        return entry_text.lower().strip() in match_text.lower()

    def on_entry_changed(self, widget=None):
        """Display a triangle if entry's text is not in completions.

        Connect the entry's changed signal to this.
        """
        entry_text = self._entry.get_text()
        if entry_text in (i[0] for i in self._model):
            self._image.clear()
            self._image.set_tooltip_text(None)
        else:
            self._image.set_from_icon_name(Gtk.STOCK_CAPS_LOCK_WARNING,
                                           Gtk.IconSize.BUTTON)
            self._image.set_tooltip_text(self._tooltip.format(entry_text))

    def set_completions(self, completions):
        """Set the autocompletion list to complete from."""
        self._model.clear()
        for completion in completions:
            self._model.append([completion])
        self.on_entry_changed()


@contextlib.contextmanager
def blocked(widget, function):
    """Block a GObject signal temporarily."""
    widget.handler_block_by_func(function)
    yield
    widget.handler_unblock_by_func(function)


def debug(func):
    """Return a function that prints func's name and runs func.

    Decorate functions with this for debugging.
    """
    try:
        msg = func.__qualname__
    except AttributeError:
        msg = func.__name__
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return inner


def debug_class(cls):
    """Apply debug() to all methods of a class.

    Note that this modifies the original class and also returns it.
    """
    for key, val in cls.__dict__.items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls
