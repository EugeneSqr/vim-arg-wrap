from typing import Optional, Tuple
from dataclasses import dataclass

from app.types import VimCursor, VimBuffer
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

BracketPosition = Tuple[int, int]

def signature_at_cursor(cursor: VimCursor, buffer: VimBuffer) -> Signature:
    args_range = _get_args_range(cursor, buffer)
    if not args_range:
        return Signature()
    (start_row, start_col), (end_row, end_col) = args_range
    beginning = buffer[start_row][:start_col + 1]
    ending = buffer[end_row][end_col:]
    buffer_range_len = sum(len(buffer[row]) for row in range(start_row, end_row + 1))
    args_start = start_col + 1
    args_end = args_start + buffer_range_len - len(beginning) - len(ending)
    return Signature(
        rows=RowsRange(start_row, end_row, _get_line_indent(buffer[start_row])),
        beginning=beginning,
        args=parse_args_line(''.join(buffer[start_row:end_row + 1])[args_start:args_end]),
        ending=ending)

def _get_args_range(cursor: VimCursor,
                    buffer: VimBuffer) -> Optional[Tuple[BracketPosition, BracketPosition]]:
    last_bracket_position = _get_last_closing_bracket_position(cursor, buffer)
    if not last_bracket_position:
        return None
    first_bracket_position = _get_first_opening_bracket_position(last_bracket_position, buffer)
    if not first_bracket_position:
        return None
    return first_bracket_position, last_bracket_position

def _get_last_closing_bracket_position(cursor: VimCursor,
                                       buffer: VimBuffer) -> Optional[BracketPosition]:
    row = cursor[0] - 1
    for current_row in range(row, len(buffer)):
        line = buffer[current_row]
        last_bracket_col = line.rfind(')', 0, len(line))
        if last_bracket_col != -1:
            if last_bracket_col == len(line) - 1:
                return current_row, last_bracket_col
            ending_col = _skip_spaces_after_last_closing_bracket(line, last_bracket_col)
            if _is_ending_commented_out(line, ending_col):
                return current_row, last_bracket_col
    return None

def _get_first_opening_bracket_position(last_closing_bracket_position: Optional[BracketPosition],
                                        buffer: VimBuffer) -> Optional[BracketPosition]:
    if last_closing_bracket_position is None:
        return None
    row, col = last_closing_bracket_position
    bracket_balance = 0
    for current_row in range(row, -1, -1):
        line = buffer[current_row]
        if current_row != row:
            col = len(line) - 1
        for current_col in range(col, -1, -1):
            bracket_balance = _update_bracket_balance(line[current_col], bracket_balance)
            if bracket_balance == 0:
                return current_row, current_col
    return None

def _skip_spaces_after_last_closing_bracket(line: str, col: int) -> int:
    ending_col = col + 1
    while ending_col < len(line) and line[ending_col] == ' ':
        ending_col += 1
    return ending_col

def _is_ending_commented_out(line: str, col: int) -> bool:
    return line[col] not in [',', '(', '[']

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
