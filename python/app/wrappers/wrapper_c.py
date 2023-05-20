from typing import TYPE_CHECKING

from app.buffer_parser import Signature
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperC(ArgWrapperBase):
    def _wrap_args(self, signature: Signature, buffer: 'Buffer') -> None:
        '''
        Applies wrap of type C:
        method_invocation(a,
                          b,
                          c)
        '''
        buffer[signature.rows.start] = signature.beginning + signature.args[0] + ','
        arg_offset = self._get_offset(len(signature.beginning))
        for arg_index in range(1, len(signature.args)):
            arg_line = _build_arg_line(
                signature.args[arg_index],
                arg_offset,
                ',' if arg_index < len(signature.args) - 1 else signature.ending)
            buffer[signature.rows.start + arg_index] = arg_line

    def _recognized(self, signature: Signature, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a type C wrapper
        '''
        return signature.rows.end - signature.rows.start == len(signature.args) - 1

    def _lines_needed(self, args_count: int) -> int:
        return 1 if args_count == 0 else args_count

def _build_arg_line(arg: str, arg_offset: str, ending: str) -> str:
    return arg_offset + arg + ending
