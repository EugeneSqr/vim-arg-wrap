from .wrapper_base import ArgWrapperBase

# TODO: add unit tests
class ArgWrapperB(ArgWrapperBase):
    '''
    Applies wrap of type B:
    method_invocation(
       a,
       b,
       c)
    '''
    def _wrap_args(self, parsed_range, buffer):
        self._remove_range(parsed_range, buffer)
        buffer[parsed_range.start_row_index] = parsed_range.beginning
        range_offset = self._get_offset(parsed_range.start_row_indent)
        for arg_index, arg in enumerate(parsed_range.args):
            arg_line = self._build_arg_line(
                arg,
                range_offset,
                ',' if arg_index < len(parsed_range.args) - 1 else parsed_range.ending)
            buffer.append(arg_line, parsed_range.start_row_index + arg_index + 1)

    def _build_arg_line(self, arg, range_offset, ending):
        return self._get_offset() + range_offset + arg + ending
