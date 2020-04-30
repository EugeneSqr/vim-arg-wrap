def find_args_range(cursor_row, cursor_col, buffer):
    row_index, col_index = _cursor_to_index(cursor_row, cursor_col)
    line = buffer[row_index]
    return ((cursor_row, _index_to_cursor(_search_line_backward(line, '(', col_index))),
            (cursor_row, _index_to_cursor(_search_line_forward(line, ')', col_index))))

def _search_line_backward(search_in, search_for, right_index):
    match_index = search_in.rfind(search_for, 0, right_index)
    if match_index == -1:
        match_index = search_in.find(search_for, right_index, len(search_in))
    return match_index

def _search_line_forward(search_in, search_for, right_index):
    match_index = search_in.find(search_for, right_index, len(search_in))
    if match_index == -1:
        match_index = search_in.rfind(')', 0, right_index)
    return match_index

def _cursor_to_index(cursor_row, cursor_col):
    return cursor_row - 1, cursor_col - 1

def _index_to_cursor(index):
    return index + 1
