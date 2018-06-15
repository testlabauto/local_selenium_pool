from multiprocessing import Process, Pool, JoinableQueue, cpu_count

import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Worker(Process):

    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.daemon = True
        self.driver = None
        self.results = None

    def create_driver(self):
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def stop_driver(self):
        self.driver.quit()

    def run(self):

        self.create_driver()

        while True:

            items = self.queue.get()
            func = items[0]

            arg_count = len(items)
            if isinstance(items[arg_count - 1], dict):
                kwargs = items[arg_count - 1]
                args = items[1:arg_count - 1]
            else:
                args = items[1:]
                kwargs = {}

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

# can use this:
#    def get_url(driver, url, *args, **kwargs):
# or:
#    def get_url(driver, url):
# or:
#    def get_url(driver, url, a, b, **kwargs):
# or:
#     def get_url(driver, url, *args):

def get_url(driver, results, url, *args, **kwargs):


    print('getting url {}'.format(url))
    driver.get(url)

def get_data():
    with open('misc.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    urls = [x[0] for x in your_list]
    return urls

if __name__ == "__main__":
    urls = get_data()

    url_queue = JoinableQueue()
    workers=[]
    for i in range(cpu_count()):
        workers.append(Worker(url_queue).start())

    pool = Pool()

    for url in urls:
        url_queue.put((get_url, url))

    print('done putting')

    url_queue.join()




