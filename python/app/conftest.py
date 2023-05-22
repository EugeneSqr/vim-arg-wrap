from typing import List, Iterator, Union, Callable, Optional
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from app.types import VimBuffer, TKey
from app.wrappers import wrapper_base
from app.buffer_parser import Signature

@pytest.fixture(name='mock_signature_at_cursor')
def fixture_mock_signature_at_cursor(monkeypatch: MonkeyPatch) -> Callable[[Signature], None]:
    def _mock_signature_at_cursor(expected: Signature) -> None:
        monkeypatch.setattr(wrapper_base, 'signature_at_cursor', Mock(return_value=expected))
    return _mock_signature_at_cursor

class VimBufferMock():
    """ Vim buffer replacement for testing. """
    def __init__(self, rows: List[str]):
        self._rows = rows

    def __iter__(self) -> Iterator[str]:
        return iter(self._rows)

    def __getitem__(self, key: TKey) -> Union[str, List[str]]:
        return self._rows[key]

    def __setitem__(self, key: int, value: str) -> None:
        self._rows[key] = value

    def __delitem__(self, key: TKey) -> None:
        del self._rows[key]

    def __len__(self) -> int:
        return len(self._rows)

    def append(self, str_: List[str], nr: Optional[int] = None) -> None:
        nr = nr if nr is not None else len(self._rows)
        self._rows = self._rows[:nr] + str_ + self._rows[nr:]

def assert_buffer(actual: VimBuffer, expected: List[str]):
    for index in range(0, len(actual)):
        assert actual[index] == expected[index]
