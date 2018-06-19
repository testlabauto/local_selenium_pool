sample_out = '''Process 5667:

Starting get_url3
Message: 
blouse 0
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 74, in execute_job
    func(driver=self.driver, output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 109, in get_url3
    assert n == 1
AssertionError

Process 5669:

Starting get_url
Message: 
Message: element not visible
  (Session info: headless chrome=67.0.3396.87)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.11.6 x86_64)
Message: element not visible
  (Session info: headless chrome=67.0.3396.87)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.11.6 x86_64)
Message: element not visible
  (Session info: headless chrome=67.0.3396.87)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.11.6 x86_64)
dress 3
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 74, in execute_job
    func(driver=self.driver, output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 88, in get_url
    assert n == 6, "msg 1"
AssertionError: msg 1

Process 5666:

Starting get_url4
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 74, in execute_job
    func(driver=self.driver, output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 117, in get_url4
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
Starting get_url8
straps 2
straps $47.38
Finished get_url8

Process 5668:

Starting get_url5
Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 74, in execute_job
    func(driver=self.driver, output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 36, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 127, in get_url5
    n = body(driver, "summer")
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
Starting get_url7
faded 1
faded $18.51
Finished get_url7
Starting get_url9
evening 1
evening $52.99
Finished get_url9
45.858981132507324'''

class TestOutputParser(object):


    def parse(self, outstring):
        current_process = None
        current_function = None
        current_pass = False
        current_body = ''
        for line in outstring.split('\n'):
            #print(line)
            if line.startswith('Process'):
                current_process = line.split()[1].replace(':','')
                continue
            elif current_process is not None and line.startswith('Starting'):
                current_function = line.split()[1]
                current_body = ''

                #print(current_function)
            elif current_process is not None and current_function is not None:
                if line.startswith('Finished'):
                    current_pass = True
                    current_function = None
                else:
                    current_body += line
                    continue

            if current_process is not None and current_function is not None:
                print('{} {} {}'.format(current_process, current_function, current_pass))








if __name__ == "__main__":
    parser = TestOutputParser()
    parsed = parser.parse(sample_out)