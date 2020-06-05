from abc import ABC, abstractmethod

from buffer_parser import parse_at_cursor

class ArgWrapperBase(ABC):
    def __init__(self, indent):
        self._indent = indent

    def wrap_args(self, cursor, buffer):
        parsed_range = parse_at_cursor(cursor, buffer)
        if _can_wrap(parsed_range):
            _remove_range(parsed_range, buffer)
            self._wrap_args(parsed_range, buffer)

    def recognized(self, cursor, buffer):
        parsed_range = parse_at_cursor(cursor, buffer)
        return _can_wrap(parsed_range) and self._recognized(parsed_range)

    @abstractmethod
    def _wrap_args(self, parsed_range, buffer):
        raise NotImplementedError('Provide implementation in a derived class')

    @abstractmethod
    def _recognized(self, parsed_range):
        raise NotImplementedError('Provide implementation in a derived class')

    def _get_offset(self, indent=None):
        return ' '*(self._indent if indent is None else indent)

def _can_wrap(parsed_range):
    return parsed_range is not None and bool(parsed_range.args)

def _remove_range(parsed_range, buffer):
    del buffer[parsed_range.start_row_index:parsed_range.end_row_index + 1]
