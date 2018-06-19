import multiprocessing_on_dill.queues as queues
from multiprocessing_on_dill.queues import JoinableQueue
import multiprocessing_on_dill as multiprocessing

from queue import Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import traceback


class StdoutQueue(queues.Queue):
    def __init__(self, *args, **kwargs):
        ctx = multiprocessing.get_context()
        super(StdoutQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self, msg):
        if msg == '\n':
            return
        process_ident = multiprocessing.current_process().ident
        entry = (process_ident, msg.strip('\n'))
        self.put(entry)
        #sys.__stdout__.write('{0}\n'.format(msg))

    def flush(self):
        sys.__stdout__.flush()


def fixture_decorator(test_function):

    def wrapper(**kwargs):
        q = kwargs.pop('output_queue')
        sys.stdout = q
        sys.stderr = q
        print('Starting {0}'.format(test_function.__name__))
        test_function(**kwargs)
        print('Finished {0}'.format(test_function.__name__))

    return wrapper

class SeleniumWorker(multiprocessing.Process):

    def __init__(self, input_queue, output_queue):
        super(SeleniumWorker, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.driver = None

    def create_driver(self):
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def extract_args(self, job):
        arg_count = len(job)
        if isinstance(job[arg_count - 1], dict):
            kwargs = job[arg_count - 1]
            args = job[1:arg_count - 1]
        else:
            args = job[1:]
            kwargs = {}

        return args, kwargs

    def execute_job(self, func, args, kwargs):
        try:
            self.driver.delete_all_cookies()
            if len(args) > 0 and len(kwargs) > 0:
                func(*args, driver=self.driver, output_queue=self.output_queue, **kwargs)
            elif len(args) > 0 and len(kwargs) == 0:
                func(*args, driver=self.driver, output_queue=self.output_queue)
            elif len(args) == 0 and len(kwargs) > 0:
                func(driver=self.driver, output_queue=self.output_queue, **kwargs)
            elif len(args) == 0 and len(kwargs) == 0:
                func(driver=self.driver, output_queue=self.output_queue)
            #print(self.ident)

        except AssertionError as e:
            print(traceback.format_exc())

        except Exception as e:
            print(traceback.format_exc())
        finally:
            self.input_queue.task_done()

    def run(self):

        self.create_driver()

        while True:
            try:
                job = self.input_queue.get_nowait()
            except Empty:
                self.driver.quit()
                return
            if not callable(job):
                func = job[0]
                args, kwargs = self.extract_args(job)
            else:
                func = job
                args = []
                kwargs = {}
            self.execute_job(func, args, kwargs)


def create_pool(worker_count=multiprocessing.cpu_count()):
    output_queue = StdoutQueue()

    ctx = multiprocessing.get_context()
    input_queue = JoinableQueue(ctx=ctx)

    workers = []
    for i in range(worker_count):
        workers.append(SeleniumWorker(input_queue, output_queue).start())

    return input_queue, output_queue


def wait_for_pool_completion(input_queue):
    input_queue.join()

    print('done')

