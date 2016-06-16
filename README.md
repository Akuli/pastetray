# PasteTray

PasteTray is a simple GTK+ 3 client for online pastebins that displays a
system tray icon. You can easily make new pastes by clicking it.

These pastebins are supported by default:

- [dpaste](http://dpaste.com/)
- [Ghostbin](https://ghostbin.com/)
- [hastebin](http://hastebin.com/)
- [Paste ofCode](http://paste.ofcode.org/)

Writing custom pastebin scripts in Python is also possible.

### Downloading, running and installing

To run PasteTray, you need to install gi with GTK+ 3 and git if you
don't already have them installed. You also need Python 3 with PIP. Most
GNU/Linux distributions come with gi and GTK+ 3 installed, and you can
install git and PIP on Debian-based distribution (like Ubuntu and Linux
Mint) by running this on a terminal (`$` is the prompt, don't type it
literally):

    $ sudo aptitude install git python3-pip

You can use apt-get if you don't have aptitude:

    $ sudo apt-get install git

When you have everything installed you can download PasteTray with git
and install it with PIP. This will install it user-wide, everything will
be inside your home directory. The `/` in the end of the PIP command is
important, it tells PIP that pastetray is a directory.

    $ git clone https://github.com/Akuli/pastetray
    $ pip install --user pastetray/

### Authors

I am Akuli and I have written most of PasteTray, but I want to thank
these people for helping me with it:

- [SquishyStrawberry](https://github.com/SquishyStrawberry/) wrote the
original versions of Paste ofCode and hastebin pasting scripts.
- [Chisight](https://github.com/Chisight/) wrote the original ghostbin
pasting script. His version of it is available in his
[ghostbinit repository](https://github.com/Chisight/ghostbinit).
