from poolworker import create_pool
from multiprocessing import JoinableQueue
import csv



# can use this:
#    def get_url(driver, url, *args, **kwargs):
# or:
#    def get_url(driver, url):
# or:
#    def get_url(driver, url, a, b, **kwargs):
# or:
#     def get_url(driver, url, *args):

def get_url(driver, results, url, *args, **kwargs):


    print('getting url {}'.format(url))
    driver.get(url)



def get_data():
    with open('test/random_urls.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    urls = [x[0] for x in your_list]
    return urls

if __name__ == "__main__":
    urls = get_data()

    url_queue = JoinableQueue()
    pool = create_pool(url_queue)

    for url in urls:
        url_queue.put((get_url, url))

    print('done putting')

    url_queue.join()

    print('here')




