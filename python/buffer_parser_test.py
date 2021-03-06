from contextlib import contextmanager
from unittest.mock import Mock

import pytest

import buffer_parser

_FIELD_NAMES = [
    'start_row_index',
    'end_row_index',
    'start_row_indent',
    'beginning',
    'args',
    'ending',
]

@pytest.fixture(name='arrange_parse_args_line')
def fixture_arrange_parse_args_line(monkeypatch):
    @contextmanager
    def create_mock(args_line, expected_args):
        mock = Mock(return_value=expected_args)
        monkeypatch.setattr(buffer_parser, 'parse_args_line', mock)
        yield mock
        # normally a try catch wrapper is needed here, however if something goes
        # wrong inside tests, we don't want the assertion to be checked to prevent extra error
        # output, which may hide the main problem
        mock.assert_called_once_with(args_line)

    return create_mock

def test_parse_at_cursor_no_opening_bracket():
    '''
    GIVEN function invocation occupies single line
    AND opening bracket is absent
    WHEN parsing the buffer range
    THEN empty parsed range is returned
    '''
    buffer = ['test)']
    assert buffer_parser.parse_at_cursor((1, 0), buffer) is None

def test_parse_at_cursor_no_closing_bracket():
    '''
    GIVEN function invocation occupies single line
    AND closing bracket is absent
    WHEN parsing the buffer range
    THEN empty parsed range is returned
    '''
    buffer = ['test(',
              '     a, b,',
              '     c']
    assert buffer_parser.parse_at_cursor((1, 0), buffer) is None

@pytest.mark.parametrize(
    ['offset', 'text_beginning'],
    [('', ''), ('    ', 'test'), ('  ', '')])
def test_parse_at_cursor_single_line_inside_brackets_beginning(offset,
                                                               text_beginning,
                                                               arrange_parse_args_line):
    '''
    GIVEN function invocation occupies single line
    AND beginning text is of varied length
    AND offset is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = [offset + text_beginning + '(a, b, c, d)']
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a, b, c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((1, len(offset) + len(text_beginning) + 1), buffer),
            [0, 0, len(offset), offset + text_beginning + '(', expected_args, ')'])

@pytest.mark.parametrize('text_ending', ['', ' #test'])
def test_parse_at_cursor_single_line_inside_brackets_ending(text_ending, arrange_parse_args_line):
    '''
    GIVEN function invocation occupies single line
    AND ending text is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = ['this_is_test_function(a, b, c, d)' + text_ending]
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a, b, c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((1, 23), buffer),
            [0, 0, 0, 'this_is_test_function(', expected_args, ')' + text_ending])

@pytest.mark.parametrize('cursor_col', [0, 21, 23, 32, 36])
def test_parse_at_cursor_single_line_cursor_positions(cursor_col, arrange_parse_args_line):
    '''
    GIVEN function invocation occupies single line
    AND some text is present at the end
    AND cursor position varies from left to right
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    AND result does not depend on cursor position
    '''
    buffer = ['this_is_test_function(a, b, c, d) #test']
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a, b, c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((1, cursor_col), buffer),
            [0, 0, 0, 'this_is_test_function(', expected_args, ') #test'])

@pytest.mark.parametrize(
    ['offset', 'text_beginning'],
    [('', ''), ('    ', 'test'), ('  ', '')])
def test_parse_at_cursor_two_lines_inside_brackets_beginning(offset,
                                                             text_beginning,
                                                             arrange_parse_args_line):
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
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a, b,   c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((2, 0), buffer),
            [0, 1, len(offset), offset + text_beginning + '(', expected_args, ')'])

@pytest.mark.parametrize('text_ending', ['', ' #test'])
def test_parse_at_cursor_two_lines_inside_brackets_ending(text_ending, arrange_parse_args_line):
    '''
    GIVEN function invocation occupies two lines
    AND ending text is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = ['this_is_test_function(',
              '    a, b, c, d)' + text_ending]
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('    a, b, c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((2, 0), buffer),
            [0, 1, 0, 'this_is_test_function(', expected_args, ')' + text_ending])

@pytest.mark.parametrize(
    ['cursor_row', 'cursor_col'],
    [(1, 0), (1, 21), (1, 23), (2, 0), (2, 5), (2, 7)])
def test_parse_at_cursor_two_lines_cursor_positions(cursor_row,
                                                    cursor_col,
                                                    arrange_parse_args_line):
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
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a, b,  c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((cursor_row, cursor_col), buffer),
            [0, 1, 0, 'this_is_test_function(', expected_args, ') #test'])

@pytest.mark.parametrize(
    ['offset', 'text_beginning'],
    [('', ''), ('    ', 'test'), ('  ', '')])
def test_parse_at_cursor_multiple_lines_inside_brackets_beginning(offset,
                                                                  text_beginning,
                                                                  arrange_parse_args_line):
    '''
    GIVEN function invocation occupies multiple lines
    AND beginning text is of varied length
    AND offset is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = [offset + text_beginning + '(a,',
              '   b,',
              '   c, ',
              '   d)']
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a,   b,   c,    d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((2, 0), buffer),
            [0, 3, len(offset), offset + text_beginning + '(', expected_args, ')'])

