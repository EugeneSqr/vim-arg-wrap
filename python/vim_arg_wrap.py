#pylint:disable=import-error
from vim import current, eval as vim_eval

from wrappers import ArgsWrapperA

def wrap_args():
    indent = int(vim_eval('&g:tabstop'))
    ArgsWrapperA(indent).wrap_args(current.window.cursor, current.buffer)
