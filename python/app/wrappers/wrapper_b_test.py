from typing import Tuple
from unittest.mock import Mock

import pytest

from app.buffer_parser import Signature, RowsRange
from app.conftest import VimBufferMock, assert_buffer
from . import wrapper_b

def test_b_wrap_args_single_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 8)))
    wrapper_b.ArgWrapperB(7).wrap_args((3, 1), buffer)
    assert_buffer(buffer, [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '               b_a,',
        '               b_b,',
        '               b_c)',
        ' # b end comment',
    ])

def test_b_wrap_args_two_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3, 8)))
    wrapper_b.ArgWrapperB(0).wrap_args((4, 0), buffer)
    assert_buffer(buffer, [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '        b_a,',
        '        b_b,',
        '        b_c)',
        ' # b end comment',
    ])

def test_b_wrap_args_multiple_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 8)))
    wrapper_b.ArgWrapperB(4).wrap_args((6, 0), buffer)
    assert_buffer(buffer, [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ])

def test_b_wrap_args_multiple_lines_below_first(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a,',
        '                 b_b,',
        '                 b_c)',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 8)))
    wrapper_b.ArgWrapperB(2).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '          b_a,',
        '          b_b,',
        '          b_c)',
        ' # b end comment',
    ])

def test_b_wrap_args_multiple_lines_below_first_extra_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c,',
        '        )',
        ' # b end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 6, 8)))
    wrapper_b.ArgWrapperB(2).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '          b_a,',
        '          b_b,',
        '          b_c)',
        ' # b end comment',
    ])

def test_b_recognizes_b(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 0)))
    assert wrapper_b.ArgWrapperB(4).recognized((0, 0), VimBufferMock([])) is True

def test_b_does_not_recognize_empty_range(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(Signature())
    assert wrapper_b.ArgWrapperB(4).recognized((0, 0), VimBufferMock([])) is False

def test_b_does_not_recognize_empty_args(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 0), args=()))
    assert wrapper_b.ArgWrapperB(4).recognized((0, 0), VimBufferMock([])) is False

@pytest.mark.parametrize('b_row_index_diff', [0, 1, 2, 200])
def test_b_does_not_recognize_other_ranges(mock_signature_at_cursor: Mock,
                                           b_row_index_diff: int) -> None:
    start_row = 2
    rows_range = RowsRange(start_row, start_row + b_row_index_diff, 0)
    mock_signature_at_cursor(_build_signature(rows_range))
    assert wrapper_b.ArgWrapperB(2).recognized((0, 0), VimBufferMock([])) is False

def _build_signature(rows_range: RowsRange,
                     args: Tuple[str, ...]=('b_a', 'b_b', 'b_c'),
                     ending: str=')') -> Signature:
    return Signature(rows=rows_range, beginning='        b_method(', args=args, ending=ending)
