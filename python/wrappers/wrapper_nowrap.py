from .wrapper_base import ArgWrapperBase

# TODO: add unit tests
class ArgWrapperNoWrap(ArgWrapperBase):
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
