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
    get_buffer_indent,
    get_line_indent,
)

def wrap_args(cursor, buffer):
    (start_row, start_col), (end_row, _) = get_args_range(cursor, buffer)
    line = buffer[start_row:end_row + 1][0]
    line_indent = get_line_indent(line)
    buffer_indent = get_buffer_indent(buffer)
    line_start = line[:start_col]
    line_end = line_indent + buffer_indent + line[start_col:]
    buffer[start_row] = line_start
    buffer.append(line_end, start_row + 1)
