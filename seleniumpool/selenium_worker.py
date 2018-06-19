import multiprocessing_on_dill as multiprocessing
from queue import Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback

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
                func(*args,
                     driver=self.driver,
                     output_queue=self.output_queue,
                     **kwargs)
            elif len(args) > 0 and len(kwargs) == 0:
                func(*args,
                     driver=self.driver,
                     output_queue=self.output_queue)
            elif len(args) == 0 and len(kwargs) > 0:
                func(driver=self.driver,
                     output_queue=self.output_queue,
                     **kwargs)
            elif len(args) == 0 and len(kwargs) == 0:
                func(driver=self.driver,
                     output_queue=self.output_queue)
                # print(self.ident)

        except AssertionError as e:
            x = traceback.format_exc()
            print('[assertfail]{}[endassertfail]'.format(x))
        except Exception as e:
            x = traceback.format_exc()
            print('[error]{}[enderror]'.format(x))
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
