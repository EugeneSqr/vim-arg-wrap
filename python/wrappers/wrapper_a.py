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

    def _recognized(self, parsed_range, buffer):
        '''
        Determines if the provided range is wrapped with a type A wrapper
        '''
        wraps_count = parsed_range.end_row_index - parsed_range.start_row_index
        return wraps_count == 1 and not _has_first_argument_in_start_row(parsed_range, buffer)

def _has_first_argument_in_start_row(parsed_range, buffer):
    if not parsed_range.args:
        return False

    start_row = buffer[parsed_range.start_row_index]
    if len(start_row) < len(parsed_range.beginning) + len(parsed_range.args[0]):
        return False

    ending_start_index = len(parsed_range.beginning)
    ending_end_index = ending_start_index + len(parsed_range.args[0]) - 1
    return start_row[ending_start_index:ending_end_index + 1] == parsed_range.args[0]
