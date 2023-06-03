from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class BracketBalance:
    opening: str
    closing: str
    balance: int = 0

def parse_args_line(args_line: str) -> Tuple[str, ...]:
    args: List[str] = []
    current_arg = ''
    bracket_balances = [
        BracketBalance('(', ')'),
        BracketBalance('[', ']'),
        BracketBalance('{', '}'),
    ]

    for char in args_line:
        if char == ',':
            if _brackets_balanced(bracket_balances):
                _append_arg(args, current_arg)
                current_arg = ''
            else:
                current_arg += char
        else:
            current_arg += char
            if not _bracket_balances_valid(bracket_balances, char):
                break
    _append_arg(args, current_arg)
    return tuple(args) if args else (args_line,)

def _append_arg(args: List[str], current_arg: str = '') -> None:
    current_arg = current_arg.strip()
    if current_arg:
        args.append(current_arg)

def _update_bracket_balance(bracket_balance: BracketBalance, char: str) -> None:
    if char == bracket_balance.opening:
        bracket_balance.balance += 1
    elif char == bracket_balance.closing:
        bracket_balance.balance -= 1

def _brackets_balanced(bracket_balances: List[BracketBalance]) -> bool:
    return all(b.balance == 0 for b in bracket_balances)

def _bracket_balances_valid(bracket_balances: List[BracketBalance], char: str) -> bool:
    for bracket_balance in bracket_balances:
        _update_bracket_balance(bracket_balance, char)
        if bracket_balance.balance < 0:
            return False
    return True
