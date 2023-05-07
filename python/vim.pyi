from typing import List, Tuple, TypeVar

TGetKey = TypeVar('TGetKey', slice, int)

class Buffer:
    def __iter__(self) -> str:
        pass

    def __getitem__(self, key: TGetKey) -> str:
        pass

    def __setitem__(self, key: int, value: str) -> None:
        pass

    def __delitem__(self, key: slice) -> None:
        pass

    def __len__(self) -> int:
        pass

    def append(self, str_: List[str], nr: int) -> None:
        pass

class Window:
    cursor: Tuple[int, int]

class Current:
    buffer: Buffer
    window: Window

current: Current

def eval(value: str) -> str:
    pass
