from abc import ABC, abstractmethod

class ArgsWrapperBase(ABC):
    def __init__(self, indent):
        self._next_wrapper = None
        self._indent = indent

    def set_next_wrapper(self, value):
        self._next_wrapper = value
        return self._next_wrapper

    def wrap_args(self, cursor, buffer):
        if self._can_wrap(cursor, buffer):
            self._wrap_args(cursor, buffer)
        elif self._next_wrapper is not None:
            self._next_wrapper.wrap_args(cursor, buffer)
        else:
            pass

    @abstractmethod
    def _wrap_args(self, cursor, buffer):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def _can_wrap(self, cursor, buffer):
        # TODO: accept parsed_range instead of cursor and buffer
        raise NotImplementedError("You should implement this method.")

    def _get_next_wrapper(self):
        return self._next_wrapper

    def _get_indent(self):
        return self._indent
