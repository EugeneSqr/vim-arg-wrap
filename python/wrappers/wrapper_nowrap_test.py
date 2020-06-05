import pytest

from . import wrapper_nowrap

def test_nowrap_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '   def nowrap_func():',
        '      nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 6,
        'beginning': '      nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(3).wrap_args((2, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '   def nowrap_func():',
        '      nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((4, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a,',
        '            nowrap_b,',
        '            nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((6, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a,',
        '                      nowrap_b,',
        '                      nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((5, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_recognizes_nowrap(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    assert wrapper_nowrap.ArgWrapperNoWrap(4).recognized(None, None) is True

def test_nowrap_does_not_recognize_empty_range(mock_parse_at_cursor):
    mock_parse_at_cursor(None)
    assert wrapper_nowrap.ArgWrapperNoWrap(4).recognized(None, None) is False

def test_nowrap_does_not_recognize_empty_args(mock_parse_at_cursor):
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': [],
        'ending': ')',
    })
    assert wrapper_nowrap.ArgWrapperNoWrap(4).recognized(None, None) is False

@pytest.mark.parametrize('nowrap_row_index_diff', [1, 2, 3, 400])
def test_nowrap_does_not_recognize_other_ranges(mock_parse_at_cursor, nowrap_row_index_diff):
    start_row_index = 2
    mock_parse_at_cursor({
        'start_row_index': start_row_index,
        'end_row_index': start_row_index + nowrap_row_index_diff,
        'start_row_indent': 0,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    assert wrapper_nowrap.ArgWrapperNoWrap(2).recognized(None, None) is False
