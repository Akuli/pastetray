"""A pastebin editor window."""

import collections
from gettext import gettext as _
from gi.repository import Gtk
from pastetray import backend, utils


class _PastebinNotebook(Gtk.Notebook):

    def on_new_clicked(self, button):
        content = Gtk.Label("Hello World!")
        content.show_all()

        top = Gtk.Box()
        top.pack_start(Gtk.Label('foo'), True, True, 0)
        button = Gtk.Button()
        button.connect('clicked', self._on_close_clicked, content)
        button.set_image(Gtk.Image.new_from_icon_name(
            Gtk.STOCK_CLOSE, Gtk.IconSize.MENU,
        ))
        top.pack_end(button, False, False, 0)
        top.show_all()

        self.append_page(content)
        self.set_tab_label(content, top)
        self.show_all()
        self.set_current_page(self.get_n_pages() - 1)   # last page

    def _on_close_clicked(self, widget, content):
        self.remove_page(self.page_num(content))


@utils.debug
def run(*ign):
    """Open a window for editing pastebin settings."""
    dialog = Gtk.Dialog(
        # The transient parent is None, because there is no parent
        # window.
        _("Pastebin settings"), None, 0, (
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        )
    )

    overlay = Gtk.Overlay()
    notebook = _PastebinNotebook()
    overlay.add(notebook)
    button = Gtk.Button(_("New pastebin"))
    button.connect('clicked', notebook.on_new_clicked)
    button.set_halign(Gtk.Align.END)
    button.set_valign(Gtk.Align.START)
    overlay.add_overlay(button)

    dialog.get_content_area().pack_start(overlay, True, True, 0)
    dialog.show_all()
    dialog.run()
    dialog.destroy()
