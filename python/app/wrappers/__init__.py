from .wrapper_sequence import WrapperSequence
from .wrapper_a import ArgWrapperA
from .wrapper_b import ArgWrapperB
from .wrapper_c import ArgWrapperC
from .wrapper_d import ArgWrapperD
from .wrapper_nowrap import ArgWrapperNoWrap

def init_wrappers(indent: int) -> WrapperSequence:
    return WrapperSequence([
        ArgWrapperNoWrap(indent),
        ArgWrapperA(indent),
        ArgWrapperB(indent),
        ArgWrapperC(indent),
        ArgWrapperD(indent),
    ])
