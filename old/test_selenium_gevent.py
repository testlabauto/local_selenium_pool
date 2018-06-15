import logging
import sys
import unittest
import gevent
from gevent import queue, monkey
from selenium import webdriver


class Crawler():

    def __init__(self, name, visited):
        self.name = name
        self.visited = visited
        self.browser = webdriver.Chrome()

    def visit(self, url):
        logging.info('job:%s:visit:%s' % (self.name, url))
        self.browser.get(url)
        self.visited.append(url)
        return


def process(name, q, visited):
    crawler = Crawler(name, visited)
    while True:
        try:
            item = q.get(block=True, timeout=5)
        except queue.Empty:
            crawler.browser.quit()
            break
        gevent.sleep(1)
        try:
            crawler.visit(item)
        except Exception:
            logging.warning('job:%s:error:%s' % (crawler.name, item))


class QueueSample(unittest.TestCase):

    def test_queue(self):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        monkey.patch_subprocess()
        q = queue.Queue()
        for i in range(4):
            q.put('http://localhost:8000/')
        visited = list()
        jobs = [gevent.spawn(process, i, q, visited) for i in range(2)]
        gevent.joinall(jobs)
        logging.info('finished')
        return


if __name__ == '__main__':
    unittest.main()
