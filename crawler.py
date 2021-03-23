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
import requests

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

                if self.current_page_html == "BINARY":
                    #TODO: save page as binary
                    pass

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

        req = requests.get(page_to_crawl_url)

        if(req.headers['content-type'] == "application/pdf"):
            print("PDF")
            return "BINARY"
        elif(req.headers['content-type'] == "application/msword"):
            print("DOC")
            return "BINARY"
        elif(req.headers['content-type'] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            print("DOCX")
            return "BINARY"
        elif(req.headers['content-type'] == "application/vnd.ms-powerpoint"):
            print("PPT")
            return "BINARY"
        elif(req.headers['content-type'] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"):
            print("PPTX")
            return "BINARY"

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

            current_url_relative = link.get('href')

            current_url = urllib.parse.urljoin(self.site_currently_crawling[1], current_url_relative)

            current_parsed_url = urllib.parse.urlparse(current_url)

            links.add(current_parsed_url)

        for image in soup.find_all("img"):

            current_url_relative = image.get('src')

            current_url = urllib.parse.urljoin(self.site_currently_crawling[1], current_url_relative)

            current_parsed_url = urllib.parse.urlparse(current_url)

            images.add(current_parsed_url)
        
        print(images)

        return list(links)


    def add_links_to_frontier(self):
        for link in self.links_to_crawl:

            current_link_url = link.geturl()
            current_link_domain = link.netloc

            self.lock.acquire()
            all_sites = db.get_all_sites()
            all_pages = db.get_all_pages()
            self.lock.release()
            # we need a list of already existing domain urls in db
            # we need a list of already existing page urls in db

            all_sites_urls = []
            all_pages_urls = []

            for site in all_sites:
                all_sites_urls.append(urllib.parse.urlparse(site[1]))

            for page in all_pages:
                all_pages_urls.append(urllib.parse.urlparse(page[3]))


            # Only scrape sites in the gov.si domain
            ALLOWED_DOMAIN = ".gov.si"
            if ALLOWED_DOMAIN in current_link_domain:
                pass
                # Only add pages in the allowed domain

                # check if the link exists in any of the pages in db



                # check if the domain of the link already exists in db
                    # if it does, check if the full link already exists in


            #
            #
            # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=link)
            # print("---------------------------->DOMAIN:", domain)
            #
            # if domain == self.site_currently_crawling[1]:
            #     # we are on the same domain, so just add page on the same domain
            # else:
            #     # we are on a new domain, so create a new site, ad page to this new site
            # pass

