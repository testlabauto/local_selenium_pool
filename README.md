# pyloselpo (Python local Selenium pool)

This documentation is in progress.

A local selenium pool for increased testing performance without requiring multiple hosts.    multiprocessing-on-dill is used to provide a configurable number of Chrome webdriver instances on which to simultaneously run selenium tests.   Each instance reuses its _applicationCacheEnabled = False_ webdriver for multiple tests, erasing all cookies between tests.

This project includes a sample test that depends an awesome free resource called [automationpractice.com](http://automationpractice.com/index.php) which is a full featured web store sandbox.  Much thanks to [StMarco89](https://github.com/StMarco89/automationpractice.com)!  

The sample test [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py), has nine tests in it which each take , which can be executed with any number of processes reading from the same queue of tests.  Each test searches the site's products for a different keyword.  It then adds each item found to the cart, one at a time.  Finally, it goes to the checkout page and compares the expected total to the basket total.

After the pool of webdrivers has no remaining tests to execute, it creates a JSON report in an XUnit style.  Stdout is stored as a list, while assertions and errors are stored as strings to preserve formatting.


<details>
  <summary>Click to expand sample output</summary>
  <p>
<!-- the above p cannot start right at the beginning of the line and is mandatory for everything else to work -->

```python
{
    "tests": 9,
    "passed": 7,
    "errors": 1,
    "failed": 1,
    "testcase": [
        [
            {
                "function": "test_url3",
                "process_id": 36593,
                "stdout": [
                    "Starting test_url3",
                    "blouse 1",
                    "blouse $29.00",
                    "Finished test_url3"
                ],
                "passed": true
            },
            {
                "function": "test_url8",
                "process_id": 36593,
                "stdout": [
                    "Starting test_url8",
                    "straps 2",
                    "straps $47.38",
                    "Finished test_url8"
                ],
                "passed": true
            },
            {
                "function": "test_url1",
                "process_id": 36594,
                "stdout": [
                    "Starting test_url1",
                    "dress 7",
                    "Finished test_url1"
                ],
                "passed": false,
                "assertion": "msg 1\nTraceback (most recent call last):\n  File \"/Users/cmead/local_selenium_pool/pyloselpo/selenium_worker.py\", line 58, in execute_job\n    output_queue=self.stdout_queue)\n  File \"/Users/cmead/local_selenium_pool/pyloselpo/decorator.py\", line 18, in decorated_function\n    f(*y, **z)\n  File \"/Users/cmead/local_selenium_pool/test_pool.py\", line 84, in test_url1\n    assert n == 6, \"msg 1\" # wrong on purpose\nAssertionError: msg 1\n"
            },
            {
                "function": "test_url4",
                "process_id": 36596,
                "stdout": [
                    "Starting test_url4",
                    "printed 5",
                    "printed $154.87",
                    "Finished test_url4"
                ],
                "passed": true
            },
            {
                "function": "test_url5",
                "process_id": 36597,
                "stdout": [
                    "Starting test_url5",
                    "summer 4",
                    "summer $94.39",
                    "Finished test_url5"
                ],
                "passed": true
            },
            {
                "function": "test_url2",
                "process_id": 36595,
                "stdout": [
                    "Starting test_url2",
                    "chiffon 2",
                    "chiffon $48.90",
                    "Finished test_url2"
                ],
                "passed": true
            },
            {
                "function": "test_url9",
                "process_id": 36595,
                "stdout": [
                    "Starting test_url9",
                    "evening 1",
                    "evening $52.99",
                    "Finished test_url9"
                ],
                "passed": true
            },
            {
                "function": "test_url6",
                "process_id": 36600,
                "stdout": [
                    "Starting test_url6",
                    "popular 0",
                    "Finished test_url6"
                ],
                "passed": true
            },
            {
                "function": "test_url7",
                "process_id": 36600,
                "stdout": [
                    "Starting test_url7",
                    "faded 1",
                    "faded $18.51",
                    "Finished test_url7"
                ],
                "passed": false,
                "error": "division by zero\nTraceback (most recent call last):\n  File \"/Users/cmead/local_selenium_pool/pyloselpo/selenium_worker.py\", line 58, in execute_job\n    output_queue=self.stdout_queue)\n  File \"/Users/cmead/local_selenium_pool/pyloselpo/decorator.py\", line 18, in decorated_function\n    f(*y, **z)\n  File \"/Users/cmead/local_selenium_pool/test_pool.py\", line 154, in test_url7\n    print(1/0)\nZeroDivisionError: division by zero\n"
            }
        ]
    ],
    "host": "SomebodysMacmini.somewhere.com",
    "duration": 45.529669761657715,
    "name": "test_pool",
    "time": "2018-06-21 15:09:54"
}
```
</p></details>


### Use of multiprocessing

Multiprocessing is used as instead of multithreading and gevent in order to best isolate each selenium instance in a pool from the other instances.  Multiprocessing on Dill is used for compatibility with attr (avoid pickling errors when using decorators).

## Getting Started

### Prerequisites
This project requires Python 3.6.  

I have only tested this on OS X so far, but welcome feedback from anyone working on Windows.  I plan to test on Windows soon.

### Installing
#### Clone project

1) Create a Python 3.6 virtualenv
2) Clone the project and run pip install -r requirements.txt 

#### pip
1) Create a Python 3.6 virtualenv
2) pip install git+https://github.com/testlabauto/local_selenium_pool.git#egg=local_selenium_pool
3) Create a python file and copy the contents of the file  [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py) into it


## Running the sample test, test_pool.py
* Run the script several times, varying the _processes_ parameter to create_pool().  The default, shown below, is 6.
* Comment out the input_queue.put() lines and uncomment the auto_fill_queue() line.  These are the two alternative ways to add tests to the pool

```
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
```

## The sample test cases

<details>
  <summary>Click to expand sample test case code</summary>
  <p>
<!-- the above p cannot start right at the beginning of the line and is mandatory for everything else to work -->

```python

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
```
</p></details>

## Debugging

If using input_queue.put(), you will need to only add the test case you are debugging to the queue 

If using xxx, he prefix parmeter to auto_fill_queue can be used to 

## Built With

* [selenium](https://pypi.org/project/selenium/) - Python bindings for Selenium
* [Multiprocessing on Dill](https://pypi.org/project/multiprocessing_on_dill/) - A friendly fork of multiprocessing which uses dill instead of pickle
* [attr](https://pypi.org/project/attr/) - Simple decorator to set attributes of target function or class in a DRY way.
* [setuptools](https://pypi.org/project/setuptools/) - Easily download, build, install, upgrade, and uninstall Python packages

## Authors

* **Chris Mead** - *Initial work* - [TestLabAuto](https://github.com/testlabauto)

## License

This project is licensed under the Apache License Version 2.0

