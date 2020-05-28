def parse_at_cursor(cursor, buffer):
    arg_range = _get_arg_range(cursor, buffer)
    if not arg_range:
        return None
    (start_row, start_col), (end_row, end_col) = arg_range
    beginning = buffer[start_row][:start_col + 1]
    ending = buffer[end_row][end_col:]
    buffer_range_len = sum(len(buffer[index]) for index in range(start_row, end_row + 1))
    arg_line_start = start_col + 1
    arg_line_len = buffer_range_len - len(beginning) - len(ending)
    arg_line = ''.join(buffer[start_row:end_row + 1])[arg_line_start:arg_line_start + arg_line_len]
    return type('', (), {
        'start_row_index': start_row,
        'end_row_index': end_row,
        'start_row_indent': _get_line_indent(buffer[start_row]),
        'beginning': beginning,
        'args': _line_to_args(arg_line),
        'ending': ending,
    })

def _get_arg_range(cursor, buffer):
    last_bracket_index = _get_last_closing_bracket_index(cursor, buffer)
    if not last_bracket_index:
        return None
    first_bracket_index = _get_first_opening_bracket_index(last_bracket_index, buffer)
    if not first_bracket_index:
        return None
    return first_bracket_index, last_bracket_index

def _cursor_to_index(cursor):
    row, col = cursor
    return row - 1, col

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

def _get_line_indent(line):
    indent = 0
    if line:
        for char in line:
            if char != ' ':
                break
            indent += 1

    return indent

def _line_to_args(args):
    return list(map(str.strip, args.split(',')))
