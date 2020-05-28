from . import wrapper_a

def test_wrap_args(arrange_vim_buffer, mock_parse_at_cursor):
    buffer = arrange_vim_buffer([
        '    # comment line goes here',
        '    def func():',
        '        a_method(a_a, a_b, a_c)',
        '# a comment',
    ])
    mock_parse_at_cursor({
        'start_row_index': 2, 'end_row_index': 2, 'indent': 8,
        'beginning': '        a_method(',
        'args': ['a_a', 'a_b', 'a_c'],
        'ending': ')',
    })
    wrapper_a.ArgWrapperA(4).wrap_args((3, 1), buffer)
    assert buffer == [
        '    # comment line goes here',
        '    def func():',
        '        a_method(',
        '            a_a, a_b, a_c)',
        '# a comment',
    ]
