from vim import current, eval as vim_eval #pylint:disable=import-error

from .wrappers import init_wrappers


# TODO: add typing
# TODO: add dataclasses
indent = int(vim_eval('&g:tabstop'))
_wrappers = init_wrappers(indent)

def wrap_args() -> None:
    _wrappers.wrap_next(current.window.cursor, current.buffer)

def wrap_args_back() -> None:
    _wrappers.wrap_prev(current.window.cursor, current.buffer)
