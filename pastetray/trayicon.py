"""The application indicator/tray icon."""
from gettext import gettext as _
import pkg_resources
import webbrowser
from gi.repository import Gtk, Gdk, GdkPixbuf
from pastetray import backend, pastebin_editor, preference_editor, utils

# AppIndicator3 may not be installed.
try:
    from gi.repository import AppIndicator3     # NOQA
except ImportError:
    print("AppIndicator3 is not installed.")
    AppIndicator3 = None

# Gtk.StatusIcon is deprecated in new versions of GTK+.
if AppIndicator3 is None:
    if not hasattr(Gtk, 'StatusIcon'):
        raise ImportError("AppIndicator3 is not installed and Gtk.StatusIcon "
                          "is deprecated in the current version of GTK+.")
    print("AppIndicator3 is not installed, Gtk.StatusIcon "
          "will be used instead.")


@utils.debug
def _on_statusicon_click(statusicon, button, time):
    statusicon.get_menu().popup(
        None, None, Gtk.StatusIcon.position_menu, statusicon,
        button, time or Gtk.get_current_event_time(),
    )


@utils.debug
def _on_url_clicked(menuitem, url):
    """Open the url."""
    webbrowser.open(url)


@utils.debug
def about_dialog(*ign):
    """Display an about dialog."""
    # Load the license and paste icon.
    license = pkg_resources.resource_string('pastetray', 'LICENSE')
    logo = Gtk.IconTheme.get_default().lookup_icon(
        Gtk.STOCK_PASTE, Gtk.IconSize.DIALOG,
        Gtk.IconLookupFlags.NO_SVG,
    )

    # Display a dialog.
    dialog = Gtk.AboutDialog()
    dialog.set_program_name("PasteTray")
    dialog.set_version(about.VERSION)
    dialog.set_comments(about.SHORT_DESC[0].upper() +
                        about.SHORT_DESC[1:] + ".")
    dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(logo.get_filename()))
    dialog.set_license(license.decode('utf-8'))
    dialog.set_resizable(True)         # the license is a bit long
    dialog.set_authors(about.AUTHORS)
    dialog.set_translator_credits(
        '\n'.join(': '.join(item) for item in about.TRANSLATORS.items())
    )
    dialog.run()
    dialog.destroy()


@utils.debug
def update(*ign):
    """Update the menu."""
    # This file is imported by new_paste.py.
    from pastetray.new_paste import new_paste
    menu = _TRAYICON.get_menu()

    # Clear the menu.
    for item in menu.get_children():
        menu.remove(item)   # this may make a weird error message

    # Make the menuitems.
    stocks = [Gtk.STOCK_NEW, Gtk.STOCK_PREFERENCES, None, None,
              Gtk.STOCK_ABOUT, Gtk.STOCK_QUIT]
    texts = [_("New paste"), _("Settings"), _("Pastebin settings"),
             _("Preferences"), _("About"), _("Quit")]
    funcs = [new_paste, None, pastebin_editor.run, preference_editor.run,
             about_dialog, Gtk.main_quit]

    if hasattr(Gtk, 'ImageMenuItem'):
        # Gtk.ImageMenuItem is not deprecated.
        items = []
        for stock, text in zip(stocks, texts):
            if stock is None:
                items.append(Gtk.MenuItem(text))
            else:
                items.append(Gtk.ImageMenuItem.new_from_stock(stock))
    else:
        items = [Gtk.MenuItem(text) for text in texts]

    for item, func in zip(items, funcs):
        if func is not None:
            item.connect('activate', func)

    # Add the items.
    items = iter(items)

    # New paste.
    menu.add(next(items))
    menu.add(Gtk.SeparatorMenuItem())

    # Recent pastes.
    if backend.RECENT_PASTES:
        for number, url in enumerate(backend.RECENT_PASTES, start=1):
            item = Gtk.MenuItem('%d. %s' % (number, url))
            item.connect('activate', _on_url_clicked, url)
            menu.add(item)
    else:
        item = Gtk.MenuItem(_("(no pastes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        menu.add(item)
    menu.add(Gtk.SeparatorMenuItem())

    # Settings.
    setting_item = next(items)
    submenu = Gtk.Menu()
    submenu.add(next(items))   # pastebin settings
    submenu.add(next(items))   # general preferences
    setting_item.set_submenu(submenu)
    menu.add(setting_item)

    # Rest of the items.
    for item in items:
        menu.add(item)

    # Showing the items.
    menu.show_all()


@utils.debug
def load():
    """Load the trayicon."""
    global _TRAYICON
    menu = Gtk.Menu()

    if AppIndicator3 is None:
        _TRAYICON = Gtk.StatusIcon()
        _TRAYICON.set_from_icon_name(Gtk.STOCK_PASTE)
        _TRAYICON.connect('popup-menu', _on_statusicon_click)
        _TRAYICON.connect('activate', _on_statusicon_click,
                          Gdk.BUTTON_PRIMARY, False)
        _TRAYICON.get_menu = lambda menu=menu: menu

    else:
        _TRAYICON = AppIndicator3.Indicator.new(
            'pastetray', Gtk.STOCK_PASTE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        _TRAYICON.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        _TRAYICON.set_menu(menu)
