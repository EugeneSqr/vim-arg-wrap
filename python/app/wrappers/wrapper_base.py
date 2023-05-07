from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod

from app.buffer_parser import parse_at_cursor, ParsedRange
from app.types import Cursor

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class ArgWrapperBase(ABC):
    def __init__(self, indent: int):
        self._indent = indent

    def wrap_args(self, cursor: Cursor, buffer: 'Buffer') -> None:
        parsed_range = parse_at_cursor(cursor, buffer)
        if _can_wrap(parsed_range):
            self._allocate_lines(parsed_range, buffer)
            self._wrap_args(parsed_range, buffer)

    def recognized(self, cursor: Cursor, buffer: 'Buffer') -> bool:
        parsed_range = parse_at_cursor(cursor, buffer)
        return _can_wrap(parsed_range) and self._recognized(parsed_range, buffer)

    @abstractmethod
    def _wrap_args(self, parsed_range: ParsedRange, buffer: 'Buffer') -> None:
        pass

    @abstractmethod
    def _recognized(self, parsed_range: ParsedRange, buffer: 'Buffer') -> bool:
        pass

    @abstractmethod
    def _lines_needed(self, args_count: int) -> int:
        pass

    # TODO: consider removing Optional
    def _get_offset(self, indent: Optional[int] = None) -> str:
        return ' '*(self._indent if indent is None else indent)

    def _allocate_lines(self, parsed_range: ParsedRange, buffer: 'Buffer') -> None:
        lines_occupied = parsed_range.end_row_index - parsed_range.start_row_index + 1
        lines_needed = self._lines_needed(len(parsed_range.args))
        if lines_needed >= lines_occupied:
            buffer.append(['']*(lines_needed - lines_occupied), parsed_range.start_row_index)
        else:
            del buffer[
                parsed_range.start_row_index:
                parsed_range.start_row_index + lines_occupied - lines_needed
            ]

def _can_wrap(parsed_range: ParsedRange) -> bool:
    return len(parsed_range.args) > 0

def _remove_range(parsed_range: ParsedRange, buffer: 'Buffer') -> None:
    del buffer[parsed_range.start_row_index:parsed_range.end_row_index + 1]
