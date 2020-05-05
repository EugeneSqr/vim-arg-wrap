import pytest

from buffer_search import get_args_range, get_line_indent

def test_get_args_range_inside_brackets():
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = get_args_range((1, 27), buffer)
    assert actual == ((0, 26), (0, 35))

@pytest.mark.parametrize('cursor_col', [0, 25])
def test_get_args_range_left(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = get_args_range((1, cursor_col), buffer)
    assert actual == ((0, 26), (0, 35))

@pytest.mark.parametrize('cursor_col', [40, 36])
def test_get_args_range_right(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = get_args_range((1, cursor_col), buffer)
    assert actual == ((0, 26), (0, 35))

@pytest.mark.parametrize('empty_line', [None, ''])
def test_get_indent_empty(empty_line):
    assert get_line_indent(empty_line) == ''

def test_get_indent_0():
    assert get_line_indent('a    aaa') == ''

def test_get_indent_4():
    assert get_line_indent('    aa aa') == '    '
