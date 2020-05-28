from unittest.mock import Mock
from . import wrapper_a, wrapper_base

def test_wrap_args(monkeypatch):
    buffer = _arrange_vim_buffer([
        '    # comment line goes here',
        '    def func():',
        '        method_invocation(first, second, third)',
        '# another comment',
    ])
    _mock_parse_at_cursor(monkeypatch, {
        'start_row_index': 2,
        'end_row_index': 2,
        'indent': 8,
        'beginning': '        method_invocation(',
        'args': ['first', 'second', 'third'],
        'ending': ')',
    })
    arg_wrapper = wrapper_a.ArgWrapperA(4)
    arg_wrapper.wrap_args((3, 1), buffer)
    assert buffer == [
        '    # comment line goes here',
        '    def func():',
        '        method_invocation(',
        '            first, second, third)',
        '# another comment',
    ]

def _arrange_vim_buffer(lines):
    vim_buffer = VimBuffer()
    for line in lines:
        vim_buffer.append(line)
    return vim_buffer

def _mock_parse_at_cursor(monkeypatch, values):
    monkeypatch.setattr(wrapper_base, 'parse_at_cursor', Mock(return_value=type('', (), values)))

class VimBuffer(list):
    """ Vim buffer replacement for testing """
    def append(self, line, index=None):
        if not index:
            super().append(line)
        else:
            super().insert(index, line)
