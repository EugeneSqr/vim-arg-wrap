class WrapperSequence():
    def __init__(self, wrappers):
        self._wrappers = wrappers
        self._index = 0

    def wrap_next(self, cursor, buffer):
        pass

    def wrap_prev(self, cursor, buffer):
        pass

    # TODO: obsolete
    def get_next_wrapper(self):
        self._index = (self._index + 1) % len(self._wrappers)
        return self._wrappers[self._index]

    # TODO: obsolete
    def get_prev_wrapper(self):
        self._index = (self._index - 1) % len(self._wrappers)
        return self._wrappers[self._index]
