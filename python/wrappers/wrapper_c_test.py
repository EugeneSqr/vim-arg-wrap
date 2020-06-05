import pytest

from . import wrapper_c

def test_c_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # c begin comment',
        '   def c_func():',
        '         c_method(c_a, c_b, c_c)',
        ' # c end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 9,
        'beginning': '         c_method(',
        'args': ['c_a', 'c_b', 'c_c'],
        'ending': ')',
    })
    wrapper_c.ArgWrapperC(500).wrap_args((3, 1), buffer)
    assert buffer == [
        ' # c begin comment',
        '   def c_func():',
        '         c_method(c_a,',
        '                  c_b,',
        '                  c_c)',
        ' # c end comment',
    ]

def test_c_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # c begin comment',
        '    def c_func():',
        '        c_method(',
        '            c_a, c_b, c_c)',
        ' # c end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        c_method(',
        'args': ['c_a', 'c_b', 'c_c'],
        'ending': ')',
    })
    wrapper_c.ArgWrapperC(None).wrap_args((4, 0), buffer)
    assert buffer == [
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ]

def test_c_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # c begin comment',
        '    def c_func():',
        '        c_method(',
        '            c_a,',
        '            c_b,',
        '            c_c)',
        ' # c end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        c_method(',
        'args': ['c_a', 'c_b', 'c_c'],
        'ending': ')',
    })
    wrapper_c.ArgWrapperC(None).wrap_args((6, 0), buffer)
    assert buffer == [
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ]

def test_c_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        c_method(',
        'args': ['c_a', 'c_b', 'c_c'],
        'ending': ')',
    })
    wrapper_c.ArgWrapperC(None).wrap_args((5, 0), buffer)
    assert buffer == [
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ]

def test_c_recognizes_c(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 0,
        'beginning': '        c_method(',
        'args': ['c_a', 'c_b', 'c_c'],
        'ending': ')',
    })
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is True

def test_c_does_not_recognize_empty_range(mock_parse_at_cursor):
    mock_parse_at_cursor(None)
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is False

def test_c_does_not_recognize_empty_args(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 0,
        'beginning': '        c_method(',
        'args': [],
        'ending': ')',
    })
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is False

@pytest.mark.parametrize('c_row_index_diff', [0, 1, 3, 200])
def test_c_does_not_recognize_other_ranges(mock_parse_at_cursor, c_row_index_diff):
    start_row_index = 5
    mock_parse_at_cursor({
        'start_row_index': start_row_index, 'end_row_index': start_row_index + c_row_index_diff,
        'start_row_indent': 0,
        'beginning': '        c_method(',
        'args': ['c_a', 'c_b', 'c_c'],
        'ending': ')',
    })
    assert wrapper_c.ArgWrapperC(2).recognized(None, None) is False
