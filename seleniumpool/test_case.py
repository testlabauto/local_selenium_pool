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