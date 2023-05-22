from typing import Optional, Tuple
from dataclasses import dataclass

from app.types import Cursor, VimBuffer
from .args_parser import parse_args_line

@dataclass
class RowsRange:
    start: int = 0
    end: int = 0
    start_indent: int = 0

@dataclass
class Signature:
    rows: RowsRange = RowsRange()
    beginning: str = ""
    args: Tuple[str, ...] = ()
    ending: str = ""

def signature_at_cursor(cursor: Cursor, buffer: VimBuffer) -> Signature:
    args_range = _get_args_range(cursor, buffer)
    if not args_range:
        return Signature()
    (start_row, start_col), (end_row, end_col) = args_range
    beginning = buffer[start_row][:start_col + 1]
    ending = buffer[end_row][end_col:]
    buffer_range_len = sum(len(buffer[index]) for index in range(start_row, end_row + 1))
    args_start = start_col + 1
    args_end = args_start + buffer_range_len - len(beginning) - len(ending)
    return Signature(
        rows=RowsRange(start_row, end_row, _get_line_indent(buffer[start_row])),
        beginning=beginning,
        args=parse_args_line(''.join(buffer[start_row:end_row + 1])[args_start:args_end]),
        ending=ending)

# TODO: consider removing Optional
def _get_args_range(cursor: Cursor,
                    buffer: VimBuffer) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    last_bracket_index = _get_last_closing_bracket_index(cursor, buffer)
    if not last_bracket_index:
        return None
    first_bracket_index = _get_first_opening_bracket_index(last_bracket_index, buffer)
    if not first_bracket_index:
        return None
    return first_bracket_index, last_bracket_index

# TODO: consider removing cols to avoid unnecessary Tuples down the road
def _cursor_to_index(cursor: Cursor) -> Tuple[int, int]:
    row, col = cursor
    return row - 1, col

# TODO: consider removing Optional
def _get_last_closing_bracket_index(cursor: Cursor, buffer: VimBuffer) -> Optional[Tuple[int, int]]:
    row_index, _ = _cursor_to_index(cursor)
    for current_row_index in range(row_index, len(buffer)):
        line = buffer[current_row_index]
        last_bracket_col_index = line.rfind(')', 0, len(line))
        if last_bracket_col_index != -1:
            if last_bracket_col_index == len(line) - 1:
                return current_row_index, last_bracket_col_index
            ending_col_index = _skip_spaces_after_last_closing_bracket(line, last_bracket_col_index)
            if _is_ending_commented_out(line, ending_col_index):
                return current_row_index, last_bracket_col_index
    return None

def _skip_spaces_after_last_closing_bracket(line: str, index: int) -> int:
    ending_index = index + 1
    while ending_index < len(line) and line[ending_index] == ' ':
        ending_index += 1
    return ending_index

def _is_ending_commented_out(line: str, index: int) -> bool:
    return line[index] not in [',', '(', '[']

def _get_first_opening_bracket_index(last_closing_bracket_index: Optional[Tuple[int, int]],
                                     buffer: VimBuffer) -> Optional[Tuple[int, int]]:
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

def _update_bracket_balance(current_char: str, bracket_balance: int) -> int:
    if current_char == '(':
        bracket_balance -= 1
    elif current_char == ')':
        bracket_balance += 1
    return bracket_balance

def _get_line_indent(line: str) -> int:
    indent = 0
    if line:
        for char in line:
            if char != ' ':
                break
            indent += 1

    return indent
