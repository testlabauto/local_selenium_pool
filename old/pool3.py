import sys
IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue

import csv
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        print('new driver')
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(self.driver, *args, **kwargs)
                print(self.ident)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        self.workers = []
        for _ in range(num_threads):
            self.workers.append(Worker(self.tasks))

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()
        for worker in self.workers:
            worker.driver.quit()


def get_url(driver, url):

    print('getting url {}'.format(url))
    driver.get(url)

    #print(driver.page_source)


if __name__ == "__main__":
    with open('misc.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    urls = [x[0] for x in your_list]
    pool = ThreadPool(5)
    pool.map(get_url, urls)
    pool.wait_completion()

