from typing import TYPE_CHECKING, List, Optional

from app.types import Cursor
from .wrapper_base import ArgWrapperBase

if TYPE_CHECKING:
    from vim import Buffer #pylint:disable=import-error

class WrapperSequence():
    def __init__(self, wrappers: List[ArgWrapperBase]):
        self._wrappers = wrappers

    def wrap_next(self, cursor: Cursor, buffer: 'Buffer') -> None:
        current_wrapper_index = self._get_current_wrapper_index(cursor, buffer)
        if current_wrapper_index is None:
            return

        self._get_next_wrapper(current_wrapper_index).wrap_args(cursor, buffer)

    def wrap_prev(self, cursor: Cursor, buffer: 'Buffer') -> None:
        current_wrapper_index = self._get_current_wrapper_index(cursor, buffer)
        if current_wrapper_index is None:
            return
        self._get_prev_wrapper(current_wrapper_index).wrap_args(cursor, buffer)

    def _get_current_wrapper_index(self, cursor: Cursor, buffer: 'Buffer') -> Optional[int]:
        recognized_indexes = (index for index, wrapper in enumerate(self._wrappers)
                              if wrapper.recognized(cursor, buffer))
        return next(recognized_indexes, None)

    def _get_next_wrapper(self, index: int) -> ArgWrapperBase:
        return self._wrappers[(index + 1) % len(self._wrappers)]

    def _get_prev_wrapper(self, index: int) -> ArgWrapperBase:
        return self._wrappers[(index - 1) % len(self._wrappers)]
