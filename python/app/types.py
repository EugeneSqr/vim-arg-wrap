from typing import Tuple, Protocol, TypeVar, List, Union, Iterator, Optional

Cursor = Tuple[int, int]

TKey = TypeVar('TKey', slice, int)

class VimBuffer(Protocol):
    def __iter__(self) -> Iterator[str]:
        pass

    def __getitem__(self, key: TKey) -> Union[str, List[str]]:
        pass

    def __setitem__(self, key: int, value: str) -> None:
        pass

    def __delitem__(self, key: TKey) -> None:
        pass

    def __len__(self) -> int:
        pass

    def append(self, str_: List[str], nr: Optional[int] = None) -> None:
        pass
