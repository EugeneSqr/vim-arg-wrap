from buffer_parser import parse_at_cursor

from .wrapper_base import ArgsWrapperBase

class ArgsWrapperA(ArgsWrapperBase):
    # TODO: fix description, move types to different files
    """
    Converts between wrap types
    Form A: no wrap at all
    method_invocation(a, b, c)

    Form B: single line wrap
    method_invocation(
        a, b, c)
    """
    def _wrap_args(self, cursor, buffer):
        print('wrap args from A')
        parsed_range = parse_at_cursor(cursor, buffer)
        first_line = parsed_range.beginning
        second_line = (_get_offset(parsed_range.indent) + _get_offset(self._indent) +
                       ', '.join(parsed_range.args) + parsed_range.ending)
        buffer[parsed_range.start_row_index] = first_line
        buffer.append(second_line, parsed_range.start_row_index + 1)
    def _can_wrap(self, cursor, buffer):
        # TODO: proper implementation
        return True

def _get_offset(indent):
    # TODO: consider moving to base class
    return ' '*indent
