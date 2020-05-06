"""
Converts between wrap types
Form A: no wrap at all
method_invocation(a, b, c)

Form B: single line wrap
method_invocation(
    a, b, c)
"""

from buffer_parser import parse_at_cursor

class ArgsWrapper():
    def __init__(self, indent):
        self._indent = indent

    def wrap_args(self, cursor, buffer):
        parsed_range = parse_at_cursor(cursor, buffer)
        first_line = parsed_range.beginning
        second_line = (_get_offset(parsed_range.indent) + _get_offset(self._indent) +
                       parsed_range.args + parsed_range.ending)
        buffer[parsed_range.start_row_index] = first_line
        buffer.append(second_line, parsed_range.start_row_index + 1)

def _get_offset(indent):
    return ' '*indent
