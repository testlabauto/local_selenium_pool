import multiprocessing_on_dill as multiprocessing
from multiprocessing_on_dill.queues import JoinableQueue
from seleniumpool.output_parser import TestOutputParser
from seleniumpool.output_queue import StdoutQueue
from seleniumpool.selenium_worker import SeleniumWorker
from queue import Empty
import time


start = None

def create_pool(processes=multiprocessing.cpu_count()):
    global start
    start = time.time()

    output_queue = StdoutQueue()
    ctx = multiprocessing.get_context()
    input_queue = JoinableQueue(ctx=ctx)

    workers = []
    for i in range(processes):
        workers.append(SeleniumWorker(input_queue, output_queue).start())

    return input_queue, output_queue


def wait_for_pool_completion(input_queue):
    input_queue.join()

    print('done')


def queue_get_all(q):
    items = {}
    maxItemsToRetreive = 10000
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            new = q.get_nowait()
            pid = new[0]
            msg = new[1]
            if pid not in items:
                items[pid] = ''
            old = items[pid]
            new = '{0}\n{1}'.format(old, msg)
            items[pid] = new
        except Empty:
            break
    return items


def get_parsed_ouput(output_queue, name=None):
    global start
    output_queue.flush()
    buffer = ''
    for okey, ovalue in queue_get_all(output_queue).items():
        buffer += ('\nProcess {0}:'.format(okey))
        buffer += ovalue

    parser = TestOutputParser()
    parsed = parser.parse(start, buffer, name)

    return parsed