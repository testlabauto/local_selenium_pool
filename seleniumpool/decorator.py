import sys
from functools import wraps




def sel_pool(*decorator_args, **decorator_kwargs):  # the decorator
    def wrapper(f):  # a wrapper for the function
        @wraps(f)
        def decorated_function(*args, **kwargs):  # the decorated function

            out = kwargs.pop('output_queue')
            sys.stdout = out
            sys.stderr = out
            print('Starting {0}'.format(f.__name__))
            z = {**kwargs, **decorator_kwargs}
            y = {*args, *decorator_args}
            f(*y, **z)
            print('Finished {0}'.format(f.__name__))

            return f(*args, **kwargs)
        return decorated_function
    return wrapper