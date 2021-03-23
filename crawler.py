from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib import parse
import urllib.request, urllib.robotparser
import helper_functions as hf
import selenium
import lxml
from threading import Thread, currentThread
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
        self.page_currently_crawling = None
        self.site_currently_crawling = None
        self.time_between_calls = 5

    def stop(self):
        self.running = False

    def run(self):
        while self.running:

            page_to_crawl, page_to_crawl_site = self.get_page_to_crawl()

            self.page_currently_crawling = page_to_crawl
            self.site_currently_crawling = page_to_crawl_site

            print("page to crawl found:", page_to_crawl)
            self.stop()

            # self.crawl_page("http://gov.si", "http://gov.si", self.time_accessed)
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
                print("There are no pages available to crawl!")
                self.lock.release()
                self.stop()

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


    # Start crawling pages
    def crawl_page(self, page_url, domain_name, time_accessed):

        # Check if url has already been crawled
        # check if enough time has elapsed from the last request

        #if page_url not in Crawler.crawled:
        print(str("thread") + " now crawling: " + page_url)
        #print('Frontier ' + str(len(Crawler.frontier)) + ' | Crawled  ' + str(len(Crawler.crawled)))

        # Gather links
        gathered_links = self.gather_links(page_url, domain_name, time_accessed)
        print("Gathered links:", gathered_links)

        # Add them to frontier
        #self.add_links_to_frontier(gathered_links)

        # Remove page from frontier to crawled set
        # Crawler.frontier.remove(page_url)
        # Crawler.crawled.add(page_url)

        # Update txt files
        # Crawler.update_files()

    # Find a href attributes on html page
    def gather_links(self, page_url, domain_name, time_accessed):
        # Define Browser Options

        hf.wait5sDelay(domain_name, time_accessed, self.lock)

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Hides the browser window
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(page_url)

        # Not sure what timeout does
        time.sleep(TIMEOUT)
        htmltext = driver.page_source
        driver.quit()

        # Parse HTML structure
        soup = BeautifulSoup(htmltext, "lxml")

        # Extract links to profiles from TWDS Authors
        links = set()
        for link in soup.find_all("a"):
            current_url = link.get('href')

            # Links can be relative so join them with base_url
            #print("Relative url: " + value, "  Joined url: " + joinedUrl)
            links.add(joinedUrl)

        return links
    #
    #
    # def add_links_to_frontier(links):
    #     # Are they already in frontier?
    #     # Are they already in the crawled list?
    #     for link in links:
    #         if link in Crawler.frontier or link in Crawler.crawled:
    #             continue
    #         # Url should contain the domain gov.si
    #         ## FILTER URLS !!
    #         if Crawler.domain_name not in link:
    #             continue
    #         Crawler.frontier.add(link)
