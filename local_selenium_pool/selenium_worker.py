import multiprocessing_on_dill as multiprocessing
from queue import Empty
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import traceback
import sys


class SeleniumWorker(multiprocessing.Process):
    """
    This subclass of Process excecutes tests and hold on to driver that it reuses
    """
    def __init__(self, input_queue, output_queue, chrome_options):
        super(SeleniumWorker, self).__init__()
        self.input_queue = input_queue
        self.stdout_queue = output_queue.getStdOutQueue()
        self.error_queue = output_queue.getErrorQueue()
        self.assertion_queue = output_queue.getAssertionQueue()
        self.output_queue = output_queue
        self.driver = None
        self.chrome_options = chrome_options

    def create_driver(self):
        """
        Create the driver that this worker will use with the options passed in
        :return:
        """
        if self.driver is None:
            cap = DesiredCapabilities.CHROME
            cap.update({'applicationCacheEnabled': False})
            self.driver = webdriver.Chrome(desired_capabilities=cap,
                                           chrome_options=self.chrome_options)

    def extract_args(self, job):
        """
        Helper function to extract the arguments from a job popped from the input_queue
        :param job: test method and params, if any
        :return: kwargs
        """
        arg_count = len(job)
        if isinstance(job[arg_count - 1], dict):
            kwargs = job[arg_count - 1]
        else:
            kwargs = {}

        return kwargs

    def run(self):
        """
        Called when process is started.  Begins by creating a driver for this worker.  The time it takes to
        create the driver allows for follow on addition of tests to the queue.  Loops as long as the queue is
        not empty, running tests
        :return:
        """

        self.create_driver()

        while True:
            try:
                job = self.input_queue.get_nowait()
            except Empty:
                self.driver.quit()
                return
            if not callable(job):
                func = job[0]
                kwargs = self.extract_args(job)
            else:
                func = job
                kwargs = {}
            self.execute_job(func, kwargs)

    def execute_job(self, func, kwargs):
        """
        Called by run() to execute a single test.  Deletes all cookies between tests.
        Adds the driver and output_queue to the test case via kwargs (merges kwargs if kwargs supplied by test case)
        When an exception or assertion is hit, stdout/stderr redirected to appropriate queue
        and then stdout/stderr restored.  Logging of "Finished" is not optional as it is used by the results parser
        Mraks tests as done in the queue when complete.
        :param func: name of function to run
        :param kwargs: kwargs passed from the user
        :return:
        """
        try:
            self.driver.delete_all_cookies()

            if len(kwargs) > 0:
                func(driver=self.driver,
                     output_queue=self.stdout_queue,
                     **kwargs)
            elif len(kwargs) == 0:
                func(driver=self.driver,
                     output_queue=self.stdout_queue)
        except AssertionError as e:
            x = traceback.format_exc()
            print('Finished {}'.format(func.__name__))
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = self.assertion_queue
            sys.stderr = self.assertion_queue
            print('[{}]\n{}\n{}'.format(func.__name__, str(e), x))
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        except Exception as e:
            x = traceback.format_exc()
            print('Finished {}'.format(func.__name__))
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = self.error_queue
            sys.stderr = self.error_queue
            print('[{}]\n{}\n{}'.format(func.__name__, str(e), x))
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        finally:
            self.input_queue.task_done()

