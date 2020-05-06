def get_args_range(cursor, buffer):
    row_index, col_index = _cursor_to_index(cursor)
    line = buffer[row_index]
    return ((row_index, _find_start_col_index(line, '(', col_index)),
            (row_index, _find_end_col_index(line, ')', col_index)))

def get_line_indent(line):
    indent = 0
    if line:
        for char in line:
            if char != ' ':
                break
            indent += 1

    return indent

def _find_start_col_index(search_in, search_for, right_index):
    match_index = search_in.rfind(search_for, 0, right_index)
    if match_index == -1:
        match_index = search_in.find(search_for, right_index, len(search_in))
    return match_index + 1

def _find_end_col_index(search_in, search_for, right_index):
    match_index = search_in.find(search_for, right_index, len(search_in))
    if match_index == -1:
        match_index = search_in.rfind(')', 0, right_index)
    return match_index - 1

def _cursor_to_index(cursor):
    row, col = cursor
    return row - 1, col