@pytest.mark.parametrize('text_ending', ['', ' #test'])
def test_parse_at_cursor_multiple_lines_inside_brackets_ending(text_ending,
                                                               arrange_parse_args_line):
    '''
    GIVEN function invocation occupies multiple lines
    AND ending text is of varied length
    AND cursor position is inside brackets
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    '''
    buffer = ['this_is_test_function(',
              '    a, ',
              '    b, ',
              '    c, d)' + text_ending]
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('    a,     b,     c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((2, 0), buffer),
            [0, 3, 0, 'this_is_test_function(', expected_args, ')' + text_ending])

@pytest.mark.parametrize(
    ['cursor_row', 'cursor_col'],
    [(1, 0), (1, 21), (1, 23), (2, 0), (2, 2), (3, 1), (4, 3)])
def test_parse_at_cursor_multiple_lines_cursor_positions(cursor_row,
                                                         cursor_col,
                                                         arrange_parse_args_line):
    '''
    GIVEN function invocation occupies multiple lines
    AND some text is present at the end
    AND cursor position varies from top left to bottom right
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    AND result does not depend on cursor position
    '''
    buffer = ['this_is_test_function(a,',
              'b, ',
              ' c, ',
              'd) #test']
    expected_args = ['a', 'b', 'c', 'd']
    with arrange_parse_args_line('a,b,  c, d', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((cursor_row, cursor_col), buffer),
            [0, 3, 0, 'this_is_test_function(', expected_args, ') #test'])

@pytest.mark.parametrize(
    ['cursor_row', 'cursor_col'],
    [(1, 0), (1, 5), (1, 7), (2, 5), (3, 0), (3, 5), (3, 8)])
def test_extra_brackets(cursor_row, cursor_col, arrange_parse_args_line):
    '''
    GIVEN function invocation occupies multiple lines
    AND there are a few extra brackets
    AND cursor position varies from top left to bottom right
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    AND result does not depend on cursor position
    '''
    buffer = ['test((a) + (b), ',
              '    (b + c), d,',
              '    (f)) # comment']
    expected_args = ['(a) + (b)', '(b + c)', 'd', '(f)']
    with arrange_parse_args_line(
            '(a) + (b),     (b + c), d,    (f)', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((cursor_row, cursor_col), buffer),
            [0, 2, 0, 'test(', expected_args, ') # comment'])

@pytest.mark.parametrize(
    ['cursor_row', 'cursor_col'],
    [(1, 0), (1, 5), (2, 9), (3, 17), (3, 19), (4, 1)])
def test_nested_invocations_with_square_brackets(cursor_row, cursor_col, arrange_parse_args_line):
    '''
    GIVEN function invocation occupies multiple lines
    AND there are a few nested function invocations
    AND some function results are accessed by index
    AND some function resutls are functions that are invoked
    AND cursor position varies from top left to bottom right
    WHEN parsing the buffer range
    THEN the data is extracted correctly
    AND result does not depend on cursor position
    '''
    buffer = [
        'test(',
        '    n_1(a)(a1),',
        '    n_2(n_3(b))[0],',
        '    n_4(c))'
    ]
    expected_args = ['n_1(a)(a1)', 'n_2(n_3(b))[0]', 'n_4(c)']
    with arrange_parse_args_line('    n_1(a)(a1),    n_2(n_3(b))[0],    n_4(c)', expected_args):
        assert _properties_equal(
            buffer_parser.parse_at_cursor((cursor_row, cursor_col), buffer),
            [0, 3, 0, 'test(', expected_args, ')'])

def _properties_equal(actual, expected):
    return all(actual.__dict__[_FIELD_NAMES[i]] == expected[i] for i in range(len(_FIELD_NAMES)))
