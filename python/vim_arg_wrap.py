from vim import current

from buffer_search import find_args_range

def make_replacement():
    start, end = find_args_range(current.window.cursor, current.buffer)
    print('>>', start, end)
