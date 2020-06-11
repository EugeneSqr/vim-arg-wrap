from .wrapper_base import ArgWrapperBase

class ArgWrapperC(ArgWrapperBase):
    def _wrap_args(self, parsed_range, buffer):
        '''
        Applies wrap of type C:
        method_invocation(a,
                          b,
                          c)
        '''
        buffer[parsed_range.start_row_index] = parsed_range.beginning + parsed_range.args[0] + ','
        arg_offset = self._get_offset(len(parsed_range.beginning))
        for arg_index in range(1, len(parsed_range.args)):
            arg_line = _build_arg_line(
                parsed_range.args[arg_index],
                arg_offset,
                ',' if arg_index < len(parsed_range.args) - 1 else parsed_range.ending)
            buffer[parsed_range.start_row_index + arg_index] = arg_line

    def _recognized(self, parsed_range, buffer):
        '''
        Determines if the provided range is wrapped with a type C wrapper
        '''
        return (parsed_range.end_row_index - parsed_range.start_row_index ==
                len(parsed_range.args) - 1)

    def _lines_needed(self, args_count):
        return 1 if args_count == 0 else args_count

def _build_arg_line(arg, arg_offset, ending):
    return arg_offset + arg + ending
