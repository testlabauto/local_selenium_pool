import datetime
import json
from loselpo.output_queue import queue_get_all
from loselpo.test_case import TestCase
import socket
import time


class TestOutputParser(object):

    def add_error_item_to_testcase(self, stderr_type, tc_key, testcases, lines):
        assert tc_key in testcases
        testcases[tc_key].failed()
        if stderr_type == 'error':
            testcases[tc_key].add_error(lines)
        else:
            testcases[tc_key].add_assertion(lines)

    def process_stderr_component(self, stderr_type, queue, testcases):
        items = queue_get_all(queue)
        lines = ''
        func_name = ''
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
                    no_timestamp = ']'.join(parts[1:])
                    parts2 = no_timestamp.split(']')
                    func_name = parts2[0][1:]
                else:
                    lines += line + '\n'

            if func_name != '' and lines != '':
                tc_key = '{}-{}'.format(pid, func_name)
                self.add_error_item_to_testcase(stderr_type, tc_key, testcases, lines)
                func_name = ''
                lines = ''

    def parse(self, start, output_queue, name):
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
                    func_name = msg.split()[1]
                if msg.startswith('Finished'):
                    end_func_name = msg.split()[1]
                    assert func_name == end_func_name
                    runs.append((pid, func_name, lines))
                    lines = []

        testcases = {}
        for run in runs:
            tc = TestCase(function=run[1], process_id=run[0], stdout=[x[1] for x in run[2]])
            testcases['{}-{}'.format(run[0], run[1])] = tc

        self.process_stderr_component('error', output_queue.getErrorQueue(), testcases)
        self.process_stderr_component('assertion', output_queue.getAssertionQueue(), testcases)

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

        return json.dumps(suite, indent=4)
