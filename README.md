# pyloselpo (Python local Selenium pool)

A local selenium pool for increased testing performance without requiring multiple hosts.    multiprocessing-on-dill is used to provide a configurable number of Chrome webdriver instances on which to simultaneously run selenium tests.   Each instance reuses its _applicationCacheEnabled = False_ webdriver for multiple tests, erasing all cookies between tests.

This project includes a sample test that depends an awesome free resource called [automationpractice.com](http://automationpractice.com/index.php) which is a full featured web store sandbox.  Much thanks to [StMarco89](https://github.com/StMarco89/automationpractice.com)!  

The sample test [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py), has nine tests in it which each take , which can be executed with any number of processes reading from the same queue of tests.  Each test searches the site's products for a different keyword.  It then adds each item found to the cart, one at a time.  Finally, it goes to the checkout page and compares the expected total to the basket total.

After the pool of webdrivers has no remaining tests to execute, it creates a JSON report in an XUnit style.  Stdout is stored as a list, while assertions and errors are stored as strings to preserve formatting.


<details>
  <summary>Click to expand sample output</summary>
  <p>
<!-- the above p cannot start right at the beginning of the line and is mandatory for everything else to work -->

```java
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


## Getting Started

This project requires Python 3.6.  

### Prerequisites

I have only tested this on OS X so far, but welcome feedback from anyone working on Windows.  I plan to test on Windows soon.

### Installing

* Create a Python 3.6 virtualenv
* pip install git+https://github.com/testlabauto/local_selenium_pool.git#egg=local_selenium_pool
* Create a python file and copy the contents of the file  [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py) into it


## Running the sample test, test_pool.py
* Run the script several times, varying the _processes_ parameter to create_pool().  The default, shown below, is 6.

```
input_queue, output_queue = create_pool(os.path.splitext(os.path.basename(__file__))[0],
                                            chrome_options,
                                            processes=6)
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
