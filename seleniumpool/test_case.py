class TestCase(object):
    def __init__(self, function, process_id, stdout):
        self.function = function
        self.process_id = process_id
        self.stdout = stdout
        self.passed = True

    def add_error(self, current_error):
        self.error = current_error

    def add_assertion(self, current_assertion):
        self.assertion = current_assertion

    def failed(self):
        self.passed = False