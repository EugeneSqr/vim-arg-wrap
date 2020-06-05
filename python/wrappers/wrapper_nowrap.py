from .wrapper_base import ArgWrapperBase

class ArgWrapperNoWrap(ArgWrapperBase):
    def _wrap_args(self, parsed_range, buffer):
        '''
        Converts block of text to its nowrapped form:
        invoke_method(a, b, c)
        '''
        buffer.append(
            parsed_range.beginning + ', '.join(parsed_range.args) + parsed_range.ending,
            parsed_range.start_row_index)

    def _recognized(self, parsed_range):
        '''
        Determines if the provided range is wrapped with a nowrap wrapper
        '''
        return parsed_range.end_row_index - parsed_range.start_row_index == 0
