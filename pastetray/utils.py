"""Handy utilities to make writing this program easier."""
import contextlib
import functools


def debug(func):
    """Print the name of func when it's called."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('%s.%s()' % (func.__module__, func.__name__))
        return func(*args, **kwargs)
    return wrapper


@contextlib.contextmanager
def disconnected(obj, signal, func, *user_data):
    """Disconnect a GObject signal temporarily."""
    obj.disconnect_by_func(func)
    yield
    obj.connect(signal, func, *user_data)
