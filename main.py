import threading
from queue import Queue
from crawler import Crawler
from domain import *
import helper_functions as hf
import time
import db_methods as db
import urllib.request, urllib.robotparser, urllib.parse
import run_this_if_you_want_to_clear_db

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

USER_AGENT = 'fri-wier-wieramemo-vase'
SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
NUMBER_OF_THREADS = 3
PAGE_TYPE_CODES = ["HTML","DUPLICATE","FRONTIER","BINARY"]
DATA_TYPES = ["DOC","DOCX","PDF","PPT","PPTX"]

time_accessed = {'http://gov.si': 0, 'http://evem.gov.si': 0, 'http://e-uprava.gov.si': 0, 'http://e-prostor.gov.si': 0}

crawler_threads = []

import sys
print("Python version")
print (sys.version)


# inserting page and site rows for seed urls
def insert_seed_urls_into_db():
    for seed_url in SEED_URLS:
        page_obj = urllib.parse.urlparse(seed_url)

        current_url = page_obj.geturl()
        current_site_url =  page_obj.scheme + "://" + page_obj.netloc

        robotstext_content, sitemap_content = Crawler.get_robots_and_sitemap_content(current_site_url)

        current_site = db.insert_site(current_site_url, robotstext_content, sitemap_content)
        current_page = db.insert_page(current_site[0], PAGE_TYPE_CODES[2], current_url, "", "","200", "040521")


def create_workers():
    lock = threading.Lock()
    for i in range(NUMBER_OF_THREADS):
        current_crawler = Crawler(time_accessed, lock)
        current_crawler.start()
        crawler_threads.append(current_crawler)


insert_seed_urls_into_db()
create_workers()

while True:
    time.sleep(1)
