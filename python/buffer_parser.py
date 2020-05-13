def parse_at_cursor(cursor, buffer):
    (start_row, start_col), (end_row, end_col) = _get_args_range(cursor, buffer)
    start_line = buffer[start_row]
    return type('', (), {
        'start_row_index': start_row,
        'end_row_index': end_row,
        'indent': _get_line_indent(start_line),
        'beginning': start_line[:start_col],
        'args': _parse_args_string(start_line[start_col:end_col + 1]),
        'ending': buffer[end_row][end_col + 1:],
    })

def _get_args_range(cursor, buffer):
    row_index, col_index = _cursor_to_index(cursor)
    line = buffer[row_index]
    return ((row_index, _find_start_col_index(line, '(', col_index)),
            (row_index, _find_end_col_index(line, ')', col_index)))

def _cursor_to_index(cursor):
    row, col = cursor
    return row - 1, col

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

def _get_line_indent(line):
    indent = 0
    if line:
        for char in line:
            if char != ' ':
                break
            indent += 1

    return indent

def _parse_args_string(args):
    return list(map(str.strip, args.split(',')))

def _get_last_closing_bracket_index(cursor, buffer):
    row_index, _ = _cursor_to_index(cursor)
    for current_row_index in range(row_index, len(buffer)):
        line = buffer[current_row_index]
        last_bracket_col_index = line.rfind(')', 0, len(line))
        if last_bracket_col_index != -1:
            if last_bracket_col_index == len(line) - 1:
                return current_row_index, last_bracket_col_index
            ending_col_index = _skip_spaces_after_last_closing_bracket(line, last_bracket_col_index)
            if ending_col_index == len(line) or line[ending_col_index] != ',':
                return current_row_index, last_bracket_col_index
    return None

def _skip_spaces_after_last_closing_bracket(line, index):
    ending_index = index + 1
    while ending_index < len(line) and line[ending_index] == ' ':
        ending_index += 1
    return ending_index

def _get_first_opening_bracket_index(last_closing_bracket_index, buffer):
    if last_closing_bracket_index is None:
        return None
    row_index, col_index = last_closing_bracket_index
    bracket_balance = 0
    for current_row_index in range(row_index, -1, -1):
        line = buffer[current_row_index]
        if current_row_index != row_index:
            col_index = len(line) - 1
        for current_col_index in range(col_index, -1, -1):
            bracket_balance = _update_bracket_balance(line[current_col_index], bracket_balance)
            if bracket_balance == 0:
                return current_row_index, current_col_index
    return None

def _update_bracket_balance(current_char, bracket_balance):
    if current_char == '(':
        bracket_balance -= 1
    elif current_char == ')':
        bracket_balance += 1
    return bracket_balance
