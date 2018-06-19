import json
import time
import socket
from seleniumpool.test_case import TestCase


class TestOutputParser(object):
    def parse(self, start, outstring, name):
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
            elif hasattr(case, 'error') and case.error is not None:
                errors += 1
            else:
                passed += 1

        end = time.time()


        suite = {'tests': tests,
               'passed': passed,
               'errors': errors,
               'failed': failed,
               'testcase': [testcases_json],
               'host': socket.gethostname(),
               'duration': end - start}
        if name is not None:
            suite['name'] = name

        return json.dumps(suite, indent=4)