#pylint:disable=import-error
from itertools import chain, repeat
from vim import current, eval as vim_eval

from wrappers import (
    ArgWrapperA,
    ArgWrapperNoWrap,
)

def _get_wrappers_iterator(indent):
    return iter(chain.from_iterable(repeat([
        ArgWrapperA(indent),
        ArgWrapperNoWrap(indent),
    ])))

_wrappers = _get_wrappers_iterator(int(vim_eval('&g:tabstop')))

def wrap_args():
    next(_wrappers).wrap_args(current.window.cursor, current.buffer)
