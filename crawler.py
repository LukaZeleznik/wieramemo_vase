from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib import parse
from helper_functions import *

SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
USER_AGENT = 'fri-wier-wieramemo-vase'
TIMEOUT = 5

# Tutorial:  https://www.youtube.com/watch?v=nRW90GASSXE&list=PL6gx4Cwl9DGA8Vys-f48mAH9OKSUyav0q&ab_channel=thenewboston

class Crawler:

    # Declared Class variables (shared among multiple spiders)
    base_url = ''
    domain_name = ''
    frontier_file = ''
    crawled_file = ''
    frontier = set()
    crawled = set()

    def __init__(self, seedURLs, domain_name):
        Crawler.base_url = seedURLs[0] # Base_url just gov.si for now
        Crawler.domain_name = domain_name # Domain name so we don't crawl the whole internet
        self.setup_crawler()
        self.crawl_page('Spider numero uno', Crawler.base_url)
        print("2. Frontier (also in frontier.txt):")
        print(Crawler.frontier)

    # Take the seed urls and insert them into the frontier. (just the first one... for now)
    @staticmethod
    def setup_crawler():

        create_data_files(Crawler.base_url)
        Crawler.frontier = file_to_set('frontier.txt')
        print("1. Frontier is:")
        print(Crawler.frontier)
        Crawler.crawled = file_to_set('crawled.txt')

    # Start crawling pages
    @staticmethod
    def crawl_page(thread, page_url):
        # For now crawl only gov.si
        # Check if url has already been crawled
        if page_url not in Crawler.crawled:
            print("Now crawling: " + page_url)

            # Gather links
            gathered_links = Crawler.gather_links(page_url)

            # Add them to frontier
            Crawler.add_links_to_frontier(gathered_links)

            # Remove page from frontier to crawled set
            Crawler.frontier.remove(page_url)
            Crawler.crawled.add(page_url)

            # Update txt files
            Crawler.update_files()

    # Find a href attributes on html page
    @staticmethod
    def gather_links(page_url):
        # Define Browser Options
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
            print("Relative url: " + value, "  Joined url: " + joinedUrl)
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
            ## !! IMPORTANT !! Fix domain checking
            if Crawler.domain_name not in link:
                continue
            Crawler.frontier.add(link)

    @staticmethod
    def update_files():
        set_to_file(Crawler.frontier, 'frontier.txt')
        set_to_file(Crawler.crawled, 'crawled.txt')

# Begin crawler program #
crw = Crawler(SEED_URLS, 'gov.si')
