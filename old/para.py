import inspect
try:
    # Python 2
    from future_builtins import filter
except ImportError:
    # Python 3
    pass


class Foo(object):
    def foo1(self):
        print('foo1')

    def foo2(self):
        print('foo2')

    def foo3(self, required_arg):
        print('foo3({!r})'.format(required_arg))

f = Foo()
attrs = (getattr(f, name) for name in dir(f))
methods = filter(inspect.ismethod, attrs)
for method in methods:
    try:
        method()
    except TypeError:
        # Can't handle methods with required arguments.
        pass