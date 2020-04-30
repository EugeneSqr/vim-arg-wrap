from vim import current

from buffer_search import find_args_range

def make_replacement():
    row, col = current.window.cursor
    print(find_args_range(row, col, current.buffer))

