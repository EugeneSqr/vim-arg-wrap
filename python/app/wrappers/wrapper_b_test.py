import pytest

from app.buffer_parser import Signature, RowsRange
from . import wrapper_b

def test_b_wrap_args_single_line(arrange_vim_buffer, mock_signature_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2), 8))
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

def test_b_wrap_args_two_lines(arrange_vim_buffer, mock_signature_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3), 8))
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

def test_b_wrap_args_multiple_lines(arrange_vim_buffer, mock_signature_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5), 8))
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

def test_b_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_signature_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a,',
        '                 b_b,',
        '                 b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4), 8))
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

def test_b_recognizes_b(mock_signature_at_cursor):
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5), 0))
    assert wrapper_b.ArgWrapperB(4).recognized(None, None) is True

def test_b_does_not_recognize_empty_range(mock_signature_at_cursor):
    mock_signature_at_cursor(Signature())
    assert wrapper_b.ArgWrapperB(4).recognized(None, None) is False

def test_b_does_not_recognize_empty_args(mock_signature_at_cursor):
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5), 0, args=[]))
    assert wrapper_b.ArgWrapperB(4).recognized(None, None) is False

@pytest.mark.parametrize('b_row_index_diff', [0, 1, 2, 200])
def test_b_does_not_recognize_other_ranges(mock_signature_at_cursor, b_row_index_diff):
    start_row = 2
    rows_range = RowsRange(start_row, start_row + b_row_index_diff)
    mock_signature_at_cursor(_build_signature(rows_range, 0))
    assert wrapper_b.ArgWrapperB(2).recognized(None, None) is False

def _build_signature(rows_range,
                     start_row_indent,
                     args=('b_a', 'b_b', 'b_c'),
                     ending=')'):
    return Signature(rows=rows_range,
                     start_row_indent=start_row_indent,
                     beginning='        b_method(',
                     args=args,
                     ending=ending)
