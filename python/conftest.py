from unittest.mock import Mock

import pytest

from wrappers import wrapper_base

@pytest.fixture(name='arrange_vim_buffer')
def fixture_arrange_vim_buffer():
    def _arrange_vim_buffer(lines):
        vim_buffer = VimBuffer()
        for line in lines:
            vim_buffer.append(line)
        return vim_buffer
    return _arrange_vim_buffer

@pytest.fixture(name='mock_parse_at_cursor')
def fixture_mock_parse_at_cursor(monkeypatch):
    def _mock_parse_at_cursor(values):
        monkeypatch.setattr(
            wrapper_base, 'parse_at_cursor', Mock(return_value=type('', (), values)))
    return _mock_parse_at_cursor

class VimBuffer(list):
    """ Vim buffer replacement for testing """
    def append(self, line, index=None):
        if not index:
            super().append(line)
        else:
            super().insert(index, line)
