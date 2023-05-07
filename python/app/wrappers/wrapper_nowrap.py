from typing import TYPE_CHECKING

from app.buffer_parser import ParsedRange
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperNoWrap(ArgWrapperBase):
    def _wrap_args(self, parsed_range: ParsedRange, buffer: 'Buffer') -> None:
        '''
        Converts block of text to its nowrapped form:
        invoke_method(a, b, c)
        '''
        buffer[parsed_range.start_row_index] = (parsed_range.beginning +
                                                ', '.join(parsed_range.args) +
                                                parsed_range.ending)

    def _recognized(self, parsed_range: ParsedRange, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a nowrap wrapper
        '''
        return parsed_range.end_row_index - parsed_range.start_row_index == 0

    def _lines_needed(self, args_count: int) -> int:
        return 1
