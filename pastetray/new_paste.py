"""A new paste window."""
# Remember: two pastebins must not have the same name.

import copy
import os
import pkg_resources
import threading
from gettext import gettext as _
from gi.repository import Gtk, Gdk, GLib, Pango
from pastetray import backend, trayicon, utils

_PASTERS = []


class _Paster(Gtk.Builder):
    """A window for making a new paste."""

    @utils.debug
    def __init__(self):
        """Initialize the window."""
        # Load the glade file.
        Gtk.Builder.__init__(self)
        data = pkg_resources.resource_string('pastetray', 'new_paste.glade')
        self.add_from_string(data.decode('utf-8'))

        # The pastebin list may change while this window is opened.
        self._pastebins = copy.deepcopy(backend.PASTEBINS)

        # Setting up labels and tooltips.
        get = self.get_object
        get('window').set_title(_("New paste") + " - PasteTray")
        get('title_entry').set_tooltip_text(_("The title of this paste"))
        get('textview').set_tooltip_text(_("The content of this paste"))
        get('pastebin_label').set_label(_("Pastebin:"))
        get('syntax_label').set_label(_("Syntax highlighting:"))
        get('username_label').set_label(_("Username"))
        get('expiry_label').set_label(_("Expiry in days"))
        self._apply_preferences()

        # Pasting options.
        names = [pastebin['name'] for pastebin in self._pastebins]
        names.sort(key=str.lower)
        for name in names:
            get('pastebin_combo').append_text(name)
        get('pastebin_combo').set_active(0)
        get('username_entry').set_text(os.getlogin())

        # Signals.
        get('pastebin_combo').connect('changed', self._on_pastebin_changed)
        get('syntax_combo').connect('changed', self._on_syntax_changed)
        self._on_pastebin_changed(get('pastebin_combo'))
        self._on_syntax_changed(get('syntax_combo'))
        get('username_entry').connect('changed', self._on_username_changed)
        get('paste_button').connect('clicked', self._start_pasting)
        get('cancel_button').connect('clicked', self._destroy)
        get('window').connect('delete-event', self._destroy)

    @utils.debug
    def _apply_preferences(self):
        # TODO: add preferences.
        self.get_object('textview').override_font(
            Pango.FontDescription('monospace')
        )

    @utils.debug
    def _get_current_pastebin(self):
        """Return the currently selected pastebin."""
        pastebin_name = self.get_object('pastebin_combo').get_active_text()
        for pastebin in self._pastebins:
            if pastebin['name'] == pastebin_name:
                return pastebin
        raise LookupError("no pastebin named %r" % pastebin_name)

    @utils.debug
    def _on_pastebin_changed(self, pastebin_combo):
        """Update the syntax choices and expiry settings."""
        pastebin = self._get_current_pastebin()

        # Syntax choices.
        choices = list(pastebin['syntax_choices'].keys())
        choices.sort(key=str.lower)
        combo = self.get_object('syntax_combo')
        with utils.disconnected(combo, 'changed', self._on_syntax_changed):
            combo.remove_all()
            for choice in choices:
                combo.append_text(choice)
            combo.set_active(choices.index(pastebin['default_syntax']))

        # Expiry.
        spinbutton = self.get_object('expiry_spinbutton')
        spinbutton.set_range(1, pastebin['max_expiry_days'])

    @utils.debug
    def _on_syntax_changed(self, syntax_combo):
        """Set the new default syntax to backend's pastebin."""
        pastebin_combo = self.get_object('pastebin_combo')
        pastebin_name = pastebin_combo.get_active_text()
        for pastebin in backend.PASTEBINS:
            if pastebin['name'] == pastebin_name:
                pastebin['default_syntax'] = syntax_combo.get_active_text()
                break
        # If the pastebin is not found its name has been changed while
        # this window has been open. There's no need to do anything
        # about it.

    @utils.debug
    def _on_username_changed(self, entry):
        """Change the default username."""
        # TODO

    @utils.debug
    def _start_pasting(self, button):
        """Start pasting the content."""
        # Change the sensitivity.
        for widget in self.get_objects():
            if widget in (self.get_object('window'),
                          self.get_object('progressbar')):
                widget.set_sensitive(True)
            else:
                widget.set_sensitive(False)

        # Get required information.
        get = self.get_object
        buf = get('textview').get_buffer()

        kwargs = {
            'pastebin': self._get_current_pastebin(),
            'title': get('title_entry').get_text(),
            'content': buf.get_text(buf.get_start_iter(),
                                    buf.get_end_iter(), True),
            'syntax': get('syntax_combo').get_active_text(),
            'username': get('username_entry').get_text(),
            'expiry_days': get('expiry_spinbutton').get_value_as_int(),
        }

        # Paste in a thread and move the progressbar in a timeout.
        pasting_thread = threading.Thread(
            target=self._backend_paste,
            kwargs=kwargs, daemon=True,
        )
        pasting_thread.start()
        GLib.timeout_add(50, self._on_timeout, pasting_thread)

    @utils.debug
    def _backend_paste(self, **kwargs):
        """Call backend.paste, this can be ran in another thread."""
        try:
            self._response = backend.paste(**kwargs)
            self._success = True
        except Exception as e:
            self._response = "%s: %s" % (type(e).__name__, e)
            self._success = False

    @utils.debug
    def _on_timeout(self, pasting_thread):
        if pasting_thread.is_alive():
            # Still pasting, moving the progressbar and returning True
            # to make this function run again.
            self.get_object('progressbar').pulse()
            return True

        if self._success:
            # Paste succeeded.
            backend.RECENT_PASTES.appendleft(self._response)
            dialog = Gtk.MessageDialog(
                self.get_object('window'), Gtk.DialogFlags.MODAL,
                Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                _("Pasting succeeded. The URL was copied to clipboard."),
            )
            dialog.set_title(_("Success"))
            dialog.format_secondary_text(self._response)
            dialog.run()
            dialog.destroy()
            self._destroy()
        else:
            # Paste failed.
            dialog = Gtk.MessageDialog(
                self.get_object('window'), Gtk.DialogFlags.MODAL,
                Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                _("Pasting failed!"),
            )
            dialog.set_title(_("Error"))
            dialog.format_secondary_text(self._response)
            dialog.run()
            dialog.destroy()

        # Change the sensitivity.
        for widget in self.get_objects():
            if widget is self.get_object('progressbar'):
                widget.set_sensitive(False)
            else:
                widget.set_sensitive(True)

    def _add_to_clipboard(self, text):
        """Add text to clipboard"""
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)
        

    @utils.debug
    def _destroy(self, *ign):
        """Destroy the window."""
        self.get_object('window').destroy()
        _PASTERS.remove(self)


@utils.debug
def new_paste(*ign):
    """Make a new paste."""
    paster = _Paster()
    paster.get_object('window').show_all()
    _PASTERS.append(paster)
