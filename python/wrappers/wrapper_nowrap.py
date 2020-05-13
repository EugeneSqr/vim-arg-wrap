from .wrapper_base import ArgsWrapperBase

# TODO: add unit tests
class ArgsWrapperNoWrap(ArgsWrapperBase):
    """
    Converts block of text to its unwrapped form.
    invoke_method(
        a, b, c)
    invoke_method(
        a,
        b,
        c)
    invoke_method(a,
                  b,
                  c)
    all become
    invoke_method(a, b, c)
    """

    def _wrap_args(self, cursor, buffer):
        print('Wrap Args from nowrap')
        # TODO: implement me
        # pass

    def _can_wrap(self, cursor, buffer):
        # TODO: proper implementation
        return True
