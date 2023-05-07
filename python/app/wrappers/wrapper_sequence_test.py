from unittest.mock import Mock

from app.wrappers import wrapper_sequence

def test_first_next_to_second() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_next('fake cursor', 'fake buffer')
    wrapper_mocks[1].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_second_next_to_thrird() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(True),
        _create_wrapper(False),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_next('fake cursor', 'fake buffer')
    wrapper_mocks[2].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_last_next_to_first() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_next('fake cursor', 'fake buffer')
    wrapper_mocks[0].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_last_back_to_last_but_one() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_prev('fake cursor', 'fake buffer')
    wrapper_mocks[2].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_first_back_to_last() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_prev('fake cursor', 'fake buffer')
    wrapper_mocks[-1].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_third_back_to_second() -> None:
    wrapper_mocks = [
        _create_wrapper(False),
        _create_wrapper(False),
        _create_wrapper(True),
        _create_wrapper(False),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_prev('fake cursor', 'fake buffer')
    wrapper_mocks[1].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_first_next_to_second_multiple_recognized() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_next('fake cursor', 'fake buffer')
    wrapper_mocks[1].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def test_first_back_to_last_multiple_recognized() -> None:
    wrapper_mocks = [
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
        _create_wrapper(True),
    ]
    sequence = wrapper_sequence.WrapperSequence(wrapper_mocks)
    sequence.wrap_prev('fake cursor', 'fake buffer')
    wrapper_mocks[-1].wrap_args.assert_called_once_with('fake cursor', 'fake buffer')

def _create_wrapper(should_recognize):
    return type('', (), {
        'recognized': Mock(return_value=should_recognize),
        'wrap_args': Mock(),
    })
