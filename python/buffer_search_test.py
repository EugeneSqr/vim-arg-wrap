import pytest

from buffer_search import find_args_range

def test_find_args_range_inside_brackets():
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = find_args_range(1, 27, buffer)
    assert actual == ((1, 25), (1, 36))

@pytest.mark.parametrize('cursor_col', [0, 25])
def test_find_args_range_left(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = find_args_range(1, cursor_col, buffer)
    assert actual == ((1, 25), (1, 36))

@pytest.mark.parametrize('cursor_col', [40, 36])
def test_find_args_range_right(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = find_args_range(1, cursor_col, buffer)
    assert actual == ((1, 25), (1, 36))
