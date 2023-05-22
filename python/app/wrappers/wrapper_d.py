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
        raise NotImplementedError()

    def _recognized(self, signature: Signature, buffer: VimBuffer) -> bool:
        '''
        Determines if the provided range is wrapped with a D wrapper
        '''
        raise NotImplementedError()

    def _lines_needed(self, args_count: int) -> int:
        raise NotImplementedError()
