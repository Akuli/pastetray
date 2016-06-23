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

"""A cross-platform file locker for PasteTray."""

import contextlib
import os
import platform

from pastetray import filepaths

_WINDOWS = platform.system() == 'Windows'
if _WINDOWS:
    import msvcrt       # NOQA
else:
    import fcntl        # NOQA

_LOCKFILE = os.path.join(filepaths.user_cache_dir, 'lock')


class IsLocked(BlockingIOError):
    """The lockfile has been locked by another process."""


@contextlib.contextmanager
def _windows_locked():
    """Lock-and-unlock context manager for Windows."""
    with open(_LOCKFILE, 'w') as f:
        try:
            # The lockfile needs to contain something to lock.
            content = "This is a PasteTray lock file."
            f.write(content)
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBRLCK, len(content))
        except OSError:
            raise IsLocked from None
        yield
        # Closing the file will release the lock.


@contextlib.contextmanager
def _unix_locked():
    """Lock-and-unlock context manager for Unix-like operating systems."""
    with open(_LOCKFILE, 'w') as fd:
        try:
            fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (PermissionError, BlockingIOError):
            # The errno is EACCESS or EAGAIN.
            raise IsLocked from None
        yield
        fcntl.lockf(fd, fcntl.LOCK_UN)


locked = _windows_locked if _WINDOWS else _unix_locked
