from typing import TYPE_CHECKING

from app.buffer_parser import Signature
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperNoWrap(ArgWrapperBase):
    def _wrap_args(self, signature: Signature, buffer: 'Buffer') -> None:
        '''
        Converts block of text to its nowrapped form:
        invoke_method(a, b, c)
        '''
        buffer[signature.rows.start] = (
            signature.beginning + ', '.join(signature.args) + signature.ending
        )

    def _recognized(self, signature: Signature, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a nowrap wrapper
        '''
        return signature.rows.end - signature.rows.start == 0

    def _lines_needed(self, args_count: int) -> int:
        return 1
