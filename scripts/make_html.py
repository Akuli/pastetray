#!/usr/bin/env python3

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

"""Make a help.html for PasteTray."""

import os
import sys
import textwrap

import markdown
from pygments.formatters import HtmlFormatter


def fix_codeblocks(md):
    """Change ``` code blocks to indented code blocks."""
    languages = {'py': 'python', '': 'sh'}
    lines = iter(md.split('\n'))
    content = ''

    try:
        while True:
            line = next(lines)
            if line.startswith('```'):
                # Code, this must be indented.
                lang = languages[line[3:]]
                content += '    :::{}\n'.format(lang)
                while True:
                    line = next(lines)
                    if line == '```':
                        break
                    content += '    {}\n'.format(line)
            else:
                content += '{}\n'.format(line)
    except StopIteration:
        return content


def fix_links(md):
    """Change the links in the markdown file to make them work in HTML."""
    md = md.replace('(pastetray/doc/', '(')
    md = md.replace('.md)', '.html)')
    return md


def make_html(md):
    """Convert markdown to HTML."""
    title = md.split('\n', 1)[0].lstrip('# ')
    md = fix_codeblocks(md)
    md = fix_links(md)
    content = markdown.markdown(md, extensions=['codehilite'])
    with open(os.path.join('scripts', 'template.html'), 'r') as f:
        template = f.read()
    return template.format(title=title, content=content)


def make_css():
    """Return the content of a style.css file."""
    # Nice styles: vs, tango
    formatter = HtmlFormatter(style='tango')
    with open(os.path.join('scripts', 'template.css'), 'r') as f:
        template = f.read()
    return template + formatter.get_style_defs('.codehilite')


def main():
    """Run the script."""
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(here))

    dstdir = os.path.join('pastetray', 'doc')

    # HTML files
    files = [('README.md', 'index.html'),
             ('writing_pastebins.md', 'writing_pastebins.html')]
    for src, dst in files:
        with open(src, 'r') as f:
            md = f.read()
        html = make_html(md)
        with open(os.path.join(dstdir, dst), 'w') as f:
            f.write(html)

    # CSS file
    with open(os.path.join(dstdir, 'style.css'), 'w') as f:
        f.write(make_css())

    sys.exit()


if __name__ == '__main__':
    main()
