from typing import Tuple, Protocol, List, Union, Iterator, Optional, overload

VimCursor = Tuple[int, int]

class VimBuffer(Protocol):
    def __iter__(self) -> Iterator[str]:
        pass

    @overload
    def __getitem__(self, key: int) -> str:
        pass

    @overload
    def __getitem__(self, key: slice) -> List[str]:
        pass

    def __setitem__(self, key: int, value: str) -> None:
        pass

    def __delitem__(self, key: Union[int, slice]) -> None:
        pass

    def __len__(self) -> int:
        pass

    def append(self, str_: List[str], nr: Optional[int] = None) -> None:
        pass
