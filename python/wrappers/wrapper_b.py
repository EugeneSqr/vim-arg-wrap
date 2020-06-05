from .wrapper_base import ArgWrapperBase

class ArgWrapperB(ArgWrapperBase):
    def _wrap_args(self, parsed_range, buffer):
        '''
        Applies wrap of type B:
        method_invocation(
           a,
           b,
           c)
        '''
        buffer.append(parsed_range.beginning, parsed_range.start_row_index)
        range_offset = self._get_offset() + self._get_offset(parsed_range.start_row_indent)
        for arg_index, arg in enumerate(parsed_range.args):
            arg_line = _build_arg_line(
                arg,
                range_offset,
                ',' if arg_index < len(parsed_range.args) - 1 else parsed_range.ending)
            buffer.append(arg_line, parsed_range.start_row_index + arg_index + 1)

    def _recognized(self, parsed_range):
        '''
        Determines if the provided range is wrapped with a type B wrapper
        '''
        return parsed_range.end_row_index - parsed_range.start_row_index == len(parsed_range.args)

def _build_arg_line(arg, range_offset, ending):
    return range_offset + arg + ending
