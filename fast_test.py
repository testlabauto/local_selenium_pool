from poolworker import create_pool, wait_for_pool_completion
from multiprocessing import JoinableQueue
import sys
import time

from queue import Empty

def get_url(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'http://ogp.me/ns#'
    print('getting url 1 {}'.format(url))
    driver.get(url)


def get_url2(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://www.martijnaslander.nl/xmlrpc.php'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url3(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'http://fonts.googleapis.com/css?family=Lato:300,400,700,300italic,400italic,700italic'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url4(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://www.martijnaslander.nl/a-list-of-urls/'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url5(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://yoast.com/wordpress/plugins/seo/'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url6(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://www.martijnaslander.nl/a-list-of-urls/'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url7(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://www.martijnaslander.nl/a-list-of-urls/'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url8(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://www.facebook.com/martijnaslander'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def get_url9(driver, queue):
    sys.stdout = queue
    sys.stderr = queue
    url = 'https://www.martijnaslander.nl/wp-content/plugins/gravityforms/css/formreset.min.css?ver=2.2.6.5'
    print('getting url 1 {}'.format(url))
    print(driver.get(url))


def queue_get_all(q):
    items = []
    maxItemsToRetreive = 10000
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            items.append(q.get_nowait())
        except Empty:
            break
    return items


if __name__ == "__main__":
    start = time.time()

    input_queue = JoinableQueue()

    output_queue = create_pool(input_queue)

    input_queue.put((get_url))
    input_queue.put((get_url2))
    input_queue.put((get_url3))
    input_queue.put((get_url4))
    input_queue.put((get_url5))
    input_queue.put((get_url6))
    input_queue.put((get_url7))
    input_queue.put((get_url8))
    input_queue.put((get_url9))

    wait_for_pool_completion(input_queue)

    print(output_queue.flush())
    print(queue_get_all(output_queue))

    end = time.time()
    print(end - start)






