import pytest

from buffer_search import get_args_range, get_line_indentation

def test_get_args_range_inside_brackets():
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = get_args_range((1, 27), buffer)
    assert actual == ((0, 25), (0, 36))

@pytest.mark.parametrize('cursor_col', [0, 25])
def test_get_args_range_left(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = get_args_range((1, cursor_col), buffer)
    assert actual == ((0, 25), (0, 36))

@pytest.mark.parametrize('cursor_col', [40, 36])
def test_get_args_range_right(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = get_args_range((1, cursor_col), buffer)
    assert actual == ((0, 25), (0, 36))

@pytest.mark.parametrize('empty_line', [None, ''])
def test_get_indentation_empty(empty_line):
    assert get_line_indentation(empty_line) == 0

def test_get_indentation_0():
    assert get_line_indentation('a    aaa') == 0

def test_get_indentation_4():
    assert get_line_indentation('    aa aa') == 4
