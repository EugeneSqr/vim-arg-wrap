from . import wrapper_b

def test_b_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(7).wrap_args((3, 1), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '               b_a,',
        '               b_b,',
        '               b_c)',
        ' # b end comment',
    ]

def test_b_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a, b_b, b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(0).wrap_args((4, 0), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '        b_a,',
        '        b_b,',
        '        b_c)',
        ' # b end comment',
    ]

def test_b_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(4).wrap_args((6, 0), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '            b_a,',
        '            b_b,',
        '            b_c)',
        ' # b end comment',
    ]

def test_b_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # b begin comment',
        '    def b_func():',
        '        b_method(b_a,',
        '                 b_b,',
        '                 b_c)',
        ' # b end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        b_method(',
        'args': ['b_a', 'b_b', 'b_c'],
        'ending': ')',
    })
    wrapper_b.ArgWrapperB(2).wrap_args((5, 0), buffer)
    assert buffer == [
        ' # b begin comment',
        '    def b_func():',
        '        b_method(',
        '          b_a,',
        '          b_b,',
        '          b_c)',
        ' # b end comment',
    ]
