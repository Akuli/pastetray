"""Write information about paste.ofcode.org as json to stdout."""

import html.parser
import json
import sys

import requests


class PasteOfCodeParser(html.parser.HTMLParser):
    """Extract syntax highlighting choices out of the paste page."""

    def handle_starttag(self, tag, attrs):
        """The parser enters a tag."""
        if tag == 'option':
            self._current_tag = dict(attrs)['value']

    def handle_data(self, data):
        """The parser processes data inside a tag."""
        if self._current_tag is not None:
            self._resultdict[data] = self._current_tag

    def handle_endtag(self, tag):
        """The parser leaves a tag."""
        if tag == 'option':
            self._current_tag = None

    def parse(self, data):
        """Main method."""
        self._current_tag = None
        self._resultdict = {}
        self.feed(data)
        return self._resultdict


parser = PasteOfCodeParser()
data = parser.parse(requests.get('http://paste.ofcode.org/').text)

json.dump(data, sys.stdout, indent=4)
print()
