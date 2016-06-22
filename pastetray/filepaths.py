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

"""The filepaths."""

import functools
import os
import sys
import tempfile

import appdirs
import pkg_resources


@functools.lru_cache()
def resource_filename(*args):
    """A zipsafe alternative to pkg_resources.resource_filename.

    resource must be a pkg_resources path to a file. A temporary file
    will be created if pkg_resources.resource_filename cannot be used.
    """
    try:
        return pkg_resources.resource_filename(*args)
    except NotImplementedError:
        # Running from a zipfile.
        pkg, path = args
        path = path.split('/')
        filepath = os.path.join(temp_dir, pkg, *path)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with pkg_resources.resource_stream(*args) as src:
            with open(filepath, 'wb') as dst:
                shutil.copyfileobj(src, dst)
        return filepath


def resource_listdir(*args):
    """Fix a bug in pkg_resources.resource_listdir().

    This function only returns non-empty results.
    """
    return [i for i in pkg_resources.resource_listdir(*args) if i]


# Windows uses CapsWords for application names, but most other operating
# systems don't.
app = 'PasteTray' if sys.platform == 'win32' else 'pastetray'

user_cache_dir = appdirs.user_cache_dir(app)
user_config_dir = appdirs.user_config_dir(app)
temp_dir = tempfile.mkdtemp(app)

os.makedirs(user_cache_dir, exist_ok=True)
os.makedirs(user_config_dir, exist_ok=True)
# The temporary directory will be created later if it's needed.
