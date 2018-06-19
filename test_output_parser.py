import json

sample_out = '''Process 6480:

Starting get_url
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 76, in execute_job
    func(driver=self.driver, output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 85, in get_url
    n = body(driver, "dress")
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 17, in body
    input_element = driver.find_element_by_name("search_query")
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 489, in find_element_by_name
    return self.find_element(by=By.NAME, value=name)
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 957, in find_element
    'value': value})['value']
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 314, in execute
    self.error_handler.check_response(response)
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"name","selector":"search_query"}
  (Session info: headless chrome=67.0.3396.87)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.11.6 x86_64)
Starting get_url5
summer 4
summer $94.39
Finished get_url5

Process 6477:

Starting get_url4
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 76, in execute_job
    func(driver=self.driver, output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 118, in get_url4
    n = body(driver, "printed")
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 17, in body
    input_element = driver.find_element_by_name("search_query")
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 489, in find_element_by_name
    return self.find_element(by=By.NAME, value=name)
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 957, in find_element
    'value': value})['value']
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 314, in execute
    self.error_handler.check_response(response)
  File "/Users/cmead/local_selenium_pool/venv/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"name","selector":"search_query"}
  (Session info: headless chrome=67.0.3396.87)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.11.6 x86_64)
Starting get_url6
popular 0
Finished get_url6
Starting get_url7
faded 1
faded $18.51
Finished get_url7
Starting get_url9
evening 1
evening $52.99
Finished get_url9

Process 6478:

Starting get_url3
blouse 1
blouse $29.00
Finished get_url3
Starting get_url8
straps 2
straps $47.38
Finished get_url8

Process 6479:

Starting get_url2
Message: 
chiffon 1
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 74, in execute_job
    func(driver=self.driver, output_queue=self.output_queue, **kwargs)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 99, in get_url2
    assert n == 2
AssertionError
35.62986397743225'''

class TestCase(object):
    def __init__(self, function, passed, process_id):
        self.function = function
        self.passed = passed
        self.process_id = process_id
        self.stdout = None
        self.assertion = None
        self.error = None

    def add_output(self, current_stdout, current_error, current_assertion):
        if current_stdout is not '':
            self.stdout = current_stdout
        if current_assertion is not '':
            self.assertion = current_assertion
        if current_error is not '':
            self.error = current_error


class TestOutputParser(object):

    def parse(self, outstring):
        current_process = None
        current_function = None
        current_pass = False
        current_stdout = ''
        current_assertion = ''
        current_error = ''
        testcases = []
        for line in outstring.split('\n'):
            if line.startswith('Process'):
                current_process = line.split()[1].replace(':','')
                current_function = None
                current_pass = None
            elif current_process is not None and line.startswith('Starting'):
                if current_pass is None and current_function is not None:
                    current_pass = False
                    testcase = TestCase(current_function, current_pass, current_process)
                    testcase.add_output(current_stdout, current_error, current_assertion)
                    testcases.append(testcase)
                current_function = line.split()[1]
                current_stdout = ''
                current_assertion = ''
                current_error = ''
            elif current_process is not None and current_function is not None:
                if line.startswith('Finished'):
                    current_pass = True
                    testcase = TestCase(current_function, current_pass, current_process)
                    testcase.add_output(current_stdout, current_error, current_assertion)
                    testcases.append(testcase)
                    current_function = None
                else:
                    if 'AssertionError' in line:
                        current_assertion += line + '\n'
                    elif 'Traceback' in line:
                        current_error += line + '\n'
                    else:
                        current_stdout += line + '\n'

        if current_pass is None:
            current_pass = False
            testcase = TestCase(current_function, current_pass, current_process)
            testcase.add_output(current_stdout, current_error, current_assertion)
            testcases.append(testcase)

        testcases_json = []
        for case in testcases:
            testcases_json.append(case.__dict__)

        tcs = {'testcase': [testcases_json]}

        return json.dumps(tcs, indent=4)


if __name__ == "__main__":
    parser = TestOutputParser()
    parsed = parser.parse(sample_out)
    print(parsed)