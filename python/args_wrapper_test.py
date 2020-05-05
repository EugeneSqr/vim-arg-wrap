from unittest.mock import Mock
import args_wrapper

def test_test(monkeypatch):
    _mock_get_args_range(monkeypatch, ((2, 26), (2, 45)))
    _mock_get_buffer_indent(monkeypatch, ' '*4)
    _mock_get_line_indent(monkeypatch, ' '*8)
    buffer = _arrange_vim_buffer([
        '    # comment line goes here',
        '    def func():',
        '        method_invocation(first, second, third)',
        '# another comment',
    ])
    args_wrapper.wrap_args((3, 1), buffer)
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

def _mock_get_args_range(monkeypatch, value):
    _mock_args_wrapper(monkeypatch, 'get_args_range', value)

def _mock_get_buffer_indent(monkeypatch, value):
    _mock_args_wrapper(monkeypatch, 'get_buffer_indent', value)

def _mock_get_line_indent(monkeypatch, value):
    _mock_args_wrapper(monkeypatch, 'get_line_indent', value)

def _mock_args_wrapper(monkeypatch, name, value):
    monkeypatch.setattr(args_wrapper, name, Mock(return_value=value))

class VimBuffer(list):
    """ Vim buffer replacement for testing """
    def append(self, line, index=None):
        if not index:
            super().append(line)
        else:
            super().insert(index, line)
