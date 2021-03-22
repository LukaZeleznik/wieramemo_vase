import threading
from queue import Queue
from crawler import Crawler
from domain import *
import helper_functions as hf

USER_AGENT = 'fri-wier-wieramemo-vase'
SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
DOMAIN_NAME = 'gov.si'
NUMBER_OF_THREADS = 8
FRONTIER_FILE = 'frontier.txt'
CRAWLED_FILE = 'crawled.txt'

time_accessed = {'http://gov.si': 0, 'http://evem.gov.si': 0, 'http://e-uprava.gov.si': 0, 'http://e-prostor.gov.si': 0}

queue = Queue()
# Begin first crawler program #
Crawler(SEED_URLS, 'gov.si')

# Create worker thread (will die when main exists)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Work function to set next job in the queue
def work():
    while True:
        url = queue.get()  # Grab a link from frontier
        Crawler.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# Links are a new job
def create_jobs():
    for link in hf.file_to_set(FRONTIER_FILE):
        queue.put(link)
    queue.join()
    crawl()

# Check if there are items in frontier
def crawl():
    queued_links = hf.file_to_set(FRONTIER_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the frontier')
        create_jobs()

create_workers()
crawl()