from multiprocessing import Process, cpu_count, get_context
from multiprocessing.queues import Queue
from multiprocessing import current_process
from queue import Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import traceback


class StdoutQueue(Queue):
    def __init__(self, *args, **kwargs):
        ctx = get_context()
        super(StdoutQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self, msg):
        self.put(msg)
        sys.__stdout__.write(msg)

    def flush(self):
        sys.__stdout__.flush()



class SeleniumWorker(Process):

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
                func(driver=self.driver, output_queue=self.output_queue, **kwargs)
            elif len(args) == 0 and len(kwargs) == 0:
                func(driver=self.driver, output_queue=self.output_queue)
            print(self.ident)

        except AssertionError as e:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)  # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            print('An error occurred on line {} in statement {}'.format(line, text))
        except Exception as e:
            print(type(e))
            print(e)
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


def create_pool(input_queue, worker_count=cpu_count()):
    output_queue = StdoutQueue()

    workers = []
    for i in range(worker_count):
        workers.append(SeleniumWorker(input_queue, output_queue).start())

    return output_queue


def wait_for_pool_completion(input_queue):
    input_queue.join()

    print('done')

