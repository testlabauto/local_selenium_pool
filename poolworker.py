from multiprocessing import Process, Pool, cpu_count
from queue import Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumWorker(Process):

    def __init__(self, queue):
        super(SeleniumWorker, self).__init__()
        self.queue = queue
        #self.daemon = True
        self.driver = None
        self.results = None

    def create_driver(self):
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def stop_driver(self):
        self.driver.quit()

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
            if len(args) > 0 and len(kwargs) > 0:
                func(self.driver, self.results, *args, **kwargs)
            elif len(args) > 0 and len(kwargs) == 0:
                func(self.driver, self.results, *args)
            elif len(args) == 0 and len(kwargs) == 0:
                func(self.driver, self.results)
            print(self.ident)
        except Exception as e:
            print(e)
        finally:
            self.queue.task_done()

    def run(self):

        self.create_driver()

        while True:
            try:
                job = self.queue.get(timeout=5)
            except Empty:
                self.driver.quit()
                return
            func = job[0]
            args, kwargs = self.extract_args(job)
            self.execute_job(func, args, kwargs)

    def terminate(self):
        self.driver.quit()
        return super(SeleniumWorker, self).terminate()


def create_pool(queue):

    workers = []
    for i in range(cpu_count()):
        workers.append(SeleniumWorker(queue).start())

    pool = Pool()

    return pool


