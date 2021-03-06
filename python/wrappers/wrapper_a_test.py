import pytest

from . import wrapper_a

def test_a_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(a_a, a_b, a_c)',
        ' # a end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(8).wrap_args((3, 1), buffer)
    assert buffer == [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '                a_a, a_b, a_c)',
        ' # a end comment',
    ]

def test_a_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
        ' # a end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(0).wrap_args((4, 0), buffer)
    assert buffer == [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '        a_a, a_b, a_c)',
        ' # a end comment',
    ]

def test_a_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a,',
        '            a_b,',
        '            a_c)',
        ' # a end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(2).wrap_args((6, 0), buffer)
    assert buffer == [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '          a_a, a_b, a_c)',
        ' # a end comment',
    ]

def test_a_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(a_a,',
        '                 a_b,',
        '                 a_c)',
        ' # a end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(4).wrap_args((5, 0), buffer)
    assert buffer == [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
        ' # a end comment',
    ]

def test_a_recognizes_a(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 0, 'end_row_index': 1, 'start_row_indent': 0,
        'beginning': 'a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    buffer = [
        'a_method(',
        '    a_a, a_b, a_c)',
    ]
    assert wrapper_a.ArgWrapperA(4).recognized(None, buffer) is True

def test_a_recognizes_a_with_first_row_ending(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 0, 'end_row_index': 1, 'start_row_indent': 0,
        'beginning': 'a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    buffer = [
        'a_method(# something other than a_a',
        '    a_a, a_b, a_c)',
    ]
    assert wrapper_a.ArgWrapperA(4).recognized(None, buffer) is True

def test_a_does_not_recognize_empty_range(mock_parse_at_cursor):
    mock_parse_at_cursor(None)
    assert wrapper_a.ArgWrapperA(4).recognized(None, None) is False

def test_a_does_not_recognize_empty_args(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 0,
        'beginning': '        a_method(',
        'args': [],
        'ending': ')',
    })
    assert wrapper_a.ArgWrapperA(4).recognized(None, None) is False

@pytest.mark.parametrize('a_row_index_diff', [0, 2, 3, 200])
def test_a_does_not_recognize_other_ranges(mock_parse_at_cursor, a_row_index_diff):
    start_row_index = 3
    mock_parse_at_cursor({
        'start_row_index': start_row_index, 'end_row_index': start_row_index + a_row_index_diff,
        'start_row_indent': 0,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    assert wrapper_a.ArgWrapperA(2).recognized(None, None) is False

def test_a_does_not_recognize_c_which_looks_similar(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 0, 'end_row_index': 1, 'start_row_indent': 0,
        'beginning': 'a_method(',
        'args': ['a_a', 'b_b'],
        'ending': ')',
    })
    buffer = [
        'a_method(a_a',
        '         a_b)',
    ]
    assert wrapper_a.ArgWrapperA(9).recognized(None, buffer) is False
