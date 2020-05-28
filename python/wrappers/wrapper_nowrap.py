from .wrapper_base import ArgWrapperBase

# TODO: add unit tests
class ArgWrapperNoWrap(ArgWrapperBase):
    """
    Converts block of text to its nowrapped form:
    invoke_method(a, b, c)
    """

    def _wrap_args(self, parsed_range, buffer):
        print('Wrap Args from nowrap')
        # TODO: implement me
        # pass
