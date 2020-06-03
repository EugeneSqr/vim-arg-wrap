from . import wrapper_sequence

def test_cycling_forward():
    sequence = wrapper_sequence.WrapperSequence(['A', 'B', 'C'])
    assert sequence.get_next_wrapper() == 'B'
    assert sequence.get_next_wrapper() == 'C'
    assert sequence.get_next_wrapper() == 'A'
    assert sequence.get_next_wrapper() == 'B'

def test_cycling_backward():
    sequence = wrapper_sequence.WrapperSequence(['A', 'B', 'C'])
    assert sequence.get_prev_wrapper() == 'C'
    assert sequence.get_prev_wrapper() == 'B'
    assert sequence.get_prev_wrapper() == 'A'
    assert sequence.get_prev_wrapper() == 'C'

def test_cycling_forward_single_wrapper():
    sequence = wrapper_sequence.WrapperSequence(['A'])
    assert sequence.get_next_wrapper() == 'A'

def test_cycling_backward_single_wrapper():
    sequence = wrapper_sequence.WrapperSequence(['A'])
    assert sequence.get_prev_wrapper() == 'A'

def test_mixed_cycling():
    sequence = wrapper_sequence.WrapperSequence(['A', 'B', 'C'])
    assert sequence.get_next_wrapper() == 'B'
    assert sequence.get_prev_wrapper() == 'A'
    assert sequence.get_prev_wrapper() == 'C'
    assert sequence.get_next_wrapper() == 'A'

def test_large_number_forward():
    sequence = wrapper_sequence.WrapperSequence(['A', 'B', 'C', 'D', 'E'])
    for _ in range(1024):
        wrapper = sequence.get_next_wrapper()
    assert wrapper == 'E'

def test_large_nubmer_backward():
    sequence = wrapper_sequence.WrapperSequence(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(1024):
        wrapper = sequence.get_prev_wrapper()
    assert wrapper == 'C'
