from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib import parse
import urllib.request, urllib.robotparser
import helper_functions as hf
import selenium

SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
USER_AGENT = 'fri-wier-wieramemo-vase'
TIMEOUT = 5

from threading import Thread, currentThread

class Crawler(Thread):

    # Declared Class variables (shared among multiple spiders)
    base_url = ''
    domain_name = ''
    frontier_file = ''
    crawled_file = ''
    frontier = set()
    crawled = set()
    time_accessed = {}

    def __init__(self, time_accessed, lock):
        # Crawler.base_url = seedURLs[0] # Base_url just gov.si for now
        # Crawler.domain_name = domain_name # Domain name so we don't crawl the whole internet
        # self.setup_crawler()
        # self.crawl_page('Spider numero uno', Crawler.base_url, Crawler.domain_name)

        Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.time_accessed = time_accessed
        self.lock = lock


    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            print("in")
            self.crawl_page("http://gov.si", "http://gov.si", self.time_accessed)
            time.sleep(1)


    # Take the seed urls and insert them into the frontier. (just the first one... for now)
    @staticmethod
    def setup_crawler():

        hf.create_data_files(Crawler.base_url)
        Crawler.frontier = hf.file_to_set('frontier.txt')
        Crawler.crawled = hf.file_to_set('crawled.txt')

    # Start crawling pages
    def crawl_page(self, page_url, domain_name, time_accessed):
        # For now crawl only gov.si
        # Check if url has already been crawled

        # check if enough time has elapsed from the last request

        #if page_url not in Crawler.crawled:
        print(str("thread") + " now crawling: " + page_url)
        #print('Frontier ' + str(len(Crawler.frontier)) + ' | Crawled  ' + str(len(Crawler.crawled)))

        # Gather links
        gathered_links = Crawler.gather_links(self, page_url, domain_name, time_accessed)
        #print("Gathered links:", gathered_links)

        # Add them to frontier
        #Crawler.add_links_to_frontier(gathered_links)

        # Remove page from frontier to crawled set
        #Crawler.frontier.remove(page_url)
        #Crawler.crawled.add(page_url)

        # Update txt files
        #Crawler.update_files()

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
        authors = set()
        for link in soup.find_all("a"):
            value = link.get('href')
            joinedUrl = parse.urljoin(Crawler.base_url, value)
            # Links can be relative so join them with base_url
            #print("Relative url: " + value, "  Joined url: " + joinedUrl)
            authors.add(joinedUrl)

        return authors

    @staticmethod
    def add_links_to_frontier(links):
        # Are they already in frontier?
        # Are they already in the crawled list?
        for link in links:
            if link in Crawler.frontier or link in Crawler.crawled:
                continue
            # Url should contain the domain gov.si
            ## FILTER URLS !!
            if Crawler.domain_name not in link:
                continue
            Crawler.frontier.add(link)

    @staticmethod
    def update_files():
        hf.set_to_file(Crawler.frontier, 'frontier.txt')
        hf.set_to_file(Crawler.crawled, 'crawled.txt')