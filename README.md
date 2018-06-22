# pyloselpo (Python local Selenium pool)



A local selenium pool for increased testing performance without requiring multiple hosts.    multiprocessing-on-dill is used to provide a configurable number of Chrome webdriver instances on which to simultaneously run selenium tests.   Each instance reuses its _applicationCacheEnabled = False_ webdriver for multiple tests, erasing all cookies between tests.

This project includes a sample test that depends an awesome free resource called [automationpractice.com](http://automationpractice.com/index.php) which is a full featured web store sandbox.  Much thanks to [StMarco89](https://github.com/StMarco89/automationpractice.com)!  

The sample test [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py), has nine tests in it which can be executed using any number of processes reading from the same queue of tests.  Each test searches the site's products for a different keyword.  It then adds each item found to the cart, one at a time.  Finally, it goes to the checkout page and compares the expected total to the basket total.

![Performance Gain](https://github.com/testlabauto/local_selenium_pool/blob/master/images/pyloselpo_perf.png)

After the pool of webdrivers has no remaining tests to execute, it creates a JSON report in an XUnit style. 

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
                "function": "test_url1",
                "process_id": 47455,
                "stdout": "[2018-06-22 13:03:41] Starting test_url1\n[2018-06-22 13:04:17] dress 7\n[2018-06-22 13:04:17] Finished test_url1",
                "passed": false,
                "time": "2018-06-22 13:03:41",
                "duration": "36.0",
                "assertion": "[2018-06-22 13:04:17] msg 1\n[2018-06-22 13:04:17] Traceback (most recent call last):\n[2018-06-22 13:04:17]   File \"/Users/cmead/local_selenium_pool/pyloselpo/selenium_worker.py\", line 92, in execute_job\n[2018-06-22 13:04:17]     output_queue=self.stdout_queue)\n[2018-06-22 13:04:17]   File \"/Users/cmead/local_selenium_pool/pyloselpo/decorator.py\", line 26, in decorated_function\n[2018-06-22 13:04:17]     f(**merged)\n[2018-06-22 13:04:17]   File \"/Users/cmead/local_selenium_pool/test_pool.py\", line 85, in test_url1\n[2018-06-22 13:04:17]     assert n == 6, \"msg 1\" # wrong on purpose\n[2018-06-22 13:04:17] AssertionError: msg 1\n"
            },
            {
                "function": "test_url3",
                "process_id": 47454,
                "stdout": "[2018-06-22 13:03:41] Starting test_url3\n[2018-06-22 13:03:59] blouse 1\n[2018-06-22 13:04:01] blouse $29.00\n[2018-06-22 13:04:01] Finished test_url3",
                "passed": true,
                "time": "2018-06-22 13:03:41",
                "duration": "20.0"
            },
            {
                "function": "test_url8",
                "process_id": 47454,
                "stdout": "[2018-06-22 13:04:01] Starting test_url8\n[2018-06-22 13:04:17] straps 2\n[2018-06-22 13:04:20] straps $47.38\n[2018-06-22 13:04:20] Finished test_url8",
                "passed": true,
                "time": "2018-06-22 13:04:01",
                "duration": "19.0"
            },
            {
                "function": "test_url6",
                "process_id": 47452,
                "stdout": "[2018-06-22 13:03:41] Starting test_url6\n[2018-06-22 13:03:56] popular 0\n[2018-06-22 13:03:56] Finished test_url6",
                "passed": true,
                "time": "2018-06-22 13:03:41",
                "duration": "15.0"
            },
            {
                "function": "test_url7",
                "process_id": 47452,
                "stdout": "[2018-06-22 13:03:56] Starting test_url7\n[2018-06-22 13:04:09] faded 1\n[2018-06-22 13:04:11] faded $18.51\n[2018-06-22 13:04:11] Finished test_url7",
                "passed": false,
                "time": "2018-06-22 13:03:56",
                "duration": "15.0",
                "error": "[2018-06-22 13:04:11] division by zero\n[2018-06-22 13:04:11] Traceback (most recent call last):\n[2018-06-22 13:04:11]   File \"/Users/cmead/local_selenium_pool/pyloselpo/selenium_worker.py\", line 92, in execute_job\n[2018-06-22 13:04:11]     output_queue=self.stdout_queue)\n[2018-06-22 13:04:11]   File \"/Users/cmead/local_selenium_pool/pyloselpo/decorator.py\", line 26, in decorated_function\n[2018-06-22 13:04:11]     f(**merged)\n[2018-06-22 13:04:11]   File \"/Users/cmead/local_selenium_pool/test_pool.py\", line 154, in test_url7\n[2018-06-22 13:04:11]     print(1/0)\n[2018-06-22 13:04:11] ZeroDivisionError: division by zero\n"
            },
            {
                "function": "test_url2(test=2)",
                "process_id": 47461,
                "stdout": "[2018-06-22 13:03:41] Starting test_url2(test=2)\n[2018-06-22 13:04:05] chiffon 2\n[2018-06-22 13:04:07] chiffon $48.90\n[2018-06-22 13:04:07] Finished test_url2",
                "passed": true,
                "time": "2018-06-22 13:03:41",
                "duration": "26.0"
            },
            {
                "function": "test_url9",
                "process_id": 47461,
                "stdout": "[2018-06-22 13:04:07] Starting test_url9\n[2018-06-22 13:04:17] evening 1\n[2018-06-22 13:04:20] evening $52.99\n[2018-06-22 13:04:20] Finished test_url9",
                "passed": true,
                "time": "2018-06-22 13:04:07",
                "duration": "13.0"
            },
            {
                "function": "test_url4",
                "process_id": 47453,
                "stdout": "[2018-06-22 13:03:42] Starting test_url4\n[2018-06-22 13:04:15] printed 5\n[2018-06-22 13:04:18] printed $154.87\n[2018-06-22 13:04:18] Finished test_url4",
                "passed": true,
                "time": "2018-06-22 13:03:42",
                "duration": "36.0"
            },
            {
                "function": "test_url5",
                "process_id": 47459,
                "stdout": "[2018-06-22 13:03:42] Starting test_url5\n[2018-06-22 13:04:13] summer 4\n[2018-06-22 13:04:15] summer $94.39\n[2018-06-22 13:04:15] Finished test_url5",
                "passed": true,
                "time": "2018-06-22 13:03:42",
                "duration": "33.0"
            }
        ]
    ],
    "host": "ChristophersMacmini.longmontcolorado.gov",
    "duration": 41.14260005950928,
    "name": "test_pool",
    "time": "2018-06-22 13:04:20"
}
```
</p></details>


## Multiprocessing on Dill

Multiprocessing is used instead of multithreading or gevent in order to best isolate each selenium instance in a pool from the other instances.  Multiprocessing on Dill is used for compatibility with attr (to avoid pickling errors when using decorators).

## Input and Output Queues

The Selenium executor processes share the same input and outputs.  On the input side, they get test cases from a JoinableQueue and exit when that queue is empty.  On the output side, they print() output and log exceptions and assertions to queues to avoid sharing resources.  When the input queue is empty and all the processes exit their main loop, the data from the queues is processed into a readable report.

![Overview](https://github.com/testlabauto/local_selenium_pool/blob/master/images/pyloselpo.png)

## Decorators
Decorators are required on test cases.  The _@sel_pool()_ decorator allows for stdout/stderr redirection and for the appropriate web driver to be provided to the test.  Additionally, test cases can be data driven using the decorator's parameter, **kwargs.

When adding tests to the queue with auto_fill_queue(), the decorator can be parameterized like this:  

    @sel_pool(**{'test': 2, 'test2': 5.6})

When adding tests to the queue with a put() to the JoinableQueue, parameters can be provided like this: 

    input_queue.put((test_url2, {'test': 2}))

## Getting Started

### Prerequisites
This project requires Python 3.6.  

I have only tested this on OS X so far, but welcome feedback from anyone working on Windows.  I plan to test on Windows soon.

### Installing
#### Clone project

1) Create a Python 3.6 virtualenv
2) Clone the project and run pip install -r requirements.txt 
3) Download chromedriver and put it in your PATH

#### pip
1) Create a Python 3.6 virtualenv
2) pip install git+https://github.com/testlabauto/local_selenium_pool.git#egg=local_selenium_pool
3) Create a python file and copy the contents of the file  [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py) into it
3) Download chromedriver and put it in your PATH


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

## Test Cases

There are two requirements for testcases:
* Use the **kwargs argument (you will access the driver and your own parameters via kwargs)
* Use the @sel_pool() decorator (parameters optional)
```python
@sel_pool(**{'test': 2})
def test_something(**kwargs):
    assert kwargs.pop('test') == 2
```

<details>
  <summary>Click to see more sample test case code</summary>
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

When using input_queue.put(), to run a specific test that you need to debug, you simply need to only add only that test case to the queue.

When using auto_fill_queue(), to run a specific test that you need to debug, use the prefix parameter to auto_fill_queue to match a method whose name you've altered.  
## Built With

* [selenium](https://pypi.org/project/selenium/) - Python bindings for Selenium
* [Multiprocessing on Dill](https://pypi.org/project/multiprocessing_on_dill/) - A friendly fork of multiprocessing which uses dill instead of pickle
* [attr](https://pypi.org/project/attr/) - Simple decorator to set attributes of target function or class in a DRY way.
* [setuptools](https://pypi.org/project/setuptools/) - Easily download, build, install, upgrade, and uninstall Python packages


## Authors

* **Chris Mead** - *Initial work* - [TestLabAuto](https://github.com/testlabauto) - [Test Lab Automation](https://testlabauto.com/)


## License

This project is licensed under the Apache License Version 2.0

