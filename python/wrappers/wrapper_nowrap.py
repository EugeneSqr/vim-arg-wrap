from .wrapper_base import ArgWrapperBase

class ArgWrapperNoWrap(ArgWrapperBase):
    """
    Converts block of text to its nowrapped form:
    invoke_method(a, b, c)
    """
    def _wrap_args(self, parsed_range, buffer):
        buffer[parsed_range.start_row_index] = (parsed_range.beginning +
                                                ', '.join(parsed_range.args) +
                                                parsed_range.ending)
        del buffer[parsed_range.start_row_index + 1:parsed_range.end_row_index + 1]
