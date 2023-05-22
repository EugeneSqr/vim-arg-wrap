from app.types import VimBuffer
from app.buffer_parser import Signature
from .wrapper_base import ArgWrapperBase

class ArgWrapperB(ArgWrapperBase):
    def _wrap_args(self, signature: Signature, buffer: VimBuffer) -> None:
        '''
        Applies wrap of type B:
        method_invocation(
           a,
           b,
           c)
        '''
        buffer[signature.rows.start] = signature.beginning
        range_offset = self._get_offset() + self._get_offset(signature.rows.start_indent)
        for arg_index, arg in enumerate(signature.args):
            arg_line = _build_arg_line(
                arg,
                range_offset,
                ',' if arg_index < len(signature.args) - 1 else signature.ending)
            buffer[signature.rows.start + arg_index + 1] = arg_line

    def _recognized(self, signature: Signature, buffer: VimBuffer) -> bool:
        '''
        Determines if the provided range is wrapped with a type B wrapper
        '''
        return signature.rows.end - signature.rows.start == len(signature.args)

    def _lines_needed(self, args_count: int) -> int:
        return args_count + 1

def _build_arg_line(arg: str, range_offset: str, ending: str) -> str:
    return range_offset + arg + ending
