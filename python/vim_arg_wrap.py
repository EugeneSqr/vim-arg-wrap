#pylint:disable=import-error
from vim import current, eval as vim_eval

from wrappers import (
    WrapperSequence,
    ArgWrapperA,
    ArgWrapperB,
    ArgWrapperNoWrap,
)


indent = int(vim_eval('&g:tabstop'))
_wrappers = WrapperSequence([
    ArgWrapperNoWrap(indent),
    ArgWrapperA(indent),
    ArgWrapperB(indent),
])

def wrap_args():
    _wrap_args(_wrappers.get_next_wrapper())

def wrap_args_back():
    _wrap_args(_wrappers.get_prev_wrapper())

def _wrap_args(wrapper):
    return wrapper.wrap_args(current.window.cursor, current.buffer)
