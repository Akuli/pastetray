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
import webbrowser

from gi.repository import Gtk, GLib
from pkg_resources import resource_string

from pastetray import _, backend, utils
from pastetray.settings import settings


@utils.debug_class
class NewPasteWindow:
    """Make a new paste."""

    def __init__(self, postpaste_funcs=()):
        """Initialize the window.

        If pasting succeeds, everything in postpaste_funcs will be
        called with the paste URL as the only argument.
        """
        self._postpaste_funcs = postpaste_funcs

        self._builder = Gtk.Builder()
        data = resource_string('pastetray', 'new-paste.glade')
        self._builder.add_from_string(data.decode('utf-8'))

        get = self._builder.get_object

        wrap = settings.get_int('General', 'new_paste_wrap')
        font = settings.get_font('General', 'new_paste_font')
        get('textview').set_wrap_mode(wrap)
        get('textview').override_font(font)

        get('username-label').set_text(_("Name or nick:"))
        get('pastebin-label').set_text(_("Pastebin:"))
        get('expiry-label').set_text(_("Expiry:"))
        get('syntax-label').set_text(_("Syntax highlighting:"))

        username = settings.get_string('General', 'username',
                                       fallback=os.getlogin())
        get('username-entry').set_text(username)

        pastebin_names = sorted(backend.pastebins.keys(), key=str.lower)
        pastebin_default = settings.get_string('General', 'default_pastebin',
                                               fallback=pastebin_names[0])
        index = pastebin_names.index(pastebin_default)
        for name in pastebin_names:
            get('pastebin-combo').append_text(name)
        get('pastebin-combo').set_active(index)

        self._expiry_model = Gtk.ListStore(int, str)
        get('expiry-combo').set_model(self._expiry_model)
        renderer = Gtk.CellRendererText()
        get('expiry-combo').pack_start(renderer, True)
        get('expiry-combo').add_attribute(renderer, 'text', 1)

        self._syntax_completion = utils.EntryCompletion(
            get('syntax-entry'), get('syntax-image'),
            _("No syntax highlighting named {!r}"),
        )

        get('window').set_title(_("New paste") + " - PasteTray")

        get('pastebin-combo').connect('changed', self._on_pastebin_changed)
        get('expiry-combo').connect('changed', self._on_expiry_changed)
        get('syntax-entry').connect('changed', self._on_syntax_changed)
        get('paste-button').connect('clicked', self._on_paste_clicked)
        get('cancel-button').connect('clicked', self._destroy)
        get('window').connect('delete-event', self._destroy)

        self._on_pastebin_changed()

    def show(self):
        """Show the window and all widgets inside it."""
        self._builder.get_object('window').show_all()

    def _get_pastebin_name(self):
        """Return the name of currently selected pastebin."""
        return self._builder.get_object('pastebin-combo').get_active_text()

    def _get_content(self):
        """Return the content to paste."""
        buf = self._builder.get_object('textview').get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)

    def _get_expiry(self):
        """Return currently selected expiry."""
        index = self._builder.get_object('expiry-combo').get_active()
        return self._expiry_model[index][0]

    def _get_syntax(self):
        """Return currently selected syntax.

        The return value can be passed directly to pastebin.paste().
        """
        pastebin = backend.pastebins[self._get_pastebin_name()]
        syntax_name = self._builder.get_object('syntax-entry').get_text()
        syntax_default = pastebin.syntax_choices[pastebin.syntax_default]
        return pastebin.syntax_choices.get(syntax_name, syntax_default)

    def _make_sensitive(self):
        """Make most of the widgets sensitive."""
        pastebin = backend.pastebins[self._get_pastebin_name()]

        insensitives = [self._builder.get_object('progressbar')]
        if 'title' not in pastebin.paste_args:
            insensitives.append(self._builder.get_object('title_label'))
            insensitives.append(self._builder.get_object('title-entry'))
        if 'syntax' not in pastebin.paste_args:
            insensitives.append(self._builder.get_object('syntax-label'))
            insensitives.append(self._builder.get_object('syntax-entry'))
            insensitives.append(self._builder.get_object('syntax-image'))
        if 'username' not in pastebin.paste_args:
            insensitives.append(self._builder.get_object('username-label'))
            insensitives.append(self._builder.get_object('username-entry'))
        if len(pastebin.expiry_days) < 2:
            insensitives.append(self._builder.get_object('expiry-label'))
            insensitives.append(self._builder.get_object('expiry-combo'))

        for obj in self._builder.get_objects():
            obj.set_sensitive(obj not in insensitives)

    def _make_insensitive(self):
        """Make most of the widgets insensitive."""
        sensitives = [self._builder.get_object('progressbar'),
                      self._builder.get_object('window')]
        for obj in self._builder.get_objects():
            obj.set_sensitive(obj in sensitives)

    def _on_pastebin_changed(self, widget=None):
        """Apply new syntax and expiry choices."""
        pastebin_name = self._get_pastebin_name()
        pastebin = backend.pastebins[pastebin_name]
        get = self._builder.get_object

        if 'syntax' in pastebin.paste_args:
            completions = pastebin.syntax_choices.keys()
            self._syntax_completion.set_completions(completions)
            syntax = settings.get_string('DefaultSyntax', pastebin_name,
                                         fallback=None)
            if syntax not in pastebin.syntax_choices.keys():
                syntax = pastebin.syntax_default
            with utils.blocked(get('syntax-entry'), self._on_syntax_changed):
                get('syntax-entry').set_text(syntax)
            self._syntax_completion.on_entry_changed()

        default_expiry = settings.get_string('DefaultExpiry', pastebin_name,
                                             fallback=None)
        if default_expiry in pastebin.expiry_days:
            default_expiry_index = pastebin.expiry_days.index(default_expiry)
        else:
            default_expiry_index = 0

        with utils.blocked(get('expiry-combo'), self._on_expiry_changed):
            self._expiry_model.clear()
            for expiry in pastebin.expiry_days:
                if expiry < 0:
                    text = _("Never expire this paste")
                else:
                    text = _("{} days").format(expiry)
                self._expiry_model.append([expiry, text])
            get('expiry-combo').set_active(default_expiry_index)

        get('reminder-label').set_markup(
            _("Remember to read <a href=\"{url}\">your pastebin</a>'s "
              "terms and conditions.").format(url=pastebin.url)
        )

        self._make_sensitive()

    def _on_expiry_changed(self, widget):
        """Set the default expiry to settings."""
        settings.set_int('DefaultExpiry', self._get_pastebin_name(),
                         self._get_expiry())

    def _on_syntax_changed(self, widget):
        """Set the new default syntax to settings."""
        get = self._builder.get_object
        self._syntax_completion.on_entry_changed()

        # The _get_syntax() method returns a pastebin.syntax_choices
        # value, not a key.
        settings.set_string('DefaultSyntax', self._get_pastebin_name(),
                            get('syntax-entry').get_text())

    def _on_paste_clicked(self, widget):
        """Run when user clicks the paste button."""
        self._make_insensitive()
        pastebin = backend.pastebins[self._get_pastebin_name()]
        getters = {
            'content': self._get_content,
            'expiry': self._get_expiry,
            'syntax': self._get_syntax,
            'title': self._builder.get_object('title-entry').get_text,
            'username': self._builder.get_object('username-entry').get_text,
        }
        pasting_thread = backend.PastingThread(pastebin, getters)
        pasting_thread.daemon = True
        pasting_thread.start()
        GLib.timeout_add(50, self._on_timeout, pasting_thread)

    def _on_timeout(self, pasting_thread):
        """Move the progressbar or show a message.

        This is executed with GLib's timeouts because this needs to
        access GTK+.
        """
        if pasting_thread.is_alive():
            # Move the progress bar and run this again.
            self._builder.get_object('progressbar').pulse()
            return True

        if pasting_thread.success:
            for func in self._postpaste_funcs:
                func(pasting_thread.response)
            dialog = Gtk.MessageDialog(
                self._builder.get_object('window'), Gtk.DialogFlags.MODAL,
                Gtk.MessageType.INFO, (
                    _("Open in browser"), Gtk.ResponseType.YES,
                    _("OK"), Gtk.ResponseType.OK,
                ), _("Pasting succeeded."),
            )
            dialog.set_title(_("Success"))
            dialog.format_secondary_text(pasting_thread.response)
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                webbrowser.open(pasting_thread.response)
            self._destroy()

        else:
            dialog = Gtk.MessageDialog(
                self._builder.get_object('window'), Gtk.DialogFlags.MODAL,
                Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                _("Pasting failed!"),
            )
            dialog.set_title(_("Error"))
            dialog.format_secondary_text(pasting_thread.response)
            dialog.run()
            dialog.destroy()
            self._make_sensitive()

    def _destroy(self, widget=None, event=None):
        """Save some settings and destroy the window."""
        get = self._builder.get_object

        settings.set_string('General', 'username',
                            get('username-entry').get_text())
        settings.set_string('General', 'default_pastebin',
                            self._get_pastebin_name())
        get('window').destroy()
