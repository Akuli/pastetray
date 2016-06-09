"""Take care of HTTP posting, recent pastes and pastebin settings."""

import collections
import json
import os
import pkg_resources
import requests
from pastetray import about, filepaths, utils

PASTEBINS = []
RECENT_PASTES = collections.deque(maxlen=10)
USER_AGENT = 'PasteTray/%s' % about.VERSION

_RECENT_PASTE_PATH = os.path.join(filepaths.user_config_dir,
                                  'recent_pastes.txt')
_PASTEBIN_JSON_PATH = os.path.join(filepaths.user_config_dir,
                                   'pastebins')
os.makedirs(_PASTEBIN_JSON_PATH, exist_ok=True)


@utils.debug
def paste(pastebin, title, content, syntax, username, expiry_days):
    """Make a paste and returns the URL."""
#    print('paste' + repr((pastebin, title, content, syntax, username, expiry_days)))
    # Get the formatters.
    d = {'title': title, 'content': content,
         'syntax': pastebin['syntax_choices'][syntax],
         'username': username, 'expiry_days': expiry_days,
         'user_agent': USER_AGENT}

    # Paste.
    response = requests.post(
        pastebin['url'],
        data={key: val % d for key, val in pastebin['data'].items()},
        params={key: val % d for key, val in pastebin['params'].items()},
        headers={key: val % d for key, val in pastebin['headers'].items()},
    )
    response.raise_for_status()
    result = getattr(response, pastebin['response_attr'])
    if isinstance(result, bytes):
        result = result.decode('utf-8')
    return result.strip()


@utils.debug
def load():
    """Load information about pastebins and recent pastes."""
    # Load the recent pastes
    RECENT_PASTES.clear()
    try:
        with open(_RECENT_PASTE_PATH, 'r') as f:
            RECENT_PASTES.extend(line.strip() for line in f)
    except FileNotFoundError:
        pass

    # Load the pastebins
    PASTEBINS.clear()
    files = os.listdir(_PASTEBIN_JSON_PATH)
    if files:
        for name in files:
            with open(os.path.join(_PASTEBIN_JSON_PATH, name), 'r') as f:
                PASTEBINS.append(json.load(f))
    else:
        for name in pkg_resources.resource_listdir('pastetray',
                                                   'default_pastebins'):
            data = pkg_resources.resource_string(
                'pastetray', 'default_pastebins/' + name
            )
            PASTEBINS.append(json.loads(data.decode('utf-8')))


@utils.debug
def unload():
    """Save the pastebin list and the list of recent pastes."""
    with open(_PASTEBIN_JSON_PATH, 'w') as f:
        json.dump(PASTEBINS, f)

    with open(_RECENT_PASTE_PATH, 'w') as f:
        for url in RECENT_PASTES:
            print(url, file=f)
