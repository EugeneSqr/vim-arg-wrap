from vim import current

from args_wrapper import wrap_args

def make_replacement():
    wrap_args(current.window.cursor, current.buffer)
