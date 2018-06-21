import multiprocessing_on_dill as multiprocessing
from multiprocessing_on_dill.queues import JoinableQueue
from loselpo.output_parser import TestOutputParser
from loselpo.output_queue import TestRunOutput
from loselpo.selenium_worker import SeleniumWorker
import time


start = None
output_queue = None
name = None

def create_pool(test_name, chrome_options, processes=multiprocessing.cpu_count()):
    global start, output_queue, name
    start = time.time()
    name = test_name

    output_queue = TestRunOutput()
    ctx = multiprocessing.get_context()
    input_queue = JoinableQueue(ctx=ctx)

    workers = []
    for i in range(processes):
        workers.append(SeleniumWorker(input_queue, output_queue, chrome_options).start())

    return input_queue, output_queue


def wait_for_pool_completion(input_queue):
    global start, output_queue, name
    input_queue.join()

    return TestOutputParser().parse(start, output_queue, name)


def auto_fill_queue(module, input_queue, prefix='test_'):
    test_func_names = []
    for x in dir(module):
        if x.startswith(prefix):
            test_func_names.append(x)
    for test_func_name in test_func_names:
        func = getattr(module, test_func_name)
        if callable(func):
            input_queue.put(func)

