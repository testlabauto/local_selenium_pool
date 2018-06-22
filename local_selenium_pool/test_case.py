class TestCase(object):
    """
    This class is used as part of the output report construction
    """
    def __init__(self, function, process_id, stdout, time, duration):
        """
        Test case objects are created with the function name, PID, and stdout.  Errors and assertions are added on
        afterwards
        :param function: test method name
        :param process_id: PID of subprocess running the test
        :param stdout: Stdout captured during test case run
        :param time: start time for test case
        :param duration: test case duration
        """
        self.function = function
        self.process_id = process_id
        self.stdout = stdout
        self.passed = True
        self.time = time
        self.duration = duration

    def add_error(self, current_error):
        """
        An error is an exception occuring during a test that is not from a failed assertion
        :param current_error: formatted string with stacktrace
        :return: None
        """
        self.error = current_error
        self.failed()

    def add_assertion(self, current_assertion):
        """
        An assertion includes a stacktrace
        :param current_assertion: formatted string with assertion
        :return:
        """
        self.assertion = current_assertion
        self.failed()

    def failed(self):
        """
        When an assertion or error is added, that test case is marked failed
        :return:
        """
        self.passed = False