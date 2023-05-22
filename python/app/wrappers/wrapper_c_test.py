import pytest

from app.buffer_parser import Signature, RowsRange
from app.conftest import VimBufferMock, assert_buffer
from . import wrapper_c

def test_c_wrap_args_single_line(mock_signature_at_cursor):
    buffer = VimBufferMock([
        ' # c begin comment',
        '   def c_func():',
        '        c_method(c_a, c_b, c_c)',
        ' # c end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 8)))
    wrapper_c.ArgWrapperC(500).wrap_args((3, 1), buffer)
    assert_buffer(buffer, [
        ' # c begin comment',
        '   def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ])

def test_c_wrap_args_two_lines(mock_signature_at_cursor):
    buffer = VimBufferMock([
        ' # c begin comment',
        '    def c_func():',
        '        c_method(',
        '            c_a, c_b, c_c)',
        ' # c end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3, 8)))
    wrapper_c.ArgWrapperC(None).wrap_args((4, 0), buffer)
    assert_buffer(buffer, [
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ])

def test_c_wrap_args_multiple_lines(mock_signature_at_cursor):
    buffer = VimBufferMock([
        ' # c begin comment',
        '    def c_func():',
        '        c_method(',
        '            c_a,',
        '            c_b,',
        '            c_c)',
        ' # c end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 8)))
    wrapper_c.ArgWrapperC(None).wrap_args((6, 0), buffer)
    assert_buffer(buffer, [
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ])

def test_c_wrap_args_multiple_lines_below_first(mock_signature_at_cursor):
    buffer = VimBufferMock([
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 8)))
    wrapper_c.ArgWrapperC(None).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # c begin comment',
        '    def c_func():',
        '        c_method(c_a,',
        '                 c_b,',
        '                 c_c)',
        ' # c end comment',
    ])

def test_c_recognizes_c(mock_signature_at_cursor):
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 0)))
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is True

def test_c_does_not_recognize_empty_range(mock_signature_at_cursor):
    mock_signature_at_cursor(Signature())
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is False

def test_c_does_not_recognize_empty_args(mock_signature_at_cursor):
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 0), args=[]))
    assert wrapper_c.ArgWrapperC(4).recognized(None, None) is False

@pytest.mark.parametrize('c_row_index_diff', [0, 1, 3, 200])
def test_c_does_not_recognize_other_ranges(mock_signature_at_cursor, c_row_index_diff):
    start_row = 5
    rows_range = RowsRange(start_row, start_row + c_row_index_diff, 0)
    mock_signature_at_cursor(_build_signature(rows_range))
    assert wrapper_c.ArgWrapperC(2).recognized(None, None) is False

def _build_signature(rows_range, args=('c_a', 'c_b', 'c_c'), ending=')'):
    return Signature(rows=rows_range, beginning='        c_method(', args=args, ending=ending)
