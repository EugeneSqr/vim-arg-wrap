from typing import List, Tuple, TypeVar

from app.types import VimBuffer

class Window:
    cursor: Tuple[int, int]

class Current:
    buffer: VimBuffer
    window: Window

current: Current

def eval(value: str) -> str:
    pass
