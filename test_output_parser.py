from poolworker import TestOutputParser

sample_out ='''Process 8538:

Starting get_url
dress 7
[assertfail]Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 175, in execute_job
    output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 127, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 88, in get_url
    assert n == 6, "msg 1"
AssertionError: msg 1
[assertfail]
Starting get_url9
evening 1
evening $52.99
Finished get_url9

Process 8540:

Starting get_url2
chiffon 2
chiffon $48.90
Finished get_url2
Starting get_url6
popular 0
Finished get_url6
Starting get_url7
faded 1
faded $18.51
[error]Traceback (most recent call last):
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 175, in execute_job
    output_queue=self.output_queue)
  File "/Users/cmead/local_selenium_pool/poolworker.py", line 127, in wrapper
    test_function(**kwargs)
  File "/Users/cmead/local_selenium_pool/test_pool.py", line 152, in get_url7
    print (1/0)
ZeroDivisionError: division by zero
[error]

Process 8537:

Starting get_url4
printed 5
printed $154.87
Finished get_url4
Starting get_url8
straps 2
straps $47.38
Finished get_url8

Process 8539:

Starting get_url3
blouse 1
blouse $29.00
Finished get_url3
Starting get_url5
summer 4
summer $94.39
Finished get_url5
55.22320222854614'''


if __name__ == "__main__":
    parser = TestOutputParser()
    parsed = parser.parse(sample_out)
    print(parsed)