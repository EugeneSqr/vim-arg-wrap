from .wrapper_base import ArgWrapperBase

class ArgWrapperA(ArgWrapperBase):
    def _wrap_args(self, parsed_range, buffer):
        '''
        Applies wrap of type A:
        method_invocation(
            a, b, c)
        '''
        second_line = (self._get_offset(parsed_range.start_row_indent) + self._get_offset() +
                       ', '.join(parsed_range.args) + parsed_range.ending)
        buffer.append(parsed_range.beginning, parsed_range.start_row_index)
        buffer.append(second_line, parsed_range.start_row_index + 1)

    def _recognized(self, parsed_range):
        '''
        Determines if the provided range is wrapped with a type A wrapper
        '''
        return parsed_range.end_row_index - parsed_range.start_row_index == 1
