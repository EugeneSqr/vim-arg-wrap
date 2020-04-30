def find_args_range(row_cursor, col_cursor, buffer):
    row_index = _row_cursor_to_index(row_cursor)
    col_index = _col_cursor_to_index(col_cursor)
    line = buffer[row_index]
    return ((row_cursor, _col_index_to_cursor(_search_line_backward(line, '(', col_index))),
            (row_cursor, _col_index_to_cursor(_search_line_forward(line, ')', col_index))))

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

def _row_cursor_to_index(row_cursor):
    return row_cursor - 1

def _col_cursor_to_index(col_cursor):
    return col_cursor

def _row_index_to_cursor(row_index):
    return row_index + 1

def _col_index_to_cursor(col_index):
    return col_index
