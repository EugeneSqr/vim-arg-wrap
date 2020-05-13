#pylint:disable=import-error
from itertools import chain, repeat
from vim import current, eval as vim_eval

from wrappers import (
    ArgsWrapperA,
    ArgsWrapperNoWrap,
)

def _get_wrappers_iterator(indent):
    return iter(chain.from_iterable(repeat([
        ArgsWrapperA(indent),
        ArgsWrapperNoWrap(indent),
    ])))

_wrappers = _get_wrappers_iterator(int(vim_eval('&g:tabstop')))

def wrap_args():
    next(_wrappers).wrap_args(current.window.cursor, current.buffer)
