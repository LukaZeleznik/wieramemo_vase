from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib import parse
import urllib.request, urllib.robotparser, urllib.parse
import helper_functions as hf
import selenium
import lxml
from threading import Thread
import threading
import db_methods as db
import random

SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
USER_AGENT = 'fri-wier-wieramemo-vase'
TIMEOUT = 5
PAGE_TYPE_CODES = ["HTML","DUPLICATE","FRONTIER","BINARY"]
DATA_TYPES = ["DOC","DOCX","PDF","PPT","PPTX"]

class Crawler(Thread):

    def __init__(self, time_accessed, lock):
        Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.time_accessed = time_accessed
        self.lock = lock
        self.time_between_calls = 5

        self.page_currently_crawling = None
        self.site_currently_crawling = None
        self.current_page_html = None
        self.links_to_crawl = []

    def stop(self):
        self.running = False

    def run(self):
        while self.running:

            # clear values from possible previous iterations
            self.page_currently_crawling = None
            self.site_currently_crawling = None
            self.current_page_html = None
            self.links_to_crawl = []

            # retrieve a page that is suitable for crawling
            page_to_crawl, page_to_crawl_site = self.get_page_to_crawl()
            self.page_currently_crawling = page_to_crawl
            self.site_currently_crawling = page_to_crawl_site

            # check if there is a page available to crawl
            if self.page_currently_crawling is not None and self.site_currently_crawling is not None:

                print("page to crawl found:", page_to_crawl)

                self.current_page_html = self.crawl_page()

                if self.current_page_html is not None:
                    # the page has not yet been crawled, so crawl it
                    print("------------------------------------> gathering links on page: ", self.page_currently_crawling[3])
                    self.links_to_crawl = self.gather_links()

                    if len(self.links_to_crawl) > 0:
                        # if any links are found, add them to the frontier
                        self.add_links_to_frontier()

                else:
                    # the page has already been crawled, need to mark it as duplicate
                    pass

            # time.sleep(1)

    def get_page_to_crawl(self):
        while True:
            # acquire lock
            self.lock.acquire()

            # get all pages
            all_pages = db.get_all_pages()

            # find first page that has the tag frontier
            page_to_crawl = None
            for page in all_pages:
                if page[2] == "FRONTIER":
                    page_to_crawl = page
                    break
            if page_to_crawl is None:
                print("---------------------->", threading.get_ident(), "There are no pages available to crawl!")
                self.lock.release()
                self.stop()
                return None, None

            # get site url for the first page that has the tag frontier
            page_to_crawl_site = db.get_site_by_id(page[1])

            # check if the domain can be accessed at current time
            if hf.can_domain_be_accessed_at_current_time(page_to_crawl_site[1], self.time_accessed, self.time_between_calls):
                # if yes, return page and domain, and mark the page as visited (just change the tag to HTML)
                updated_page = db.update_page_by_id(page_to_crawl[0], page_to_crawl[1], PAGE_TYPE_CODES[0],
                                                    page_to_crawl[3], page_to_crawl[4], page_to_crawl[5], page_to_crawl[6])
                page_to_crawl = updated_page
                self.lock.release()
                return page_to_crawl, page_to_crawl_site

            else:
                # if no, then wait for a random time
                self.lock.release()
                random_wait = random.uniform(0, self.time_between_calls)
                time.sleep(random_wait)


    # visit a page and return its content html
    def crawl_page(self):

        # Check if url has already been crawled

        page_to_crawl_url = self.page_currently_crawling[3]

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Hides the browser window
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(page_to_crawl_url)

        # Not sure what timeout does
        time.sleep(TIMEOUT)
        html_text = driver.page_source
        driver.quit()

        return html_text


    # Find a href attributes on html page
    def gather_links(self):
        # Define Browser Options

        soup = BeautifulSoup(self.current_page_html, "lxml")

        # Extract links to profiles from TWDS Authors
        links = set()
        images = set()
        for link in soup.find_all("a"):
            current_url = link.get('href')
            links.add(current_url)

        for image in soup.find_all("img"):
            value = image.get('src')
            joined_url = parse.urljoin(Crawler.base_url, value)
            images.add(joined_url)
        
        print(images)

        return list(links)


    def add_links_to_frontier(self):
        for link in self.links_to_crawl:
            print(link)

