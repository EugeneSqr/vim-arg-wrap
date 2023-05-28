from unittest.mock import Mock

from app.wrappers import wrapper_sequence
from app.conftest import VimBufferMock

def test_first_next_to_second() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_next(cursor, buffer)
    wrapper_mocks[1].wrap_args.assert_called_once_with(cursor, buffer)

def test_second_next_to_thrird() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(True),
        _create_wrapper(False),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_next(cursor, buffer)
    wrapper_mocks[2].wrap_args.assert_called_once_with(cursor, buffer)

def test_last_next_to_first() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_next(cursor, buffer)
    wrapper_mocks[0].wrap_args.assert_called_once_with(cursor, buffer)

def test_last_back_to_last_but_one() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_prev(cursor, buffer)
    wrapper_mocks[2].wrap_args.assert_called_once_with(cursor, buffer)

def test_first_back_to_last() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_prev(cursor, buffer)
    wrapper_mocks[-1].wrap_args.assert_called_once_with(cursor, buffer)

def test_third_back_to_second() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(True),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_prev(cursor, buffer)
    wrapper_mocks[1].wrap_args.assert_called_once_with(cursor, buffer)

def test_first_next_to_second_multiple_recognized() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_next(cursor, buffer)
    wrapper_mocks[1].wrap_args.assert_called_once_with(cursor, buffer)

def test_first_back_to_last_multiple_recognized() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    cursor, buffer = (0, 0), VimBufferMock([])
    sequence.wrap_prev(cursor, buffer)
    wrapper_mocks[-1].wrap_args.assert_called_once_with(cursor, buffer)

def _create_wrapper(should_recognize: bool):
    return type('', (), {
        'recognized': Mock(return_value=should_recognize),
        'wrap_args': Mock(),
    })
