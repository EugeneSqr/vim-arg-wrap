#pylint:disable=import-error
from vim import current, eval as vim_eval

from wrappers import (
    WrapperSequence,
    ArgWrapperA,
    ArgWrapperB,
    ArgWrapperC,
    ArgWrapperNoWrap,
)


indent = int(vim_eval('&g:tabstop'))
_wrappers = WrapperSequence([
    ArgWrapperNoWrap(indent),
    ArgWrapperA(indent),
    ArgWrapperB(indent),
    ArgWrapperC(None),
])

def wrap_args():
    _wrappers.wrap_next(current.window.cursor, current.buffer)

def wrap_args_back():
    _wrappers.wrap_prev(current.window.cursor, current.buffer)
