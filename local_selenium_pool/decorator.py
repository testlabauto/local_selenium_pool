import sys
from functools import wraps


def sel_pool(**decorator_kwargs):
    """
    Decorator used to redirect stdout to the queue and, optionally, pass arguments to the test.
    Logging before and after f(**z) is not optional.  It is used as part of the process of parsing
    the unstructured stdout data from the queue.
    :param decorator_kwargs: optional args to pass to test (to data drive a test)
    :return: test function with stdout redirected to queue
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(**kwargs):
            out = kwargs.pop('output_queue')
            sys.stdout = out
            merged = {**kwargs, **decorator_kwargs}
            copy_of_merged = {**kwargs, **decorator_kwargs}
            del copy_of_merged['driver']
            if len(copy_of_merged) > 0:
                print('Starting {0}({1})'.format(f.__name__,
                      ', '.join('%s=%r' % x for x in copy_of_merged.items())))
            else:
                print('Starting {0}'.format(f.__name__))
            f(**merged)
            print('Finished {0}'.format(f.__name__))
        return decorated_function
    return wrapper