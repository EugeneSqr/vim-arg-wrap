from typing import Tuple
from unittest.mock import Mock

from app.buffer_parser import Signature, RowsRange
from app.conftest import VimBufferMock, assert_buffer
from . import wrapper_d

def test_d_wrap_args_single_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # d begin comment',
        '   def d_func():',
        '        d_method(d_a, d_b, d_c)',
        ' # d end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 2, 8)))
    wrapper_d.ArgWrapperD(4).wrap_args((3, 1), buffer)
    assert_buffer(buffer, [
        ' # d begin comment',
        '   def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c,',
        '        )',
        ' # d end comment',
    ])

def test_d_wrap_args_two_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a, d_b, d_c)',
        ' # d end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 3, 8)))
    wrapper_d.ArgWrapperD(4).wrap_args((4, 0), buffer)
    assert_buffer(buffer, [
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c,',
        '        )',
        ' # d end comment',
    ])

def test_d_wrap_args_multiple_lines(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c)',
        ' # d end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 5, 8)))
    wrapper_d.ArgWrapperD(4).wrap_args((6, 0), buffer)
    assert_buffer(buffer, [
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c,',
        '        )',
        ' # d end comment',
    ])

def test_d_wrap_args_multiple_lines_below_first(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # d begin comment',
        '    def d_func():',
        '        d_method(d_a,',
        '                 d_b,',
        '                 d_c)',
        ' # d end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 4, 8)))
    wrapper_d.ArgWrapperD(4).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c,',
        '        )',
        ' # d end comment',
    ])

def test_d_wrap_args_multiple_lines_below_first_extra_line(mock_signature_at_cursor: Mock) -> None:
    buffer = VimBufferMock([
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c,',
        '        )',
        ' # d end comment',
    ])
    mock_signature_at_cursor(_build_signature(RowsRange(2, 6, 8)))
    wrapper_d.ArgWrapperD(4).wrap_args((5, 0), buffer)
    assert_buffer(buffer, [
        ' # d begin comment',
        '    def d_func():',
        '        d_method(',
        '            d_a,',
        '            d_b,',
        '            d_c,',
        '        )',
        ' # d end comment',
    ])

def test_d_recognizes_d(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 6, 0)))
    assert wrapper_d.ArgWrapperD(4).recognized((0, 0), VimBufferMock([])) is True

def test_d_does_not_recognize_empty_range(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(Signature())
    assert wrapper_d.ArgWrapperD(4).recognized((0, 0), VimBufferMock([])) is False

def test_d_does_not_recognize_empty_args(mock_signature_at_cursor: Mock) -> None:
    mock_signature_at_cursor(_build_signature(RowsRange(2, 6, 0), args=()))
    assert wrapper_d.ArgWrapperD(4).recognized((0, 0), VimBufferMock([])) is False

def _build_signature(rows_range: RowsRange,
                     args: Tuple[str, ...]=('d_a', 'd_b', 'd_c'),
                     ending: str=')') -> Signature:
    return Signature(rows=rows_range, beginning='        d_method(', args=args, ending=ending)
