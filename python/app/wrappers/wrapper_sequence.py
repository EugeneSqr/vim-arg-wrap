from typing import List, Optional

from app.types import VimCursor, VimBuffer
from .wrapper_base import ArgWrapperBase

class WrapperSequence():
    def __init__(self, wrappers: List[ArgWrapperBase]):
        self._wrappers = wrappers

    def wrap_next(self, cursor: VimCursor, buffer: VimBuffer) -> None:
        current_wrapper_index = self._get_current_wrapper_index(cursor, buffer)
        if current_wrapper_index is None:
            return

        self._get_next_wrapper(current_wrapper_index).wrap_args(cursor, buffer)

    def wrap_prev(self, cursor: VimCursor, buffer: VimBuffer) -> None:
        current_wrapper_index = self._get_current_wrapper_index(cursor, buffer)
        if current_wrapper_index is None:
            return
        self._get_prev_wrapper(current_wrapper_index).wrap_args(cursor, buffer)

    def _get_current_wrapper_index(self, cursor: VimCursor, buffer: VimBuffer) -> Optional[int]:
        recognized_indexes = (index for index, wrapper in enumerate(self._wrappers)
                              if wrapper.recognized(cursor, buffer))
        return next(recognized_indexes, None)

    def _get_next_wrapper(self, index: int) -> ArgWrapperBase:
        return self._wrappers[(index + 1) % len(self._wrappers)]

    def _get_prev_wrapper(self, index: int) -> ArgWrapperBase:
        return self._wrappers[(index - 1) % len(self._wrappers)]
