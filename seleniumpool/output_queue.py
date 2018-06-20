import multiprocessing_on_dill as multiprocessing
import multiprocessing_on_dill.queues as queues
import sys
import time


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
        entry = OutputEntry(process_ident, time.time(), msg.strip('\n'))
        self.put(entry)
        sys.__stdout__.write('Process {0}: {1}\n'.format(process_ident, msg))

    def flush(self):
        sys.__stdout__.flush()