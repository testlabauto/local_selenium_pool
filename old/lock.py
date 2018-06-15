import multiprocessing
from concurrent.futures import ProcessPoolExecutor

import time

def f(i, lock):
    with lock:
        print(i, 'hello')
        time.sleep(1)
        print(i, 'world')

def main():
    pool = ProcessPoolExecutor()
    m = multiprocessing.Manager()
    lock = m.Lock()
    futures = [pool.submit(f, num, lock) for num in range(5)]
    for future in futures:
        future.result()


if __name__ == '__main__':
    main()