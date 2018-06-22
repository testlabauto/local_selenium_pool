import datetime
import json
from local_selenium_pool.output_queue import queue_get_all
from local_selenium_pool.test_case import TestCase
import socket
import time


class TestOutputParser(object):
    """
    This class creates a JSON report using the data stored in the three output queues during a tets run
    """

    def parse(self, start, output_queue, name):
        """
        Parse creates the report and returns it as JSON
        :param start: Timestamp of when the test was started
        :param output_queue: object that holds references to all three output queues
        :param name: name of the output report (test module name is recommended)
        :return: json formatted report in XUnit style
        """
        testcases = self.build_base_report(output_queue)

        self.process_stderr_component('error', output_queue.getErrorQueue(), testcases)
        self.process_stderr_component('assertion', output_queue.getAssertionQueue(), testcases)

        suite = self.create_json_report(testcases, start, name)

        return json.dumps(suite, indent=4)

    @staticmethod
    def build_base_report(output_queue):
        """
        Each test case run will have stdout, but not each one will have errors and assertions.
        The base report consists of test cases an d their stdout
        :param output_queue:
        :return: list of testcases
        """
        stdout = queue_get_all(output_queue.getStdOutQueue())
        runs = []
        lines = []
        for key, value in stdout.items():
            pid = key
            for line in value.split('\n'):
                parts = line.split(']')
                ts = parts[0][1:]
                msg = ']'.join(parts[1:])
                if msg is not '':
                    lines.append((ts, msg))
                if msg.startswith('Starting '):
                    func_name = parts[1].split()[1]
                if msg.startswith('Finished'):
                    runs.append((pid, func_name, lines))
                    lines = []

        testcases = {}
        for run in runs:
            standard_out = '\n'.join(['[{}] {}'.format(x[0], x[1]) for x in run[2]])
            first_ts = run[2][0][0]
            last_ts = run[2][-1][0]
            fs = "%Y-%m-%d %H:%M:%S"
            first_ts_time = time.strptime(first_ts, fs)
            last_ts_time = time.strptime(last_ts, fs)

            duration = str(time.mktime(last_ts_time) - time.mktime(first_ts_time))

            tc = TestCase(function=run[1], process_id=run[0], stdout=standard_out, time=first_ts,
                          duration=duration)
            testcases['{}-{}'.format(run[0], run[1])] = tc

        return testcases

    def process_stderr_component(self, stderr_type, queue, testcases):
        """
        This method is called to add exceptions and assertions to the base report
        :param stderr_type: flag used to determine which attribute on test case to add to
        :param queue: error or assertion queue
        :param testcases: base report
        :return:
        """
        items = queue_get_all(queue)
        lines = ''
        func_name = ''
        current_ts = ''
        for key, value in items.items():
            pid = key
            for line in value.split('\n'):
                if line == '':
                    continue
                # get function name from line starting with marker [
                if line.startswith('['):
                    if func_name != '' and lines != '':
                        tc_key = '{}-{}'.format(pid, func_name)
                        self.add_error_item_to_testcase(stderr_type, tc_key, testcases, lines)
                        lines = ''
                    parts = line.split(']')
                    ts = parts[0][1:]
                    current_ts = ts
                    no_timestamp = ']'.join(parts[1:])
                    parts2 = no_timestamp.split(']')
                    func_name = parts2[0][1:]
                else:
                    lines += '[{}] {}\n'.format(current_ts, line)

            if func_name != '' and lines != '':
                tc_key = '{}-{}'.format(pid, func_name)
                self.add_error_item_to_testcase(stderr_type, tc_key, testcases, lines)
                func_name = ''
                lines = ''

    @staticmethod
    def add_error_item_to_testcase(stderr_type, tc_key, testcases, lines):
        """
        Update a test case in the base report with an assertion or error
        :param stderr_type: error or assertion
        :param tc_key: key into base report dict
        :param testcases: base report
        :param lines: captured stacktrace to add
        :return:
        """
        assert tc_key in testcases
        if stderr_type == 'error':
            testcases[tc_key].add_error(lines)
        else:
            testcases[tc_key].add_assertion(lines)

    @staticmethod
    def create_json_report(testcases, start, name):
        """
        Creates a JSON representation of the report
        :param testcases: base report with errors and assertions added
        :param start: timestamp of run start
        :param name: report name
        :return: JSON test run report
        """
        testcases_json = []
        passed = 0
        failed = 0
        errors = 0
        tests = 0
        for key, case in testcases.items():
            tests += 1
            testcases_json.append(case.__dict__)
            if hasattr(case, 'assertion') and case.assertion is not None:
                failed += 1
            elif hasattr(case, 'error') and case.error is not None:
                errors += 1
            else:
                passed += 1

        end = time.time()

        suite = {'tests': tests, 'passed': passed, 'errors': errors, 'failed': failed, 'testcase': [testcases_json],
                 'host': socket.gethostname(), 'duration': end - start, 'name': name,
                 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        return suite



