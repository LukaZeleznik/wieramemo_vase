import threading
from queue import Queue
from crawler import Crawler
from domain import *
import helper_functions as hf
import time

USER_AGENT = 'fri-wier-wieramemo-vase'
SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
DOMAIN_NAME = 'gov.si'
NUMBER_OF_THREADS = 8
FRONTIER_FILE = 'frontier.txt'
CRAWLED_FILE = 'crawled.txt'


crawler_threads = []

def create_workers():
    for i in range(NUMBER_OF_THREADS):
        current_crawler = Crawler()
        current_crawler.start()
        crawler_threads.append(current_crawler)
    while True:
        time.sleep(1)


create_workers()
