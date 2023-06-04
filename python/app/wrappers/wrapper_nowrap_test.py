from typing import Tuple
from unittest.mock import Mock

import pytest

from app.buffer_parser import Signature, RowsRange
from app.conftest import VimBufferMock, assert_buffer
from . import wrapper_nowrap

def test_nowrap_wrap_args_single_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 6)))
    wrapper_nowrap.ArgWrapperNoWrap(3).wrap_args((2, 0), buffer)
    assert_buffer(buffer, [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])

def test_nowrap_wrap_args_two_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3, 8)))
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((4, 0), buffer)
    assert_buffer(buffer, [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])

def test_nowrap_wrap_args_multiple_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a,',
        '            nowrap_b,',
        '            nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 8)))
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((6, 0), buffer)
    assert_buffer(buffer, [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])

def test_nowrap_wrap_args_multiple_lines_below_first(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a,',
        '                      nowrap_b,',
        '                      nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 8)))
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])

def test_nowrap_wrap_args_multiple_lines_below_first_extra_line(
        mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a,',
        '            nowrap_b,',
        '            nowrap_c,',
        '        )',
        ' # nowrap end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 6, 8)))
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])

def test_nowrap_recognizes_nowrap(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 8)))
    assert wrapper_nowrap.ArgWrapperNoWrap(4).recognized((0, 0), VimBufferMock([])) is True

def test_nowrap_does_not_recognize_empty_range(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(Signature())
    assert wrapper_nowrap.ArgWrapperNoWrap(4).recognized((0, 0), VimBufferMock([])) is False

def test_nowrap_does_not_recognize_empty_args(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 8), args=()))
    assert wrapper_nowrap.ArgWrapperNoWrap(4).recognized((0, 0), VimBufferMock([])) is False

@pytest.mark.parametrize('nowrap_row_index_diff', [1, 2, 3, 400])
def test_nowrap_does_not_recognize_other_ranges(mock_signature_at_cursor: Mock,
                                                nowrap_row_index_diff: int) -> None:
    start_row = 2
    rows_range = RowsRange(start_row, start_row + nowrap_row_index_diff, 0)
    mock_signature_at_cursor(_build_signature(rows_range))
    assert wrapper_nowrap.ArgWrapperNoWrap(2).recognized((0, 0), VimBufferMock([])) is False

def _build_signature(rows_range: RowsRange,
                     args: Tuple[str, ...]=('nowrap_a', 'nowrap_b', 'nowrap_c'),
                     ending: str=')') -> Signature:
    return Signature(rows=rows_range, beginning='        nowrap_method(', args=args, ending=ending)
