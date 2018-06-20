import multiprocessing_on_dill as multiprocessing
import multiprocessing_on_dill.queues as queues
import sys


class OutputQueue(queues.Queue):
    def __init__(self, *args, **kwargs):
        ctx = multiprocessing.get_context()
        super(OutputQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self, msg):
        if msg == '\n':
            return
        process_ident = multiprocessing.current_process().ident
        entry = (process_ident, msg.strip('\n'))
        self.put(entry)
        sys.__stdout__.write('Process {0}: {1}\n'.format(process_ident, msg.
                                            replace('[assertfail]','').
                                            replace('[error]', '').
                                            replace('[endassertfail]','').
                                            replace('[enderror]', '')))

    def flush(self):
        sys.__stdout__.flush()