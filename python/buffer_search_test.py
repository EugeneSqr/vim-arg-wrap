import pytest

from buffer_search import find_args_range

def test_find_args_range_inside_brackets():
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = find_args_range(1, 28, buffer)
    assert actual == ((1, 26), (1, 37))

@pytest.mark.parametrize('cursor_col', [1, 26])
def test_find_args_range_left(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = find_args_range(1, cursor_col, buffer)
    assert actual == ((1, 26), (1, 37))

@pytest.mark.parametrize('cursor_col', [40, 37])
def test_find_args_range_right(cursor_col):
    buffer = ['def this_is_test_function(a, b, c, d) #test']
    actual = find_args_range(1, cursor_col, buffer)
    assert actual == ((1, 26), (1, 37))
