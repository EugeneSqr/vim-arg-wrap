#pylint:disable=import-error
from vim import current

import args_wrapper

def wrap_args():
    args_wrapper.wrap_args(current.window.cursor, current.buffer)
