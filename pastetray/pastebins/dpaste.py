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

"""This is a dpaste file for PasteTray."""

import requests
from pastetray import USER_AGENT

name = 'dpaste'
url = 'http://dpaste.com/'
expiry_days = [1, 7, 30, 365]
syntax_default = 'Plain text'
syntax_choices = {
    # This was generated with scripts/syntax_getters/dpaste.py in the
    # PasteTray source package.
    "RHTML": "rhtml",
    "Io": "io",
    "Myghty": "myghty",
    "Haskell": "haskell",
    "nginx config": "nginx",
    "Debian sourcelist": "sourceslist",
    "MoinMoin/Trac wiki markup": "trac-wiki",
    "SQL": "sql",
    "Sass": "sass",
    "DTD": "dtd",
    "Puppet": "puppet",
    "Lighttpd config": "lighty",
    "AppleScript": "applescript",
    "Bash": "bash",
    "Swift": "swift",
    "Fortran": "fortran",
    "INI": "ini",
    "Python 2": "python",
    "Bash session": "console",
    "Ruby": "rb",
    "SPARQL": "sparql",
    "HTML + Django/Jinja template": "html+django",
    "Ruby irb session": "rbcon",
    "C": "c",
    "Awk": "awk",
    "Java": "java",
    "HTML": "html",
    "CSS": "css",
    "Scheme": "scheme",
    "JavaScript": "js",
    "APL": "apl",
    "Smarty template": "smarty",
    "Batchfile": "bat",
    "Modula-2": "modula2",
    "C++": "cpp",
    "Go": "go",
    "Python console session": "pycon",
    "Delphi": "delphi",
    "JSON": "json",
    "XML": "xml",
    "IRC logs": "irc",
    "Groovy": "groovy",
    "Dylan": "dylan",
    "Tcl": "tcl",
    "Apache config": "apacheconf",
    "Common Lisp": "common-lisp",
    "JavaScript + Django/Jinja template": "js+django",
    "Groff": "groff",
    "ActionScript": "as",
    "Mathematica": "mathematica",
    "ERB": "erb",
    "Ragel": "ragel",
    "JavaServer pages": "jsp",
    "PostScript": "postscript",
    "Genshi": "genshi",
    "Darcs patch": "dpatch",
    "Prolog": "prolog",
    "PowerShell": "powershell",
    "PHP": "php",
    "Haml": "haml",
    "Erlang": "erlang",
    "Perl 6": "perl6",
    "Python 3 traceback": "py3tb",
    "Smalltalk": "smalltalk",
    "JavaScript + PHP": "js+php",
    "Python 3": "python3",
    "Shell session": "shell-session",
    "C#": "csharp",
    "Perl": "perl",
    "SCSS": "scss",
    "Ada": "ada",
    "text + Django/Jinja template": "django",
    "COBOL": "cobol",
    "VB.net": "vb.net",
    "Lasso": "lasso",
    "Mako": "mako",
    "Scala": "scala",
    "YAML": "yaml",
    "FSharp": "fsharp",
    "LLVM": "llvm",
    "Makefile": "make",
    "Matlab": "matlab",
    "Coldfusion HTML": "cfm",
    "XSLT": "xslt",
    "Lua": "lua",
    "Eiffel": "eiffel",
    "BBCode": "bbcode",
    "HTML + PHP": "html+php",
    "Rust": "rust",
    "Dart": "dart",
    "FoxPro": "Clipper",
    "Diff": "diff",
    "TeX": "tex",
    "Python 2 traceback": "pytb",
    "JavaScript + Ruby": "js+erb",
    "reStructuredText": "rst",
    "Plain text": "text",
    "Factor": "factor",
    "CoffeeScript": "coffee-script",
    "Clojure": "clojure",
    "OCaml": "ocaml",
    "Objective-C": "objective-c",
    "D": "d"
}

paste_args = ['content', 'expiry_days', 'syntax', 'title', 'username']


def paste(content, expiry_days, syntax, title, username):
    """Make a paste to dpaste.com."""
    response = requests.post(
        'http://dpaste.com/api/v2/',
        data={
            'content': content,
            'syntax': syntax,
            'title': title,
            'poster': username,
            'expiry_days': expiry_days,
        },
        headers={'User-Agent': USER_AGENT},
    )
    response.raise_for_status()
    return response.text.strip()
