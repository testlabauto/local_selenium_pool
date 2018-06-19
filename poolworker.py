import multiprocessing_on_dill.queues as queues
from multiprocessing_on_dill.queues import JoinableQueue
import multiprocessing_on_dill as multiprocessing

from queue import Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import json
import traceback
import inspect

class TestCase(object):
    def __init__(self, function, passed, process_id):
        self.function = function
        self.passed = passed
        self.process_id = process_id


    def add_output(self, current_stdout, current_error, current_assertion):
        if current_stdout is not '':
            self.stdout = current_stdout.strip()
        if current_assertion is not '':
            self.assertion = current_assertion.strip()
        if current_error is not '':
            self.error = current_error.strip()


class TestOutputParser(object):
    def parse(self, outstring):
        current_process = None
        current_function = None
        current_pass = False
        current_stdout = ''
        current_assertion = ''
        current_error = ''
        testcases = []
        processing_assert = False
        processing_error = False
        for line in outstring.split('\n'):
            if line.startswith('Process'):
                if current_pass is None and current_function is not None:
                    current_pass = False
                    testcase = TestCase(current_function, current_pass, current_process)
                    testcase.add_output(current_stdout, current_error, current_assertion)
                    testcases.append(testcase)
                current_process = line.split()[1].replace(':', '')
                current_function = None
                current_pass = None
            elif current_process is not None and line.startswith('Starting'):
                if current_pass is None and current_function is not None:
                    current_pass = False
                    testcase = TestCase(current_function, current_pass, current_process)
                    testcase.add_output(current_stdout, current_error, current_assertion)
                    testcases.append(testcase)
                    current_pass = None
                current_function = line.split()[1]
                current_stdout = ''
                current_assertion = ''
                current_error = ''
                processing_assert = False
                processing_error = False
            elif current_process is not None and current_function is not None:
                if line.startswith('Finished'):
                    current_pass = True
                    testcase = TestCase(current_function, current_pass, current_process)
                    testcase.add_output(current_stdout, current_error, current_assertion)
                    testcases.append(testcase)
                    current_function = None
                    current_pass = None
                    current_stdout = ''
                    current_assertion = ''
                    current_error = ''
                else:
                    if '[assertfail]' in line:
                        line = line.replace('[assertfail]', '')
                        processing_assert = True
                        processing_error = False
                        current_assertion += line + '\n'
                    elif '[error]' in line:
                        line = line.replace('[error]', '')
                        processing_assert = False
                        processing_error = True
                        current_error += line + '\n'
                    else:

                        if processing_assert:
                            if '[endassertfail]' in line:
                                processing_assert = False
                                line = line.replace('[endassertfail]', '')
                            current_assertion += line + '\n'
                        elif processing_error:
                            if '[enderror]' in line:
                                processing_error = False
                                line = line.replace('[enderror]', '')
                            current_error += line + '\n'
                        else:
                            current_stdout += line + '\n'

        if current_pass is None and current_function is not None:
            current_pass = False
            testcase = TestCase(current_function, current_pass, current_process)
            testcase.add_output(current_stdout, current_error, current_assertion)
            testcases.append(testcase)

        testcases_json = []
        passed = 0
        failed = 0
        errors = 0
        tests = 0
        for case in testcases:
            tests += 1
            testcases_json.append(case.__dict__)
            if hasattr(case, 'assertion') and case.assertion is not None:
                failed += 1
            elif hasattr(case, 'assertion') and case.error is not None:
                errors += 1
            else:
                passed += 1

        tcs = {'tests': tests,
               'passed': passed,
               'errors': errors,
               'failed': failed,
               'testcase': [testcases_json]}

        return json.dumps(tcs, indent=4)


class StdoutQueue(queues.Queue):
    def __init__(self, *args, **kwargs):
        ctx = multiprocessing.get_context()
        super(StdoutQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self, msg):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe[1][3]
        if msg == '\n':
            return
        process_ident = multiprocessing.current_process().ident
        entry = (process_ident, msg.strip('\n'))
        self.put(entry)
        # sys.__stdout__.write('{0}\n'.format(msg))

    def flush(self):
        sys.__stdout__.flush()


def fixture_decorator(test_function):
    def wrapper(**kwargs):
        oq = kwargs.pop('output_queue')
        sys.stdout = oq
        sys.stderr = oq
        print('Starting {0}'.format(test_function.__name__))
        test_function(**kwargs)
        print('Finished {0}'.format(test_function.__name__))

    return wrapper


class SeleniumWorker(multiprocessing.Process):
    def __init__(self, input_queue, output_queue):
        super(SeleniumWorker, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.driver = None

    def create_driver(self):
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def extract_args(self, job):
        arg_count = len(job)
        if isinstance(job[arg_count - 1], dict):
            kwargs = job[arg_count - 1]
            args = job[1:arg_count - 1]
        else:
            args = job[1:]
            kwargs = {}

        return args, kwargs

    def execute_job(self, func, args, kwargs):
        try:
            self.driver.delete_all_cookies()
            if len(args) > 0 and len(kwargs) > 0:
                func(*args,
                     driver=self.driver,
                     output_queue=self.output_queue,
                     **kwargs)
            elif len(args) > 0 and len(kwargs) == 0:
                func(*args,
                     driver=self.driver,
                     output_queue=self.output_queue)
            elif len(args) == 0 and len(kwargs) > 0:
                func(driver=self.driver,
                     output_queue=self.output_queue,
                     **kwargs)
            elif len(args) == 0 and len(kwargs) == 0:
                func(driver=self.driver,
                     output_queue=self.output_queue)
                # print(self.ident)

        except AssertionError as e:
            x = traceback.format_exc()
            print('[assertfail]{}[endassertfail]'.format(x))
        except Exception as e:
            x = traceback.format_exc()
            print('[error]{}[enderror]'.format(x))
        finally:
            self.input_queue.task_done()

    def run(self):

        self.create_driver()

        while True:
            try:
                job = self.input_queue.get_nowait()
            except Empty:
                self.driver.quit()
                return
            if not callable(job):
                func = job[0]
                args, kwargs = self.extract_args(job)
            else:
                func = job
                args = []
                kwargs = {}
            self.execute_job(func, args, kwargs)


def create_pool(worker_count=multiprocessing.cpu_count()):
    output_queue = StdoutQueue()
    ctx = multiprocessing.get_context()
    input_queue = JoinableQueue(ctx=ctx)

    workers = []
    for i in range(worker_count):
        workers.append(SeleniumWorker(input_queue, output_queue).start())

    return input_queue, output_queue


def wait_for_pool_completion(input_queue):
    input_queue.join()

    print('done')
