from . import wrapper_nowrap

def test_nowrap_wrap_args_single_line(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '   def nowrap_func():',
        '      nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'start_row_indent': 6,
        'beginning': '      nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(3).wrap_args((2, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '   def nowrap_func():',
        '      nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_wrap_args_two_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 3, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((4, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_wrap_args_multiple_lines(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(',
        '            nowrap_a,',
        '            nowrap_b,',
        '            nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 5, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((6, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]

def test_nowrap_wrap_args_multiple_lines_below_first(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a,',
        '                      nowrap_b,',
        '                      nowrap_c)',
        ' # nowrap end comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 4, 'start_row_indent': 8,
        'beginning': '        nowrap_method(',
        'args': ['nowrap_a', 'nowrap_b', 'nowrap_c'],
        'ending': ')',
    })
    wrapper_nowrap.ArgWrapperNoWrap(4).wrap_args((5, 0), buffer)
    assert buffer == [
        ' # nowrap begin comment',
        '    def nowrap_func():',
        '        nowrap_method(nowrap_a, nowrap_b, nowrap_c)',
        ' # nowrap end comment',
    ]
