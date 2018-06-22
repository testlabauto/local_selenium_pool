import multiprocessing_on_dill as multiprocessing
import multiprocessing_on_dill.queues as queues
from queue import Empty
import sys
import datetime



class TestRunOutput():
    def __init__(self):
        self.stdout = OutputQueue()
        self.error = OutputQueue()
        self.assertion = OutputQueue()

    def getStdOutQueue(self):
        return self.stdout

    def getErrorQueue(self):
        return self.error

    def getAssertionQueue(self):
        return self.assertion

    def getQueues(self):
        return self.stdout, self.error, self.assertion


class OutputEntry():
    def __init__(self, pid, timestamp, msg):
        self.pid = pid
        self.timestamp = timestamp
        self.msg = msg


class OutputQueue(queues.Queue):
    def __init__(self, *args, **kwargs):
        ctx = multiprocessing.get_context()
        super(OutputQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self, msg):
        if msg == '\n':
            return
        process_ident = multiprocessing.current_process().ident
        entry = OutputEntry(process_ident, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg.strip('\n'))
        self.put(entry)
        sys.__stdout__.write('Process {0}: {1}\n'.format(process_ident, msg))

    def flush(self):
        sys.__stdout__.flush()


def queue_get_all(q):
    items = {}
    maxItemsToRetreive = 10000
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            new = q.get_nowait()
            pid = new.pid
            ts = new.timestamp
            msg = new.msg
            if pid not in items:
                items[pid] = ''
            old = items[pid]
            new = '{0}\n[{1}]{2}'.format(old, ts, msg)
            items[pid] = new
        except Empty:
            break
    return items
