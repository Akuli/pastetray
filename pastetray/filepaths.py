"""The filepaths."""
import os
import platform
import appdirs

# Windows uses CapsWords for application names, but most other operating
# systems don't.
_app = 'PasteTray' if platform.system() == 'Windows' else 'pastetray'

user_cache_dir = appdirs.user_cache_dir(_app)
user_config_dir = appdirs.user_config_dir(_app)
os.makedirs(user_cache_dir, exist_ok=True)
os.makedirs(user_config_dir, exist_ok=True)
