import multiprocessing_on_dill as multiprocessing
from multiprocessing_on_dill.queues import JoinableQueue
from local_selenium_pool.output_parser import TestOutputParser
from local_selenium_pool.output_queue import TestRunOutput
from local_selenium_pool.selenium_worker import SeleniumWorker
import time


start = None
output_queue = None
name = None

def create_pool(test_name, chrome_options, processes=multiprocessing.cpu_count()):
    """
    This method creates the test pool and returns.  Tests need to be added to the input queue quickly after calling this
    or else the pool will exit due to an empty input queue
    :param test_name: The test name will be used as the name field in the output JSON report
    :param chrome_options: These are the options sent to the browser.  Using these options you can, among other things,
    control whether or not the browsers run headless
    :param processes: This is the count of Selenium webdriver processes the pool should have in it
    :return: The input and output queues
    """
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
    """
    This method will block until all tests have been executed, then return the test results report
    :param input_queue: The queue to join
    :return: A parsed test report
    """
    global start, output_queue, name
    input_queue.join()

    return TestOutputParser().parse(start, output_queue, name)


def auto_fill_queue(module, input_queue, prefix='test_'):
    """
    Scans the specified module for methods beginning with prefix and puts them into the input_queue
    :param module: module whose test methods are to be added to the queue
    :param input_queue: queue to add tests to
    :param prefix: string prefix to identify tests
    :return:
    """
    test_func_names = []
    for x in dir(module):
        if x.startswith(prefix):
            test_func_names.append(x)
    for test_func_name in test_func_names:
        func = getattr(module, test_func_name)
        if callable(func):
            input_queue.put(func)

