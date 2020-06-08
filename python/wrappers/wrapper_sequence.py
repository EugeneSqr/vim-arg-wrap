class WrapperSequence():
    def __init__(self, wrappers):
        self._wrappers = wrappers

    def wrap_next(self, cursor, buffer):
        current_wrapper_index = self._get_current_wrapper_index(cursor, buffer)
        if current_wrapper_index is None:
            return

        self._get_next_wrapper(current_wrapper_index).wrap_args(cursor, buffer)

    def wrap_prev(self, cursor, buffer):
        current_wrapper_index = self._get_current_wrapper_index(cursor, buffer)
        if current_wrapper_index is None:
            return
        self._get_prev_wrapper(current_wrapper_index).wrap_args(cursor, buffer)

    def _get_current_wrapper_index(self, cursor, buffer):
        recognized_indexes = (wrapper_index
                              for wrapper_index, _ in enumerate(self._wrappers)
                              if _.recognized(cursor, buffer))
        return next(recognized_indexes, None)

    def _get_next_wrapper(self, index):
        return self._wrappers[(index + 1) % len(self._wrappers)]

    def _get_prev_wrapper(self, index):
        return self._wrappers[(index - 1) % len(self._wrappers)]
