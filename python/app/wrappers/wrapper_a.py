from typing import TYPE_CHECKING

from app.buffer_parser import ParsedRange
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperA(ArgWrapperBase):
    def _wrap_args(self, parsed_range: ParsedRange, buffer: 'Buffer') -> None:
        '''
        Applies wrap of type A:
        method_invocation(
            a, b, c)
        '''
        second_line = (self._get_offset(parsed_range.start_row_indent) + self._get_offset() +
                       ', '.join(parsed_range.args) + parsed_range.ending)
        buffer[parsed_range.start_row_index] = parsed_range.beginning
        buffer[parsed_range.start_row_index + 1] = second_line

    def _recognized(self, parsed_range: ParsedRange, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a type A wrapper
        '''
        wraps_count = parsed_range.end_row_index - parsed_range.start_row_index
        return wraps_count == 1 and not _has_first_argument_in_start_row(parsed_range, buffer)

    def _lines_needed(self, args_count: int) -> int:
        return 1 if args_count == 0 else 2

def _has_first_argument_in_start_row(parsed_range: ParsedRange, buffer: 'Buffer') -> bool:
    if not parsed_range.args:
        return False

    start_row = buffer[parsed_range.start_row_index]
    if len(start_row) < len(parsed_range.beginning) + len(parsed_range.args[0]):
        return False

    ending_start_index = len(parsed_range.beginning)
    ending_end_index = ending_start_index + len(parsed_range.args[0]) - 1
    return start_row[ending_start_index:ending_end_index + 1] == parsed_range.args[0]
