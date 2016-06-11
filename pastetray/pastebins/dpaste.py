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
use_syntax_colors = True
use_title = True
use_username = True
expiry_days = [1, 7, 30, 365]
default_syntax = 'Plain text'
syntax_choices = {
    # This was generated with syntax_getters/dpaste.py in the source
    # package.
    'Ada': 'ada',
    'Apache config': 'apacheconf',
    'APL': 'apl',
    'AppleScript': 'applescript',
    'ActionScript': 'as',
    'Awk': 'awk',
    'Bash': 'bash',
    'Batchfile': 'bat',
    'BBCode': 'bbcode',
    'C': 'c',
    'Coldfusion HTML': 'cfm',
    'FoxPro': 'Clipper',
    'Clojure': 'clojure',
    'COBOL': 'cobol',
    'CoffeeScript': 'coffee-script',
    'Common Lisp': 'common-lisp',
    'Bash session': 'console',
    'C++': 'cpp',
    'C#': 'csharp',
    'CSS': 'css',
    'D': 'd',
    'Dart': 'dart',
    'Delphi': 'delphi',
    'Diff': 'diff',
    'text + Django/Jinja template': 'django',
    'Darcs patch': 'dpatch',
    'DTD': 'dtd',
    'Dylan': 'dylan',
    'Eiffel': 'eiffel',
    'ERB': 'erb',
    'Erlang': 'erlang',
    'Factor': 'factor',
    'Fortran': 'fortran',
    'FSharp': 'fsharp',
    'Genshi': 'genshi',
    'Go': 'go',
    'Groff': 'groff',
    'Groovy': 'groovy',
    'Haml': 'haml',
    'Haskell': 'haskell',
    'HTML': 'html',
    'HTML + Django/Jinja template': 'html+django',
    'HTML + PHP': 'html+php',
    'INI': 'ini',
    'Io': 'io',
    'IRC logs': 'irc',
    'Java': 'java',
    'JavaScript': 'js',
    'JavaScript + Django/Jinja template': 'js+django',
    'JavaScript + Ruby': 'js+erb',
    'JavaScript + PHP': 'js+php',
    'JSON': 'json',
    'JavaServer pages': 'jsp',
    'Lasso': 'lasso',
    'Lighttpd config': 'lighty',
    'LLVM': 'llvm',
    'Lua': 'lua',
    'Makefile': 'make',
    'Mako': 'mako',
    'Mathematica': 'mathematica',
    'Matlab': 'matlab',
    'Modula-2': 'modula2',
    'Myghty': 'myghty',
    'nginx config': 'nginx',
    'Objective-C': 'objective-c',
    'OCaml': 'ocaml',
    'Perl': 'perl',
    'Perl 6': 'perl6',
    'PHP': 'php',
    'PostScript': 'postscript',
    'PowerShell': 'powershell',
    'Prolog': 'prolog',
    'Puppet': 'puppet',
    'Python 3 traceback': 'py3tb',
    'Python console session': 'pycon',
    'Python 2 traceback': 'pytb',
    'Python 2': 'python',
    'Python 3': 'python3',
    'Ragel': 'ragel',
    'Ruby': 'rb',
    'Ruby irb session': 'rbcon',
    'RHTML': 'rhtml',
    'reStructuredText': 'rst',
    'Rust': 'rust',
    'Sass': 'sass',
    'Scala': 'scala',
    'Scheme': 'scheme',
    'SCSS': 'scss',
    'Shell session': 'shell-session',
    'Smalltalk': 'smalltalk',
    'Smarty template': 'smarty',
    'Debian sourcelist': 'sourceslist',
    'SPARQL': 'sparql',
    'SQL': 'sql',
    'Swift': 'swift',
    'Tcl': 'tcl',
    'TeX': 'tex',
    'Plain text': 'text',
    'MoinMoin/Trac wiki markup': 'trac-wiki',
    'VB.net': 'vb.net',
    'XML': 'xml',
    'XSLT': 'xslt',
    'YAML': 'yaml',
}


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
