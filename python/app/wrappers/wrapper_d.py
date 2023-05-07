from typing import TYPE_CHECKING

from app.buffer_parser import ParsedRange
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperD(ArgWrapperBase):
    def _wrap_args(self, parsed_range: ParsedRange, buffer: 'Buffer') -> None:
        '''
        Applies wrap of type D:
        invoke_method(
            a,
            b,
            c,
        )
        '''
        raise NotImplementedError()

    def _recognized(self, parsed_range: ParsedRange, buffer: 'Buffer') -> bool:
        '''
        Determines if the provided range is wrapped with a D wrapper
        '''
        raise NotImplementedError()

    def _lines_needed(self, args_count: int) -> int:
        raise NotImplementedError()
