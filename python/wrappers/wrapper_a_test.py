from . import wrapper_a

def test_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    def a_func():',
        '        a_method(a_a, a_b, a_c)',
    ])
    mock_parse_at_cursor({
        'start_row_index': 1, 'end_row_index': 1, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(4).wrap_args((3, 1), buffer)
    assert buffer == [
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
    ]

def test_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
    ])
    mock_parse_at_cursor({
        'start_row_index': 1, 'end_row_index': 2, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(4).wrap_args((4, 0), buffer)
    assert buffer == [
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
    ]

def test_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    def a_func():',
        '        a_method(',
        '            a_a,',
        '            a_b,',
        '            a_c)',
    ])
    mock_parse_at_cursor({
        'start_row_index': 1, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(4).wrap_args((6, 0), buffer)
    assert buffer == [
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
    ]

def test_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    def a_func():',
        '        a_method(a_a,',
        '                 a_b,',
        '                 a_c)',
    ])
    mock_parse_at_cursor({
        'start_row_index': 1, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(4).wrap_args((5, 0), buffer)
    assert buffer == [
        '    def a_func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
    ]
