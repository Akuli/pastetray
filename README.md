# PasteTray

PasteTray is a simple GTK+ 3 client for online pastebins that displays a
system tray icon. You can easily make new pastes by clicking it.

These pastebins are supported by default:

- [dpaste](http://dpaste.com/)
- [Ghostbin](https://ghostbin.com/)
- [hastebin](http://hastebin.com/)
- [Paste ofCode](http://paste.ofcode.org/)

Writing custom pastebin scripts in Python is also possible.

### Dependencies

In order to run or install PasteTray you need to have these dependencies
installed.

| Name                  | Debian package        | PyPi package  | Notes
|-----------------------|-----------------------|---------------|----------
| appdirs               | python3-appdirs       | appdirs       | 
| lockfile              | none                  | lockfile      |
| pip _[1]_             | python3-pip           | pip           | You don't need PIP to run without installing. |
| pkg_resources         | python3-pkg-resources | pkg_resources |
| requests              | python3-requests      | requests      |
| git _[1]_             | python3-git           | none          | You can also download this program as a zip file.
| gi                    | python3-gi            | none _[2]_    |
| GTK+ 3 for gi         | gir1.2-gtk-3.0        | none          |
| AppIndicator3 for gi  | gir1.2-gtk-3.0        | none          |

_[1] _

_[2] If you don't want to install git _

_[3] Actually, there is a gi package in PyPi, but it's too old for
PasteTray._

On a Debian-based distribution you can install some of the dependencies
by opening a terminal and running these commmands (`$` is the prompt,
don't type that literally):

    $ sudo apt-get install python3-pip git python3-gi 

You'll probably find most of these packages from your GNU/Linux
distribution's package manager even if your distribution is not
Debian-based, but the packages' names can be different.

You can use this command to install most of the dependencies with pip.
This is user-wide so you don't need to worry about messing up your
operating system's Python directories.

    pip install --user appdirs pip pkg_resources requests

