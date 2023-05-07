from typing import Tuple, List

def parse_args_line(args_line: str) -> Tuple[str, ...]:
    args: List[str] = []
    current_arg = ''
    brackets_balance = _BracketsBalance([('(', ')'), ('[', ']'), ('{', '}')])

    for char in args_line:
        if char == ',':
            if brackets_balance.is_balanced():
                _append_arg(args, current_arg)
                current_arg = ''
            else:
                current_arg += char
        else:
            current_arg += char
            if not brackets_balance.is_valid(char):
                break
    _append_arg(args, current_arg)
    return tuple(args) if args else (args_line,)

def _append_arg(args: List[str], current_arg: str = '') -> None:
    current_arg = current_arg.strip()
    if current_arg:
        args.append(current_arg)

# TODO: replace with dataclasses
class _BracketsBalance():
    def __init__(self, bracket_pairs: List[Tuple[str, str]]):
        self._balances_by_bracket_type = list(map(_BracketTypeBalance, bracket_pairs))

    def is_balanced(self) -> bool:
        return all(map(lambda _: _.get() == 0, self._balances_by_bracket_type))

    def is_valid(self, char: str) -> bool:
        def bracket_type_balance_valid(bracket_type_balance: _BracketTypeBalance) -> bool:
            bracket_type_balance.update(char)
            return bracket_type_balance.get() >= 0

        return all(map(bracket_type_balance_valid, self._balances_by_bracket_type))

# TODO: replace with dataclasses
class _BracketTypeBalance():
    def __init__(self, bracket_pair: Tuple[str, str]):
        self._opening_bracket, self._closing_bracket = bracket_pair
        self._balance = 0

    def get(self) -> int:
        return self._balance

    def update(self, char: str) -> None:
        if char == self._opening_bracket:
            self._balance += 1
        elif char == self._closing_bracket:
            self._balance -= 1
