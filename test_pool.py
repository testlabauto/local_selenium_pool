import os
from pyloselpo.pool import create_pool, wait_for_pool_completion, auto_fill_queue
from pyloselpo.decorator import sel_pool
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def body(driver, subject):
    driver.get("http://automationpractice.com/")
    time.sleep(1)
    input_element = driver.find_element_by_name("search_query")
    input_element.send_keys(subject)
    input_element.submit()

    pic = 'product-image-container'
    time.sleep(2)

    image_containers = driver.find_elements_by_class_name(pic)
    images = []
    for container in image_containers:
        images.extend(container.find_elements_by_class_name('replace-2x'))

    counter = 0
    cart_added = 0
    for image in images:

        hover = ActionChains(driver).move_to_element(image)
        hover.perform()

        add_to_cart = 'ajax_add_to_cart_button'
        time.sleep(2)

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


def body2(driver):
    cart_block = driver.find_elements_by_xpath('//*[@title="View my shopping cart"]')[0]

    hover = ActionChains(driver).move_to_element(cart_block)
    hover.perform()

    boc = 'button_order_cart'
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, boc)))

    button_order_cart = driver.find_element(By.ID, boc)
    button_order_cart.click()

    total = 'total_price'
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, total)))

    price = driver.find_element(By.ID, total)
    return price.text


@sel_pool()
def test_url1(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "dress")
    print('dress {}'.format(n))
    #assert n == 7
    assert n == 6, "msg 1" # wrong on purpose
    m = body2(driver)
    print('dress {}'.format(m))
    #assert '$198.38' == m
    assert '$197.38' == m, 'found {}'.format(m) # wrong on purpose


@sel_pool()
def test_url2(**kwargs):
    assert kwargs.pop('test') == 2
    driver = kwargs.pop('driver')
    n = body(driver, "chiffon")
    print('chiffon {}'.format(n))
    assert n == 2
    m = body2(driver)
    print('chiffon {}'.format(m))
    assert '$48.90' == m, 'found {}'.format(m)



@sel_pool()
def test_url3(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "blouse")
    print('blouse {}'.format(n))
    assert n == 1
    m = body2(driver)
    print('blouse {}'.format(m))
    assert '$29.00' == m, 'found {}'.format(m)


@sel_pool()
def test_url4(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "printed")
    print('printed {}'.format(n))
    assert n == 5
    m = body2(driver)
    print('printed {}'.format(m))
    assert '$154.87' == m, 'found {}'.format(m)


@sel_pool()
def test_url5(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "summer")
    print('summer {}'.format(n))
    assert n == 4
    m = body2(driver)
    print('summer {}'.format(m))
    assert '$94.39' == m, 'found {}'.format(m)


@sel_pool()
def test_url6(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "popular")
    print('popular {}'.format(n))
    assert n == 0


@sel_pool()
def test_url7(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "faded")
    print('faded {}'.format(n))
    assert n == 1
    m = body2(driver)
    print('faded {}'.format(m))
    assert '$18.51' == m, 'found {}'.format(m)
    print(1/0)


@sel_pool()
def test_url8(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver,  "straps")
    print('straps {}'.format(n))
    m = body2(driver)
    assert n == 2
    print('straps {}'.format(m))
    assert '$47.38' == m, 'found {}'.format(m)


@sel_pool()
def test_url9(**kwargs):
    driver = kwargs.pop('driver')
    n = body(driver, "evening")
    print('evening {}'.format(n))
    assert n == 1
    m = body2(driver)
    print('evening {}'.format(m))
    assert '$52.99' == m, 'found {}'.format(m)


if __name__ == "__main__":

    start = time.time()

    chrome_options = Options()
    chrome_options.add_argument("--headless")


    input_queue, output_queue = create_pool(os.path.splitext(os.path.basename(__file__))[0],
                                            chrome_options,
                                            processes=6)


    #auto_fill_queue(sys.modules[__name__], input_queue, 'test_')

    input_queue.put((test_url1))
    input_queue.put((test_url2, {'test': 2}))
    input_queue.put((test_url3))
    input_queue.put((test_url4,))
    input_queue.put((test_url5))
    input_queue.put((test_url6))
    input_queue.put((test_url7))
    input_queue.put((test_url8))
    input_queue.put((test_url9))

    report = wait_for_pool_completion(input_queue)

    print(report)






