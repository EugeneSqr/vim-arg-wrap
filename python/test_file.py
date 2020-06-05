# pylint:disable-all
# comment line goes here
def method_invocation(first, second, third):
    result = first + second + third
    return result

def some_other_func():
    # nowrap
    nowrap = method_invocation('first', 'second', 'third')
    # nowrap end
    # a
    a = method_invocation(
        'first', 'second', 'third')
    # a end
    # b
    a = method_invocation(
        'first',
        'second',
        'third')
    # b end
    # c
    a = method_invocation('first',
                          'second',
                          'third')
    # c end
