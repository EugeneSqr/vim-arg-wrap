from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod

from app.buffer_parser import signature_at_cursor, Signature
from app.types import Cursor

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperBase(ABC):
    def __init__(self, indent: int):
        self._indent = indent

    def wrap_args(self, cursor: Cursor, buffer: 'Buffer') -> None:
        signature = signature_at_cursor(cursor, buffer)
        if _can_wrap(signature):
            self._allocate_lines(signature, buffer)
            self._wrap_args(signature, buffer)

    def recognized(self, cursor: Cursor, buffer: 'Buffer') -> bool:
        signature = signature_at_cursor(cursor, buffer)
        return _can_wrap(signature) and self._recognized(signature, buffer)

    @abstractmethod
    def _wrap_args(self, signature: Signature, buffer: 'Buffer') -> None:
        pass

    @abstractmethod
    def _recognized(self, signature: Signature, buffer: 'Buffer') -> bool:
        pass

    @abstractmethod
    def _lines_needed(self, args_count: int) -> int:
        pass

    # TODO: consider removing Optional
    def _get_offset(self, indent: Optional[int] = None) -> str:
        return ' '*(self._indent if indent is None else indent)

    def _allocate_lines(self, signature: Signature, buffer: 'Buffer') -> None:
        lines_occupied = signature.rows.end - signature.rows.start + 1
        lines_needed = self._lines_needed(len(signature.args))
        if lines_needed >= lines_occupied:
            buffer.append(['']*(lines_needed - lines_occupied), signature.rows.start)
        else:
            del buffer[
                signature.rows.start:
                signature.rows.start + lines_occupied - lines_needed
            ]

def _can_wrap(signature: Signature) -> bool:
    return len(signature.args) > 0

def _remove_range(signature: Signature, buffer: 'Buffer') -> None:
    del buffer[signature.rows.start:signature.rows.end + 1]