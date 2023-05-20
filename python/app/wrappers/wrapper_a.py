from typing import TYPE_CHECKING

from app.buffer_parser import Signature
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperA(ArgWrapperBase):
    def _wrap_args(self, signature: Signature, buffer: 'Buffer') -> None:
        '''
        Applies wrap of type A:
        method_invocation(
            a, b, c)
        '''
        second_line = (self._get_offset(signature.start_row_indent) + self._get_offset() +
                       ', '.join(signature.args) + signature.ending)
        buffer[signature.rows.start] = signature.beginning
        buffer[signature.rows.start + 1] = second_line

    def _recognized(self, signature: Signature, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a type A wrapper
        '''
        wraps_count = signature.rows.end - signature.rows.start
        return wraps_count == 1 and not _has_first_argument_in_start_row(signature, buffer)

    def _lines_needed(self, args_count: int) -> int:
        return 1 if args_count == 0 else 2

def _has_first_argument_in_start_row(signature: Signature, buffer: 'Buffer') -> bool:
    if not signature.args:
        return False

    start_row = buffer[signature.rows.start]
    if len(start_row) < len(signature.beginning) + len(signature.args[0]):
        return False

    ending_start_index = len(signature.beginning)
    ending_end_index = ending_start_index + len(signature.args[0]) - 1
    return start_row[ending_start_index:ending_end_index + 1] == signature.args[0]
