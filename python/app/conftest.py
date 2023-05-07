from unittest.mock import Mock

import pytest

from app.wrappers import wrapper_base

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
    def _mock_parse_at_cursor(expected):
        monkeypatch.setattr(wrapper_base, 'parse_at_cursor', Mock(return_value=expected))
    return _mock_parse_at_cursor

class VimBuffer(list):
    """ Vim buffer replacement for testing """
    def append(self, lines, index=None):
        if not isinstance(lines, list):
            lines = [lines]

        if not index:
            for line in lines:
                super().append(line)
        else:
            for i, line in enumerate(lines):
                super().insert(index + i + 1, line)
