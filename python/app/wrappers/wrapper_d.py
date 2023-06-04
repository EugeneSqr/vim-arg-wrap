from app.types import VimBuffer
from app.buffer_parser import Signature
from .wrapper_base import ArgWrapperBase

class ArgWrapperD(ArgWrapperBase):
    def _wrap_args(self, signature: Signature, buffer: VimBuffer) -> None:
        '''
        Applies wrap of type D:
        invoke_method(
            a,
            b,
            c,
        )
        '''
        buffer[signature.rows.start] = signature.beginning
        start_offset = self._get_offset(signature.rows.start_indent)
        arg_offset = self._get_offset() + start_offset
        for arg_index, arg in enumerate(signature.args):
            buffer[signature.rows.start + arg_index + 1] = arg_offset + arg + ','
        buffer[signature.rows.start + len(signature.args) + 1] = start_offset + signature.ending

    def _recognized(self, signature: Signature, buffer: VimBuffer) -> bool:
        '''
        Determines if the provided range is wrapped with a D wrapper
        '''
        return signature.rows.end - signature.rows.start == len(signature.args) + 1

    def _lines_needed(self, args_count: int) -> int:
        return 1 if args_count == 0 else args_count + 2
