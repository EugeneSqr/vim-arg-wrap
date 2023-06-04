from typing import Tuple
from unittest.mock import Mock

import pytest

from app.buffer_parser import Signature, RowsRange
from app.conftest import VimBufferMock, assert_buffer
from . import wrapper_a

def test_a_wrap_args_single_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(a_a, a_b, a_c)',
        ' # a end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 8)))
    wrapper_a.ArgWrapperA(8).wrap_args((3, 1), buffer)
    assert_buffer(buffer, [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '                a_a, a_b, a_c)',
        ' # a end comment',
    ])

def test_a_wrap_args_two_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
        ' # a end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3, 8)))
    wrapper_a.ArgWrapperA(0).wrap_args((4, 0), buffer)
    assert_buffer(buffer, [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '        a_a, a_b, a_c)',
        ' # a end comment',
    ])

def test_a_wrap_args_multiple_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a,',
        '            a_b,',
        '            a_c)',
        ' # a end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 8)))
    wrapper_a.ArgWrapperA(2).wrap_args((6, 0), buffer)
    assert_buffer(buffer, [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '          a_a, a_b, a_c)',
        ' # a end comment',
    ])

def test_a_wrap_args_multiple_lines_below_first(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(a_a,',
        '                 a_b,',
        '                 a_c)',
        ' # a end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 8)))
    wrapper_a.ArgWrapperA(4).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
        ' # a end comment',
    ])

def test_a_wrap_args_multiple_lines_below_first_extra_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a,',
        '            a_b,',
        '            a_c,',
        '        )',
        ' # a end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 6, 8)))
    wrapper_a.ArgWrapperA(4).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # a begin comment',
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
        ' # a end comment',
    ])

def test_a_recognizes_a(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(0, 1, 0), 'a_method('))
    buffer = VimBufferMock([
        'a_method(',
        '    a_a, a_b, a_c)',
    ])
    assert wrapper_a.ArgWrapperA(4).recognized((0, 0), buffer) is True

def test_a_recognizes_a_with_first_row_ending(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(0, 1, 0)))
    buffer = VimBufferMock([
        'a_method(# something other than a_a',
        '    a_a, a_b, a_c)',
    ])
    assert wrapper_a.ArgWrapperA(4).recognized((0, 0), buffer) is True

def test_a_does_not_recognize_empty_range(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(Signature())
    assert wrapper_a.ArgWrapperA(4).recognized((0, 0), VimBufferMock([])) is False

def test_a_does_not_recognize_empty_args(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3, 0), args=()))
    assert wrapper_a.ArgWrapperA(4).recognized((0, 0), VimBufferMock([])) is False

@pytest.mark.parametrize('a_row_index_diff', [0, 2, 3, 200])
def test_a_does_not_recognize_other_ranges(mock_signature_at_cursor: Mock,
                                           a_row_index_diff: int) -> None:
    start_row = 3
    rows_range = RowsRange(start_row, start_row + a_row_index_diff, 0)
    mock_signature_at_cursor(_build_signature(rows_range))
    assert wrapper_a.ArgWrapperA(2).recognized((0, 0), VimBufferMock([])) is False

def test_a_does_not_recognize_c_which_looks_similar(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(0, 1, 0), 'a_method('))
    buffer = VimBufferMock([
        'a_method(a_a',
        '         a_b)',
    ])
    assert wrapper_a.ArgWrapperA(9).recognized((0, 0), buffer) is False

def _build_signature(rows_range: RowsRange,
                     beginning: str='        a_method(',
                     args: Tuple[str, ...]=('a_a', 'a_b', 'a_c'),
                     ending: str=')') -> Signature:
    return Signature(rows=rows_range, beginning=beginning, args=args, ending=ending)
