from concurrent import futures
import os
import time


class Connection():
    def __init__(self, id):
        self.id = id
        self.in_use = False

    def use(self):
        self.in_use = True

    def done(self):
        self.in_use = False

    def inuse(self):
        return self.in_use

connections = [Connection('1'), Connection('2'), Connection('3'), Connection('4')]
def get_connection():

    for connection in connections:
        if not connection.inuse():
            connection.use()
            return connection


def task(n):
    c = get_connection()


    print(c.id)
    c.done()
    return (n, os.getpid())


ex = futures.ProcessPoolExecutor(max_workers=3)

results = ex.map(task, range(5, 0, -1))
for n, pid in results:
    print('ran task {} in process {}'.format(n, pid))