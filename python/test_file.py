# pylint:disable-all
# comment line goes here
def method_invocation(first, second, third):
    result = first + second + third
    return result

def some_other_func():
    # comment
    some_result = method_invocation('first', 'second', 'third')
    # another comment
