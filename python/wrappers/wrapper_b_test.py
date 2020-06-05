import pytest

from . import wrapper_b

def test_b_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(7).wrap_args((3, 1), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '               b_a,',
        '               b_b,',
        '               b_c)',
        ' # b end comment',
    ]

def test_b_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(0).wrap_args((4, 0), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '        b_a,',
        '        b_b,',
        '        b_c)',
        ' # b end comment',
    ]

def test_b_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(4).wrap_args((6, 0), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ]

def test_b_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a,',
        '                 b_b,',
        '                 b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(2).wrap_args((5, 0), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '          b_a,',
        '          b_b,',
        '          b_c)',
        ' # b end comment',
    ]

def test_b_recognizes_b(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 0,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    assert wrapper_b.ArgWrapperB(4).recognized(None, None) is True

def test_b_does_not_recognize_empty_range(mock_parse_at_cursor):
    mock_parse_at_cursor(None)
    assert wrapper_b.ArgWrapperB(4).recognized(None, None) is False

def test_b_does_not_recognize_empty_args(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 0,
        'beginning': '        b_method(',
        'args': [],
        'ending': ')',
    })
    assert wrapper_b.ArgWrapperB(4).recognized(None, None) is False

@pytest.mark.parametrize('b_row_index_diff', [0, 1, 2, 200])
def test_b_does_not_recognize_other_ranges(mock_parse_at_cursor, b_row_index_diff):
    start_row_index = 2
    mock_parse_at_cursor({
        'start_row_index': start_row_index, 'end_row_index': start_row_index + b_row_index_diff,
        'start_row_indent': 0,
        'beginning': '        a_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    assert wrapper_b.ArgWrapperB(2).recognized(None, None) is False
