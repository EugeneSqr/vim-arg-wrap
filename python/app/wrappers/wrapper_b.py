from typing import TYPE_CHECKING

from app.buffer_parser import ParsedRange
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperB(ArgWrapperBase):
    def _wrap_args(self, parsed_range: ParsedRange, buffer: 'Buffer') -> None:
        '''
        Applies wrap of type B:
        method_invocation(
           a,
           b,
           c)
        '''
        buffer[parsed_range.start_row_index] = parsed_range.beginning
        range_offset = self._get_offset() + self._get_offset(parsed_range.start_row_indent)
        for arg_index, arg in enumerate(parsed_range.args):
            arg_line = _build_arg_line(
                arg,
                range_offset,
                ',' if arg_index < len(parsed_range.args) - 1 else parsed_range.ending)
            buffer[parsed_range.start_row_index + arg_index + 1] = arg_line

    def _recognized(self, parsed_range: ParsedRange, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a type B wrapper
        '''
        return parsed_range.end_row_index - parsed_range.start_row_index == len(parsed_range.args)

    def _lines_needed(self, args_count: int) -> int:
        return args_count + 1

def _build_arg_line(arg: str, range_offset: str, ending: str) -> str:
    return range_offset + arg + ending
