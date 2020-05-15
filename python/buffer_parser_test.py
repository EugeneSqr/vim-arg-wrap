import pytest

from buffer_parser import (
    parse_at_cursor,
    _get_last_closing_bracket_index,
    _get_first_opening_bracket_index,
)

_FIELD_NAMES = [
    'start_row_index',
    'end_row_index',
    'indent',
    'beginning',
    'args',
    'ending',
]

@pytest.mark.parametrize(
    ['offset', 'text_beginning'],
    [('', ''), ('    ', 'test'), ('  ', '')])
def test_parse_at_cursor_single_line_inside_brackets_beginning(offset, text_beginning):
    '''
    GIVEN function invocation occupies single line
    AND beginning text is of varied length
    AND offset is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = [offset + text_beginning + '(a, b, c, d)']
    assert _properties_equal(
        parse_at_cursor((1, len(offset) + len(text_beginning) + 1), buffer),
        [0, 0, len(offset), offset + text_beginning + '(', ['a', 'b', 'c', 'd'], ')'])

@pytest.mark.parametrize('text_ending', ['', ' #test'])
def test_parse_at_cursor_single_line_inside_brackets_ending(text_ending):
    '''
    GIVEN function invocation occupies single line
    AND ending text is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = ['this_is_test_function(a, b, c, d)' + text_ending]
    assert _properties_equal(
        parse_at_cursor((1, 23), buffer),
        [0, 0, 0, 'this_is_test_function(', ['a', 'b', 'c', 'd'], ')' + text_ending])

@pytest.mark.parametrize('cursor_col', [0, 21, 23, 32, 36])
def test_parse_at_cursor_single_line_cursor_positions(cursor_col):
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position varies from left to right
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    AND result does not depend on cursor position
    '''
    buffer = ['this_is_test_function(a, b, c, d) #test']
    assert _properties_equal(
        parse_at_cursor((1, cursor_col), buffer),
        [0, 0, 0, 'this_is_test_function(', ['a', 'b', 'c', 'd'], ') #test'])

@pytest.mark.parametrize(
    ['offset', 'text_beginning'],
    [('', ''), ('    ', 'test'), ('  ', '')])
def test_parse_at_cursor_two_lines_inside_brackets_beginning(offset, text_beginning):
    '''
    GIVEN function invocation occupies two lines
    AND beginning text is of varied length
    AND offset is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = [offset + text_beginning + '(a, b,',
              '   c, d)']
    assert _properties_equal(
        parse_at_cursor((2, 0), buffer),
        [0, 1, len(offset), offset + text_beginning + '(', ['a', 'b', 'c', 'd'], ')'])

