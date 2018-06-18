from poolworker import create_pool, wait_for_pool_completion
from multiprocessing import JoinableQueue
import sys

import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


from queue import Empty

def body(driver, queue, subject):
    sys.stdout = queue
    sys.stderr = queue
    driver.get("http://automationpractice.com/")
    input_element = driver.find_element_by_name("search_query")
    input_element.send_keys(subject)
    input_element.submit()

    time.sleep(1)

    image_containers = driver.find_elements_by_class_name('product-image-container')
    images = []
    for container in image_containers:
        images.extend(container.find_elements_by_class_name('replace-2x'))

    counter = 0
    cart_added = 0
    for image in images:


        hover = ActionChains(driver).move_to_element(image)
        hover.perform()

        add_to_cart = 'ajax_add_to_cart_button'

        time.sleep(1)

        add_to_cart = driver.find_elements(By.CLASS_NAME, add_to_cart)[counter]
        counter += 1
        try:
            add_to_cart.click()

            continue_shopping = 'continue'

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, continue_shopping)))

            continue_button = driver.find_element(By.CLASS_NAME, continue_shopping)

            continue_button.click()
            cart_added += 1
        except Exception as e:
            print(e)

    return cart_added




def get_url(driver, queue):
    n = body(driver, queue, "dress")
    print('dress {}'.format(n))
    assert n == 7


def get_url2(driver, queue):
    n = body(driver, queue, "chiffon")
    print('chiffon {}'.format(n))
    assert n == 2


def get_url3(driver, queue):
    n = body(driver, queue, "blouse")
    print('blouse {}'.format(n))
    assert n == 1


def get_url4(driver, queue):
    n = body(driver, queue, "printed")
    print('printed {}'.format(n))
    assert n == 5


def get_url5(driver, queue):
    n = body(driver, queue, "summer")
    print('summer {}'.format(n))
    assert n == 4


def get_url6(driver, queue):
    n = body(driver, queue, "popular")
    print('popular {}'.format(n))
    assert n == 0


def get_url7(driver, queue):
    n = body(driver, queue, "faded")
    print('faded {}'.format(n))
    assert n == 1


def get_url8(driver, queue):
    n = body(driver, queue, "straps")
    print('straps {}'.format(n))


def get_url9(driver, queue):
    n = body(driver, queue, "evening")
    print('evening {}'.format(n))


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

    output_queue = create_pool(input_queue, 1)

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






