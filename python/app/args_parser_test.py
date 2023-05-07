import pytest

from . import args_parser

def test_parse_args_line_empty_args_returns_array_with_original_args_line() -> None:
    assert args_parser.parse_args_line(',,,') == (',,,',)

@pytest.mark.parametrize('invalid_line', [')', ']', '}', 'a(}', '[)', '(()]'])
def test_parse_args_line_invalid_args_returns_arrayed_args_line(invalid_line: str) -> None:
    assert args_parser.parse_args_line(invalid_line) == (invalid_line,)

def test_parse_args_line_returns_args_with_spaces_discarded() -> None:
    assert args_parser.parse_args_line('  a  , b,c  , d') == ('a', 'b', 'c', 'd')

def test_parse_args_line_nested_calls_single_bracket_type_returns_args() -> None:
    assert (args_parser.parse_args_line('l11(l21(l31(a, b), c), l22(d, e)), f') ==
            ('l11(l21(l31(a, b), c), l22(d, e))', 'f'))

def test_parse_args_line_nested_calls_multiple_bracket_types_returns_args() -> None:
    assert (args_parser.parse_args_line('l1([1,2,3,], {"a": [3,6,7],}), l2[5], {}, []') ==
            ('l1([1,2,3,], {"a": [3,6,7],})', 'l2[5]', '{}', '[]'))