@pytest.mark.parametrize('text_ending', ['', ' #test'])
def test_parse_at_cursor_two_lines_inside_brackets_ending(text_ending):
    '''
    GIVEN function invocation occupies two lines
    AND ending text is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = ['this_is_test_function(',
              '    a, b, c, d)' + text_ending]
    assert _properties_equal(
        parse_at_cursor((2, 0), buffer),
        [0, 1, 0, 'this_is_test_function(', ['a', 'b', 'c', 'd'], ')' + text_ending])

@pytest.mark.parametrize(
    ['cursor_row', 'cursor_col'],
    [(1, 0), (1, 21), (1, 23), (2, 0), (2, 5), (2, 7)])
def test_parse_at_cursor_two_lines_cursor_positions(cursor_row, cursor_col):
    '''
    GIVEN function invocation occupies two lines
    AND some text is present at the end
    AND cursor position varies from top left to bottom right
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    AND result does not depend on cursor position
    '''
    buffer = ['this_is_test_function(a, b, ',
              ' c, d) #test']
    assert _properties_equal(
        parse_at_cursor((cursor_row, cursor_col), buffer),
        [0, 1, 0, 'this_is_test_function(', ['a', 'b', 'c', 'd'], ') #test'])

# TODO: add multiple lines tests (2 types with or without offset)


# # TODO: THE TESTS BELOW ARE TEMPORARY
# def test_temp_last_bracket_index_1():
#     buffer = ['test((a + b), c)']
#     actual = _get_last_closing_bracket_index((1, 0), buffer)
#     assert actual == (0, 15)
#
# def test_temp_last_bracket_index_2():
#     buffer = ['test((a + b), c) # comment']
#     actual = _get_last_closing_bracket_index((1, 0), buffer)
#     assert actual == (0, 15)
#
# @pytest.mark.parametrize('cursor_row', [1, 2])
# def test_temp_last_bracket_index_3(cursor_row):
#     buffer = [
#         'test(',
#         '    (a + b), c)',
#     ]
#     actual = _get_last_closing_bracket_index((cursor_row, 0), buffer)
#     assert actual == (1, 14)
#
# @pytest.mark.parametrize('cursor_row', [1, 2])
# def test_temp_last_bracket_index_4(cursor_row):
#     buffer = [
#         'test( # comment',
#         '    (a + b), c) # comment, a, b, c',
#     ]
#     actual = _get_last_closing_bracket_index((cursor_row, 0), buffer)
#     assert actual == (1, 14)
#
# @pytest.mark.parametrize('cursor_row', [1, 2, 3])
# def test_temp_last_bracket_index_5(cursor_row):
#     buffer = [
#         'test((a + b), # comment',
#         '    b + c,',
#         '    (c)) # comment',
#     ]
#     actual = _get_last_closing_bracket_index((cursor_row, 0), buffer)
#     assert actual == (2, 7)
#
# def test_temp_last_bracket_index_6():
#     buffer = ['test(']
#     assert _get_last_closing_bracket_index((1, 0), buffer) is None
#
# def test_temp_last_bracket_index_7():
#     buffer = [
#         'test(',
#         '    a, b, c'
#     ]
#     assert _get_last_closing_bracket_index((1, 0), buffer) is None
#
# def test_temp_first_bracket_index_1():
#     buffer = ['test((a + b), c)']
#     actual = _get_first_opening_bracket_index((0, 15), buffer)
#     assert actual == (0, 4)
#
# def test_temp_first_bracket_index_2():
#     buffer = ['test((a + b), c) # comment']
#     actual = _get_first_opening_bracket_index((0, 15), buffer)
#     assert actual == (0, 4)
#
# def test_temp_first_bracket_index_3():
#     buffer = [
#         'test(',
#         '    (a + b), c)',
#     ]
#     actual = _get_first_opening_bracket_index((1, 14), buffer)
#     assert actual == (0, 4)
#
# def test_temp_first_bracket_index_4():
#     buffer = [
#         'test( # comment',
#         '    (a + b), c) # comment, a, b, c',
#     ]
#     actual = _get_first_opening_bracket_index((1, 14), buffer)
#     assert actual == (0, 4)
#
# def test_temp_first_bracket_index_5():
#     buffer = [
#         'test((a + b), # comment',
#         '    b + c,',
#         '    (c)) # comment',
#     ]
#     actual = _get_first_opening_bracket_index((2, 7), buffer)
#     assert actual == (0, 4)
#
# def test_temp_first_bracket_index_6():
#     buffer = ['test(']
#     assert _get_first_opening_bracket_index(None, buffer) is None
#
# def test_temp_first_bracket_index_7():
#     buffer = [
#         'test(',
#         '    a, b, c'
#     ]
#     assert _get_first_opening_bracket_index(None, buffer) is None
#
# def test_temp_first_bracket_index_8():
#     buffer = [
#         'test(a + b), # comment',
#         '    b + c,',
#         '    (c)) # comment',
#     ]
#     assert _get_first_opening_bracket_index((2, 7), buffer) is None

# def test_temp_parse_arg_range_single_line():
#     buffer = ['test(a, b, c) #test']
#     assert _parse_arg_range((0, 4), (0, 12), buffer) == ('test(', ['a', 'b', 'c'], ') #test')
#
# def test_temp_parse_arg_range_two_lines():
#     buffer = ['test(',
#               '   a, b, c) #test']
#     assert _parse_arg_range((0, 4), (1, 10), buffer) == ('test(', ['a', 'b', 'c'], ') #test')
#
# def test_temp_parse_arg_range_multiple_lines():
#     buffer = ['   test(a,',
#               ' b,',
#               '   c, ',
#               'd   ) #test']
#     assert (_parse_arg_range((0, 7), (3, 4), buffer) ==
#             ('   test(', ['a', 'b', 'c', 'd'], ') #test'))

def _properties_equal(actual, expected):
    return all(actual.__dict__[_FIELD_NAMES[i]] == expected[i] for i in range(len(_FIELD_NAMES)))
