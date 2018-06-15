from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor

URL ="https://pypi.python.org/pypi/{}"

li =["pywp/1.3","augploy/0.3.5"]

def get_content(url):
    driver = webdriver.Chrome()
    driver.get(url)
    tag = driver.find_element_by_tag_name("a")
    # do your work here and return the result
    return tag.get_attribute("href")


li = list(map(lambda link: URL.format(link), li ))


futures = []
with ThreadPoolExecutor(max_workers=2) as ex:
    for link in li:

        futures.append(ex.submit(get_content,link))

for future in futures:
    print(future.result())