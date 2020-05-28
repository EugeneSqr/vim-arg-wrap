from .wrapper_base import ArgWrapperBase

class ArgWrapperA(ArgWrapperBase):
    """
    Applies wrap of type A:
    method_invocation(
        a, b, c)
    """
    def _wrap_args(self, parsed_range, buffer):
        first_line = parsed_range.beginning
        second_line = (self._get_offset(parsed_range.indent) + self._get_offset() +
                       ', '.join(parsed_range.args) + parsed_range.ending)
        buffer[parsed_range.start_row_index] = first_line
        buffer.append(second_line, parsed_range.start_row_index + 1)

    def _can_wrap(self, parsed_range):
        # TODO: proper implementation
        return True
