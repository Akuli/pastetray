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

"""A new paste window."""

import os
import threading
import webbrowser

from gi.repository import Gtk, GLib, Pango
from pkg_resources import resource_string

from pastetray import _, backend, trayicon


class _Paster(Gtk.Builder):
    """Make a new paste."""

    def __init__(self):
        """Initialize the window."""
        Gtk.Builder.__init__(self)
        data = resource_string('pastetray', 'new_paste.glade')
        self.add_from_string(data.decode('utf-8'))

        get = self.get_object
        get('window').set_title(_("New paste") + " - PasteTray")
        get('title_entry').set_tooltip_text(_("The title of this paste"))
        get('textview').set_tooltip_text(_("The content of this paste"))
        get('pastebin_label').set_label(_("Pastebin:"))
        get('syntax_label').set_label(_("Syntax highlighting:"))
        get('username_label').set_label(_("Your name:"))
        get('username_label').set_halign(Gtk.Align.START)
        get('expiry_label').set_label(_("Expiry in days:"))
        self._apply_preferences()

        names = [pastebin.name for pastebin in backend.pastebins]
        names.sort(key=str.lower)
        for name in names:
            get('pastebin_combo').append_text(name)
        get('pastebin_combo').set_active(0)             # from settings
        get('username_entry').set_text(os.getlogin())   # from settings

        get('pastebin_combo').connect('changed', self._on_pastebin_changed)
        self._on_pastebin_changed(get('pastebin_combo'))
        get('paste_button').connect('clicked', self._on_paste_clicked)
        get('cancel_button').connect('clicked', self._destroy)
        get('window').connect('delete-event', self._destroy)

        self._apply_preferences()

    def _get_title(self):
        """Return the title the user has entered."""
        return self.get_object('title_entry').get_text()

    def _get_content(self):
        """Return the content to paste."""
        buf = self.get_object('textview').get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)

    def _get_pastebin_name(self):
        """Return the name of the selected pastebin."""
        combo = self.get_object('pastebin_combo')
        return combo.get_active_text()

    def _get_pastebin(self):
        """Return currently selected pastebin."""
        name = self._get_pastebin_name()
        for pastebin in backend.pastebins:
            if pastebin.name == name:
                return pastebin
        raise LookupError("no pastebin named {!r}".format(name))

    def _get_syntax(self):
        """Return currently selected syntax."""
        combo = self.get_object('syntax_combo')
        return combo.get_active_text()

    def _get_username(self):
        """Return currently entered username."""
        entry = self.get_object('username_entry')
        return entry.get_text()

    def _get_expiry(self):
        """Return currently selected expiry."""
        combo = self.get_object('expiry_combo')
        return int(combo.get_active_text())

    def _make_sensitive(self):
        """Make most of the widgets sensitive."""
        pastebin = self._get_pastebin()

        insensitives = 'progressbar',
        if not getattr(pastebin, 'use_syntax_colors', False):
            insensitives += 'syntax_label', 'syntax_combo'
        if not getattr(pastebin, 'use_title', False):
            insensitives += 'title_entry',
        if not getattr(pastebin, 'use_username', False):
            insensitives += 'username_label', 'username_entry'

        insensitives = [self.get_object(i) for i in insensitives]
        for obj in self.get_objects():
            obj.set_sensitive(obj not in insensitives)

    def _make_insensitive(self):
        """Make most of the widgets insensitive."""
        sensitives = [self.get_object('progressbar'),
                      self.get_object('window')]
        for obj in self.get_objects():
            obj.set_sensitive(obj in sensitives)

    def _on_pastebin_changed(self, pastebin_combo):
        pastebin = self._get_pastebin()

        if getattr(pastebin, 'use_syntax_colors', False):
            choices = list(pastebin.syntax_choices.keys())
            choices.sort(key=str.lower)
            combo = self.get_object('syntax_combo')
            combo.remove_all()
            for choice in choices:
                combo.append_text(choice)
            # TODO: Get this from settings.
            combo.set_active(choices.index(pastebin.default_syntax))

        combo = self.get_object('expiry_combo')
        combo.remove_all()
        for choice in pastebin.expiry_days:
            combo.append_text(str(choice))
        # TODO: Get this from settings.
        combo.set_active(0)

        self.get_object('disclaimer_label').set_markup(
            _("Make sure to read <a href='{url}'>your pastebin</a>'s terms "
              "and conditions.").format(url=pastebin.url)
        )
        self._make_sensitive()

    def _on_paste_clicked(self, button):
        """Run when user clicks the paste button."""
        pastebin = self._get_pastebin()

        kwargs = {'content': self._get_content(),
                  'expiry_days': self._get_expiry()}
        if getattr(pastebin, 'use_syntax_colors', False):
            kwargs['syntax'] = pastebin.syntax_choices[self._get_syntax()]
        if getattr(pastebin, 'use_title', False):
            kwargs['title'] = self._get_title()
        if getattr(pastebin, 'use_username', False):
            kwargs['username'] = self._get_username()

        self._make_insensitive()

        pasting_thread = threading.Thread(
            target=self._paste_with_pastebin,
            args=(pastebin, kwargs), daemon=True,
        )
        pasting_thread.start()
        GLib.timeout_add(50, self._on_timeout, pasting_thread)

    def _paste_with_pastebin(self, pastebin, kwargs):
        """Make a paste.

        This is executed in another thread, because this does not
        access GTK+.
        """
        try:
            self._response = str(pastebin.paste(**kwargs))
            self._success = True
        except Exception as e:
            self._response = "{.__name__}: {}".format(type(e), e)
            self._success = False

    def _on_timeout(self, pasting_thread):
        """Move the progressbar or show a message.

        This is executed with GLib's timeouts, because this needs to
        access GTK+.
        """
        if pasting_thread.is_alive():
            self.get_object('progressbar').pulse()
            return True

        if self._success:
            backend.recent_pastes.appendleft(self._response)
            trayicon.update()
            dialog = Gtk.MessageDialog(
                self.get_object('window'), Gtk.DialogFlags.MODAL,
                Gtk.MessageType.INFO, (
                    _("Open in browser"), Gtk.ResponseType.YES,
                    _("OK"), Gtk.ResponseType.OK,
                ), _("Pasting succeeded."),
            )
            dialog.set_title(_("Success"))
            dialog.format_secondary_text(self._response)
            if dialog.run() == Gtk.ResponseType.YES:
                webbrowser.open(self._response)
            dialog.destroy()
            self._destroy()

        else:
            dialog = Gtk.MessageDialog(
                self.get_object('window'), Gtk.DialogFlags.MODAL,
                Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                _("Pasting failed!"),
            )
            dialog.set_title(_("Error"))
            dialog.format_secondary_text(self._response)
            dialog.run()
            dialog.destroy()
            self._make_sensitive()

    def _apply_preferences(self):
        """Apply new preferences."""
        self.get_object('textview').override_font(
            Pango.FontDescription('monospace')
        )

    def _destroy(self, *ign):
        """Destroy the window."""
        # TODO: Save new default paste settings here.
        self.get_object('window').destroy()


def new_paste():
    """Make a new paste."""
    paster = _Paster()
    paster.get_object('window').show_all()
