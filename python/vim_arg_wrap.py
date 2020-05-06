#pylint:disable=import-error
from vim import current, eval as vim_eval

from args_wrapper import ArgsWrapper

def wrap_args():
    indent = int(vim_eval('&g:tabstop'))
    ArgsWrapper(indent).wrap_args(current.window.cursor, current.buffer)
