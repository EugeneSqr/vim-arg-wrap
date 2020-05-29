from . import wrapper_nowrap

def test_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '   # comment line goes here',
        '   def func():',
        '      nowrap_method(no_wrap_a, nowrap_b, no_wrap_c)',
        '# nowrap comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 6,
        'beginning': '      nowrap_method(',
        'args': ['no_wrap_a', 'nowrap_b', 'no_wrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((2, 0), buffer)
    assert buffer == [
        '   # comment line goes here',
        '   def func():',
        '      nowrap_method(no_wrap_a, nowrap_b, no_wrap_c)',
        '# nowrap comment',
    ]

def test_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    # comment line goes here',
        '    def func():',
        '        nowrap_method(',
        '            no_wrap_a, nowrap_b, no_wrap_c)',
        '# nowrap comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['no_wrap_a', 'nowrap_b', 'no_wrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((4, 0), buffer)
    assert buffer == [
        '    # comment line goes here',
        '    def func():',
        '        nowrap_method(no_wrap_a, nowrap_b, no_wrap_c)',
        '# nowrap comment',
    ]

def test_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    # comment line goes here',
        '    def func():',
        '        nowrap_method(',
        '            no_wrap_a,',
        '            nowrap_b,',
        '            no_wrap_c)',
        '# nowrap comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['no_wrap_a', 'nowrap_b', 'no_wrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((6, 0), buffer)
    assert buffer == [
        '    # comment line goes here',
        '    def func():',
        '        nowrap_method(no_wrap_a, nowrap_b, no_wrap_c)',
        '# nowrap comment',
    ]

def test_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    # comment line goes here',
        '    def func():',
        '        nowrap_method(no_wrap_a,',
        '                      nowrap_b,',
        '                      no_wrap_c)',
        '# nowrap comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['no_wrap_a', 'nowrap_b', 'no_wrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((5, 0), buffer)
    assert buffer == [
        '    # comment line goes here',
        '    def func():',
        '        nowrap_method(no_wrap_a, nowrap_b, no_wrap_c)',
        '# nowrap comment',
    ]
