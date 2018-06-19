import sys

def fixture_decorator(test_function):
    def wrapper(**kwargs):
        oq = kwargs.pop('output_queue')
        sys.stdout = oq
        sys.stderr = oq
        print('Starting {0}'.format(test_function.__name__))
        test_function(**kwargs)
        print('Finished {0}'.format(test_function.__name__))

    return wrapper
