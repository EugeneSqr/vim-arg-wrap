import pytest

from buffer_parser import parse_at_cursor

_FIELD_NAMES = [
    'start_row_index',
    'end_row_index',
    'indent',
    'beginning',
    'args',
    'ending',
]

def test_parse_at_cursor_single_line_inside_brackets_no_ending():
    '''
    GIVEN function invocation occupies single line
    AND no extra text is present at the end
    AND cursor position is inside the brackets
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['this_is_test_function(a, b, c, d)']
    assert _properties_equal(
        parse_at_cursor((1, 23), buffer),
        [0, 0, 0, 'this_is_test_function(', 'a, b, c, d', ')'])

def test_parse_at_cursor_single_line_inside_brackets():
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position is inside the brackets
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['this_is_test_function(a, b, c, d) #test']
    assert _properties_equal(
        parse_at_cursor((1, 23), buffer),
        [0, 0, 0, 'this_is_test_function(', 'a, b, c, d', ') #test'])

@pytest.mark.parametrize('cursor_col', [0, 21])
def test_parse_at_cursor_single_line_left(cursor_col):
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position is to the left of the opening bracket
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['this_is_test_function(a, b, c, d) #test']
    assert _properties_equal(
        parse_at_cursor((1, cursor_col), buffer),
        [0, 0, 0, 'this_is_test_function(', 'a, b, c, d', ') #test'])

@pytest.mark.parametrize('cursor_col', [36, 32])
def test_parse_at_cursor_single_line_right(cursor_col):
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position is to the right of the opening bracket
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['this_is_test_function(a, b, c, d) #test']
    assert _properties_equal(
        parse_at_cursor((1, cursor_col), buffer),
        [0, 0, 0, 'this_is_test_function(', 'a, b, c, d', ') #test'])

def test_parse_at_cursor_single_line_with_indent():
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position at the beginning of the line
    AND line has non zero indentation
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['   this_is_test_function(a, b, c, d) #test']
    assert _properties_equal(
        parse_at_cursor((1, 0), buffer),
        [0, 0, 3, '   this_is_test_function(', 'a, b, c, d', ') #test'])

def _properties_equal(actual, expected):
    return all(actual.__dict__[_FIELD_NAMES[i]] == expected[i] for i in range(len(_FIELD_NAMES)))
