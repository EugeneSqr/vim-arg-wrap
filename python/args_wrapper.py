"""
Converts between wrap types
Form A: no wrap at all
method_invocation(a, b, c)

Form B: single line wrap
method_invocation(
    a, b, c)
"""

from buffer_search import (
    get_args_range,
    get_line_indent,
)

class ArgsWrapper():
    def __init__(self, indent):
        self._indent = indent

    def wrap_args(self, cursor, buffer):
        (start_row, start_col), (end_row, _) = get_args_range(cursor, buffer)
        line = buffer[start_row:end_row + 1][0]
        line_start = line[:start_col]
        line_end = _get_offset(get_line_indent(line)) + _get_offset(self._indent) + line[start_col:]
        buffer[start_row] = line_start
        buffer.append(line_end, start_row + 1)

def _get_offset(indent):
    return ' '*indent
