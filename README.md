# loselpo

A local selenium pool for increased testing performance without requiring multiple hosts.    multiprocessing-on-dill is used to provide a configurable number of headless Chrome selenium webdriver instances on which to simultaneously run selenium tests.   Each instance reuses its _applicationCacheEnabled = False_ webdriver for multiple tests, erasing all cookies between tests.

This project includes a sample test that depends an awesome free resource called [automationpractice.com](http://automationpractice.com/index.php) which is a full featured web store sandbox.  Much thanks to [StMarco89](https://github.com/StMarco89/automationpractice.com)!  

The sample test [test_pool.py](https://github.com/testlabauto/local_selenium_pool/blob/master/test_pool.py), has nine standard looking tests in it, which can be executed with any number of processes reading from the same queue of tests.  Each test searches the site's products for a different keyword.  It then adds each item found to the cart, one at a time.  Finally, it goes to the checkout page and compares the expected total to the basket total.

After the pool of webdrivers has no remaining tests to execute, it creates a JSON report in an XUnit style.  Stdout is stored as a list, while assertions and errors are stored as strings to preserve formatting.   See a portion of a sample output below:
```json
{
    "tests": 9,
    "passed": 7,
    "errors": 1,
    "failed": 1,
    "testcase": [
        [
            {
                "function": "test_url1",
                "process_id": 36178,
                "stdout": [
                    "Starting test_url1",
                    "dress 7",
                    "Finished test_url1"
                ],
                "passed": false,
                "assertion": "msg 1\nTraceback (most recent call last):\n  File \"/Users/cmead/local_selenium_pool/loselpo/selenium_worker.py\", line 58, in execute_job\n    output_queue=self.stdout_queue)\n  File \"/Users/cmead/local_selenium_pool/loselpo/decorator.py\", line 18, in decorated_function\n    f(*y, **z)\n  File \"/Users/cmead/local_selenium_pool/test_pool.py\", line 84, in test_url1\n    assert n == 6, \"msg 1\" # wrong on purpose\nAssertionError: msg 1\n"
            },
            {
                "function": "test_url2",
                "process_id": 36197,
                "stdout": [
                    "Starting test_url2",
                    "chiffon 2",
                    "chiffon $48.90",
                    "Finished test_url2"
                ],
                "passed": true
            },

            ...

            {
                "function": "test_url7",
                "process_id": 36181,
                "stdout": [
                    "Starting test_url7",
                    "faded 1",
                    "faded $18.51",
                    "Finished test_url7"
                ],
                "passed": false,
                "error": "division by zero\nTraceback (most recent call last):\n  File \"/Users/cmead/local_selenium_pool/loselpo/selenium_worker.py\", line 58, in execute_job\n    output_queue=self.stdout_queue)\n  File \"/Users/cmead/local_selenium_pool/loselpo/decorator.py\", line 18, in decorated_function\n    f(*y, **z)\n  File \"/Users/cmead/local_selenium_pool/test_pool.py\", line 154, in test_url7\n    print(1/0)\nZeroDivisionError: division by zero\n"
            }
        ]
    ],
    "host": "sample.domain.com",
    "duration": 35.49641013145447,
    "name": "test_pool",
    "time": "2018-06-21 14:57:22"
}
```

## Getting Started

This project requires Python 3.6.  

### Prerequisites

I have only tested this on OS X so far, but welcome feedback from anyone working on Windows.

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
