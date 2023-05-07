import pytest

from app.buffer_parser import ParsedRange
from . import wrapper_c

def test_c_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # c begin comment',
        '   def c_func():',
        '        c_method(c_a, c_b, c_c)',
        ' # c end comment',
    ])
    mock_parse_at_cursor(_build_range(2, 2, 8))
    wrapper_c.ArgWrapperC(500).wrap_args((3, 1), buffer)
    assert buffer == [
        ' # c begin comment',
        '   def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
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
    mock_parse_at_cursor(_build_range(2, 3, 8))
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
    mock_parse_at_cursor(_build_range(2, 5, 8))
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
    mock_parse_at_cursor(_build_range(2, 4, 8))
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
    mock_parse_at_cursor(_build_range(2, 4, 0))
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is True

def test_c_does_not_recognize_empty_range(mock_parse_at_cursor):
    mock_parse_at_cursor(ParsedRange())
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is False

def test_c_does_not_recognize_empty_args(mock_parse_at_cursor):
    mock_parse_at_cursor(_build_range(2, 4, 0, args=[]))
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is False

@pytest.mark.parametrize('c_row_index_diff', [0, 1, 3, 200])
def test_c_does_not_recognize_other_ranges(mock_parse_at_cursor, c_row_index_diff):
    start_row_index = 5
    mock_parse_at_cursor(_build_range(start_row_index, start_row_index + c_row_index_diff, 0))
    assert wrapper_c.ArgWrapperC(2).recognized(None, None) is False

def _build_range(start_row_index,
                 end_row_index,
                 start_row_indent,
                 args=('c_a', 'c_b', 'c_c'),
                 ending=')'):
    return ParsedRange(start_row_index=start_row_index,
                       end_row_index=end_row_index,
                       start_row_indent=start_row_indent,
                       beginning='        c_method(',
                       args=args,
                       ending=ending)
