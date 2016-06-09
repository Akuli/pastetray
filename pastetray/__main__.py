"""Run the program."""

from gi.repository import Gtk
from pastetray import backend, trayicon


def main():
    backend.load()
    trayicon.load()
    trayicon.update()
    Gtk.main()
    backend.unload()


if __name__ == '__main__':
    main()
