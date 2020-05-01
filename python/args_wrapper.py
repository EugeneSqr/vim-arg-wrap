"""
Converts between wrap types
Form A: no wrap at all
method_invocation(a, b, c)

Form B: single line wrap
method_invocation(
    a, b, c)
"""

from buffer_search import get_args_range

def wrap_args(cursor, buffer):
    (start_row, start_col), (end_row, _) = get_args_range(cursor, buffer)
    line = buffer[start_row:end_row + 1]
    buffer.append('aaaa', start_row)
