import pytest

from buffer_parser import parse_at_cursor

def test_parse_at_cursor_single_line_inside_brackets_no_ending():
    '''
    GIVEN function invocation occupies single line
    AND no extra text is present at the end
    AND cursor position is inside the brackets
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['this_is_test_function(a, b, c, d)']
    actual = parse_at_cursor((1, 23), buffer)
    # TODO: introduce shorter checks
    assert actual.start_row_index == 0
    assert actual.end_row_index == 0
    assert actual.indent == 0
    assert actual.beginning == 'this_is_test_function('
    assert actual.args == 'a, b, c, d'
    assert actual.ending == ')'

def test_parse_at_cursor_single_line_inside_brackets():
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position is inside the brackets
    WHEN parsing the buffer range
    THEN all the data is extracted successfully
    '''
    buffer = ['this_is_test_function(a, b, c, d) #test']
    actual = parse_at_cursor((1, 23), buffer)
    assert actual.start_row_index == 0
    assert actual.end_row_index == 0
    assert actual.indent == 0
    assert actual.beginning == 'this_is_test_function('
    assert actual.args == 'a, b, c, d'
    assert actual.ending == ') #test'

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
    actual = parse_at_cursor((1, cursor_col), buffer)
    assert actual.start_row_index == 0
    assert actual.end_row_index == 0
    assert actual.indent == 0
    assert actual.beginning == 'this_is_test_function('
    assert actual.args == 'a, b, c, d'
    assert actual.ending == ') #test'

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
    actual = parse_at_cursor((1, cursor_col), buffer)
    assert actual.start_row_index == 0
    assert actual.end_row_index == 0
    assert actual.indent == 0
    assert actual.beginning == 'this_is_test_function('
    assert actual.args == 'a, b, c, d'
    assert actual.ending == ') #test'

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
    actual = parse_at_cursor((1, 0), buffer)
    assert actual.start_row_index == 0
    assert actual.end_row_index == 0
    assert actual.indent == 3
    assert actual.beginning == '   this_is_test_function('
    assert actual.args == 'a, b, c, d'
    assert actual.ending == ') #test'
