"""Set up Gtk, threading, Ctrl+C interrupting and internationalization."""
import signal
import gi
from gi.repository import GObject

gi.require_version('Gtk', '3.0')
GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
