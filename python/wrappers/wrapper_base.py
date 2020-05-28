from abc import ABC, abstractmethod

from buffer_parser import parse_at_cursor

class ArgWrapperBase(ABC):
    def __init__(self, indent):
        self._next_wrapper = None
        self._indent = indent

    def set_next_wrapper(self, value):
        self._next_wrapper = value
        return self._next_wrapper

    def wrap_args(self, cursor, buffer):
        parsed_range = parse_at_cursor(cursor, buffer)
        if self._can_wrap(parsed_range):
            self._wrap_args(parsed_range, buffer)
        elif self._next_wrapper is not None:
            self._next_wrapper.wrap_args(cursor, buffer)
        else:
            pass

    @abstractmethod
    def _wrap_args(self, parsed_range, buffer):
        raise NotImplementedError('You must implement this method.')

    @abstractmethod
    def _can_wrap(self, parsed_range):
        raise NotImplementedError('You must implement this method.')

    def _get_next_wrapper(self):
        return self._next_wrapper

    def _get_offset(self, indent=None):
        return ' '*(self._indent if indent is None else indent)
