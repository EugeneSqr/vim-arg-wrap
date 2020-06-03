from .wrapper_base import ArgWrapperBase

class ArgWrapperC(ArgWrapperBase):
    '''
    Applies wrap of type C:
    method_invocation(a,
                      b,
                      c)
    '''
    def _wrap_args(self, parsed_range, buffer):
        buffer.append(
            parsed_range.beginning + parsed_range.args[0] + ',',
            parsed_range.start_row_index)
        arg_offset = self._get_offset(len(parsed_range.beginning))
        for arg_index in range(1, len(parsed_range.args)):
            arg_line = self._build_arg_line(
                parsed_range.args[arg_index],
                arg_offset,
                ',' if arg_index < len(parsed_range.args) - 1 else parsed_range.ending)
            buffer.append(arg_line, parsed_range.start_row_index + arg_index)

    def _build_arg_line(self, arg, arg_offset, ending):
        return arg_offset + arg + ending
