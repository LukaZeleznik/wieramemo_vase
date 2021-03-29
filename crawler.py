from requests.models import MissingSchema

from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib import parse
import urllib.request, urllib.robotparser, urllib.parse
import helper_functions as hf

import lxml
from threading import Thread
import threading
import db_methods as db
import random
import requests
import os.path
from hash_tool import HashTool
from datetime import datetime

import urlcanon

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumwire import webdriver


SEED_URLS = ['http://gov.si', 'http://evem.gov.si', 'http://e-uprava.gov.si', 'http://e-prostor.gov.si']
USER_AGENT = 'fri-wier-wieramemo-vase'
TIMEOUT = 5
PAGE_TYPE_CODES = ["HTML", "DUPLICATE", "FRONTIER", "BINARY"]
DATA_TYPES = ["DOC", "DOCX", "PDF", "PPT", "PPTX"]
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
MAX_HTML_SIMILARITY = 1

# Create a global hash tool for page signatures
hash_tool = HashTool()


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
        self.status_code = None
        self.accessed_time = None
        self.links_to_crawl = []

        chrome_options = Options()

        prefs = {
            "download.open_pdf_in_system_reader": False,
            "download.prompt_for_download": True,
            "download.default_directory": "/dev/null",
            "plugins.always_open_pdf_externally": False
        }
        chrome_options.add_experimental_option(
            "prefs", prefs
        )

        chrome_options.add_argument("--headless")  # Hides the browser window
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome(options=chrome_options)



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

            t1_1 = time.time()
            page_to_crawl, page_to_crawl_site = self.get_page_to_crawl()
            t2_1 = time.time()

            self.page_currently_crawling = page_to_crawl
            self.site_currently_crawling = page_to_crawl_site

            #print(self.page_currently_crawling[3], "finding url took", t2_1 - t1_1)

            # check if there is a page available to crawl

            if self.page_currently_crawling is None or self.site_currently_crawling is None:
                random_wait = random.uniform(0, self.time_between_calls)
                time.sleep(random_wait)
                continue

            t1_2 = time.time()
            self.current_page_html, current_page_type = self.crawl_page()
            t2_2 = time.time()

            print(self.page_currently_crawling[3], "getting html took", t2_2 - t1_2)
            #print("--------------------> self.page_currently_crawling: ", self.page_currently_crawling[3])

            if current_page_type != "HTML":
                t1_6 = time.time()
                self.insert_page_as_binary(current_page_type)
                t2_6 = time.time()
                print(self.page_currently_crawling[3], "inserting binary took", t2_6 - t1_6)

            else:
                if self.current_page_html is not None:
                    # the page has not yet been crawled, so crawl it

                    t1_3 = time.time()
                    # If page is similiar to some other page - update to DUPLICATE and don't store html_content
                    if self.handle_duplicate_page():
                        # If page not a duplicate store its html_content
                        self.insert_page_hash()
                        continue

                    # Insert html in db
                    self.insert_html_content()

                    self.insert_page_hash()
                    t2_3 = time.time()
                    print(self.page_currently_crawling[3], "checking duplicate html took", t2_3 - t1_3)

                    t1_4 = time.time()
                    self.links_to_crawl = self.gather_links()
                    t2_4 = time.time()
                    print(self.page_currently_crawling[3], "gathering links took", t2_4 - t1_4)

                    t1_5 = time.time()
                    if len(self.links_to_crawl) > 0:
                        # if any links are found, add them to the frontier
                        self.add_links_to_frontier()
                    t2_5 = time.time()
                    print(self.page_currently_crawling[3], "adding to frontier took", t2_5 - t1_5)


        self.driver.quit()
            # time.sleep(1)

    def get_page_to_crawl(self):
        while True:
            # acquire lock

            all_pages = db.get_all_pages()


            # find first page that has the tag frontier
            page_to_crawl = None
            for page in all_pages:

                if page[2] == "FRONTIER":
                    page_to_crawl = page
                    break
            if page_to_crawl is None:
                #print("---------------------->", threading.get_ident(), "There are no pages available to crawl!")
                return None, None

            # get site url for the first page that has the tag frontier
            page_to_crawl_site = db.get_site_by_id(page_to_crawl[1])

            # check if the domain can be accessed at current time
            how_long_to_wait = hf.how_long_to_wait(page_to_crawl_site[1], self.time_accessed, self.time_between_calls)

            if how_long_to_wait == 0:
                # if yes, return page and domain, and mark the page as visited (just change the tag to HTML)

                #self.lock.acquire()
                updated_page = db.update_page_by_id(page_to_crawl[0], page_to_crawl[1], PAGE_TYPE_CODES[0],
                                                    page_to_crawl[3], page_to_crawl[4], page_to_crawl[5],
                                                    page_to_crawl[6], page_to_crawl[7])
                #self.lock.release()

                page_to_crawl = updated_page

                return page_to_crawl, page_to_crawl_site

            else:

                time.sleep(how_long_to_wait)

    # visit a page and return its content html
    def crawl_page(self):
        # Check if url has already been crawled
        page_to_crawl_url = self.page_currently_crawling[3]
        self.driver.get(page_to_crawl_url)

        #request = self.driver.requests[0]
        for request_iter in self.driver.requests:
            if request_iter.response:
                request = request_iter

        self.status_code = request.response.status_code
        self.accessed_time = datetime.now().strftime(TIMESTAMP_FORMAT)
        html_text = None
        # try:
        #     res = requests.get(page_to_crawl_url)
        # except Exception:
        #     print("url", page_to_crawl_url, "is not working")
        #     return None, None
        if (request.response.headers['content-type'] == "application/pdf"):
            print("PDF")
            current_page_type = "PDF"
        elif (request.response.headers['content-type'] == "application/msword"):
            print("DOC")
            current_page_type = "DOC"
        elif (request.response.headers['content-type'] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            print("DOCX")
            current_page_type = "DOCX"
        elif (request.response.headers['content-type'] == "application/vnd.ms-powerpoint"):
            print("PPT")
            current_page_type = "PPT"
        elif (request.response.headers[
                  'content-type'] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"):
            print("PPTX")
            current_page_type = "PPTX"
        else:
            current_page_type = "HTML"
            elements_present = EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
            try:
                WebDriverWait(self.driver, 5).until(elements_present)
            except Exception:
                print("timeout, url:", page_to_crawl_url,  self.driver.page_source)

            html_text = self.driver.page_source
        self.insert_status_code()
        self.insert_accessed_time()
        return html_text, current_page_type

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

            current_parsed_url_urlcanon = urlcanon.parse_url(current_url)
            urlcanon.whatwg(current_parsed_url_urlcanon)

            current_parsed_url = urllib.parse.urlparse(current_url)

            if(current_parsed_url.scheme != "http" and current_parsed_url.scheme !=  "https"):
                continue

            #print("uglyurl: ", current_url, "CANON: ", current_parsed_url_urlcanon, "current_parsed_url: ", current_parsed_url)

            # print("DOMAIN", self.site_currently_crawling[1])
            # print("     URL------->", current_url, current_parsed_url.geturl())

            links.add(current_parsed_url)

        onclicks = soup.find_all(attrs={'onclick': True})

        if len(onclicks) > 0:
            for onclick in onclicks:
                try:
                    x = onclick.find("location=")
                    if(x < 0): continue
                    onclick_split = onclick.split(onclick[x+9])
                    for index, string in enumerate(onclick_split):
                        if "location=" in string:
                            loc = onclick_split[index+1]
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", loc)
                            current_url = urllib.parse.urljoin(self.site_currently_crawling[1], loc)
                            current_parsed_url_urlcanon = urlcanon.parse_url(current_url)
                            urlcanon.whatwg(current_parsed_url_urlcanon)
                            current_parsed_url = urllib.parse.urlparse(current_url)
                            links.add(current_parsed_url)
                            break
                except Exception:
                    continue
                

        for image in soup.find_all("img"):
            current_url_relative = image.get('src')

            current_url = urllib.parse.urljoin(self.site_currently_crawling[1], current_url_relative)

            current_parsed_url = urllib.parse.urlparse(current_url)

            images.add(current_parsed_url)

        # print(images)

        for image in images:
            fullurl = urllib.parse.urljoin(self.site_currently_crawling[1], image.geturl())
            fullurl = urllib.parse.urlparse(fullurl)

            try:
                res = requests.get(fullurl.geturl())
            except Exception:
                continue

            content_type = res.headers['content-type']
            content = res.content
            url = image.geturl()
            path = urllib.parse.urlparse(url).path
            filename = os.path.basename(path)

            db.insert_image(self.page_currently_crawling[0], filename, content_type, content, int(time.time()))

        return list(links)

    def add_links_to_frontier(self):
        print("self.links_to_crawl: ", len(self.links_to_crawl))
        for link in self.links_to_crawl:

            current_link_url = link.geturl()

            # print("SCHEME: --->", link.scheme)
            current_link_domain = link.scheme + "://" + link.netloc

            #print("current_link_domain: ", current_link_domain)




            # Only scrape sites in the gov.si domain
            if not self.check_if_current_domain_is_allowed(current_link_domain):
                continue

            # Only add pages in the allowed domain

            #self.lock.acquire()
            #all_sites = db.get_all_sites()
            #all_pages = db.get_all_pages()

            # check if the link exists in any of the pages in db
            # check if the domain of the link already exists in db
            same_domain = False

            #domain_id = self.return_domain_if_it_already_exists(all_sites, current_link_domain)
            domain_id_or_false = db.check_site_exists(current_link_domain)

            if not domain_id_or_false:
                # new domain

                robotstext_content, sitemap_content = Crawler.get_robots_and_sitemap_content(current_link_domain)
                new_site = db.insert_site(current_link_domain, robotstext_content, sitemap_content)

                if self.check_if_page_is_allowed_by_robots_txt(new_site, current_link_url):
                    new_page = db.insert_page(new_site[0], PAGE_TYPE_CODES[2], current_link_url, "", "", "200",
                                                "040521")
                    db.insert_link(self.page_currently_crawling[0],new_page[0])
                    #print("inserting new page new domain")
            else:
                # existing domain
                if self.check_if_page_is_allowed_by_robots_txt(self.site_currently_crawling, current_link_url):


                    #print("inserting", current_link_url)
                    new_page = db.insert_page(domain_id_or_false, PAGE_TYPE_CODES[2], current_link_url, "", "", "200",
                                                "040521")
                    #print("inserting new page")

            #self.lock.release()

    def check_if_current_domain_is_allowed(self, domain_netloc):

        ALLOWED_DOMAIN = ".gov.si"
        # check if page contains gov.si
        return ALLOWED_DOMAIN in domain_netloc

    def check_page_url_duplicate(self, all_pages, link_url):
        # check if page url already exists in db
        return False

        duplicate_found = False
        for page in all_pages:

            current_page_url_string = page[3]

            if current_page_url_string == link_url:
                duplicate_found = True

                break

        return duplicate_found

    def return_domain_if_it_already_exists(self, all_sites, domain_link):
        current_link_domain_obj = urllib.parse.urlparse(domain_link)

        domain_netloc = current_link_domain_obj.netloc

        for site in all_sites:
            current_saved_site_obj = urllib.parse.urlparse(site[1])
            current_saved_site_netloc = current_saved_site_obj.netloc

            if current_saved_site_netloc == domain_netloc:
                return site[0]

        return -1

    def check_if_page_is_allowed_by_robots_txt(self, site_obj, link_url):
        rp = urllib.robotparser.RobotFileParser()

        rp.parse(site_obj[2].splitlines())
        # rp.set_url("http://" + self.site_currently_crawling[1] + "/robots.txt")
        # rp.read()
        return rp.can_fetch(USER_AGENT, link_url)

    def insert_page_hash(self):
        # acquire lock
        #self.lock.acquire()
        # Calculate hash from html
        hash = hash_tool.create_content_hash(self.current_page_html)

        # update hash of a page in db
        updated_page = db.update_page_by_id(self.page_currently_crawling[0], self.page_currently_crawling[1],
                                            self.page_currently_crawling[2],
                                            self.page_currently_crawling[3], self.page_currently_crawling[4], hash,
                                            self.page_currently_crawling[6], self.page_currently_crawling[7])
        self.page_currently_crawling = updated_page
        #self.lock.release()


    # Returns true if hash calculated from page html already exists in db. Also marks page as "DUPLICATE" in db
    def handle_duplicate_page(self):
        # acquire lock
        #self.lock.acquire()

        # Hash of a passed html_content
        h = hash_tool.create_content_hash(self.current_page_html)

        # Check if page is exact copy of already parsed documents in database
        returned_duplicate = db.find_page_duplicate(h)
        if returned_duplicate and returned_duplicate[3] != self.page_currently_crawling[3]:
            # Update page as 'DUPLICATE'
            updated_page = db.update_page_by_id(self.page_currently_crawling[0], self.page_currently_crawling[1],
                                                PAGE_TYPE_CODES[1], self.page_currently_crawling[3],
                                                self.page_currently_crawling[4], self.page_currently_crawling[5],
                                                self.page_currently_crawling[6], self.page_currently_crawling[7])
            self.page_currently_crawling = updated_page
            print("Page ", self.page_currently_crawling[3], "is a DUPLICATE from", returned_duplicate[3])

            # Save a new link: to_page is set to duplicate version
            db.insert_link(self.page_currently_crawling[0], returned_duplicate[0])

            #self.lock.release()
            return True
        return False
        """ else:
            # Calculate similarity html_content with others
            all_crawled_pages = db.get_all_crawled_pages()
            for page in all_crawled_pages:
                if page[4] and self.current_page_html is not None and page[3] != self.page_currently_crawling[3]:
                    similarity = hash_tool.calculate_similarity(self.current_page_html, page[4])
                    # print("PAGE: " , self.page_currently_crawling[3] , " and ", page[3], " SIMILARITY: ",
                    #     hash_tool.calculate_similarity(self.current_page_html, page[4]))
                    if similarity > MAX_HTML_SIMILARITY:
                        updated_page = db.update_page_by_id(self.page_currently_crawling[0],
                                                            self.page_currently_crawling[1],
                                                            PAGE_TYPE_CODES[1], self.page_currently_crawling[3],
                                                            self.page_currently_crawling[4],
                                                            self.page_currently_crawling[5],
                                                            self.page_currently_crawling[6],
                                                            self.page_currently_crawling[7])
                        self.page_currently_crawling = updated_page
                        print("Page ", self.page_currently_crawling[3], "is a DUPLICATE ALMOST: ", page[3],
                              " similarity ", similarity)
                        self.lock.release()
                        return True
            self.lock.release()
            return False """
        

    def insert_page_as_binary(self, data_type):
        #self.lock.acquire()
        db.update_page_by_id(self.page_currently_crawling[0], self.page_currently_crawling[1], "BINARY",
                             self.page_currently_crawling[3], self.page_currently_crawling[4],
                             self.page_currently_crawling[5],
                             self.page_currently_crawling[6], self.page_currently_crawling[7])

        db.insert_page_data(self.page_currently_crawling[0], data_type, None)
        #self.lock.release()

    @staticmethod
    def get_robots_and_sitemap_content(new_site):
        try:
            robotstxt = requests.get(new_site + "/robots.txt")
        except requests.exceptions.ConnectionError:
            print("Error: ", new_site, " has no robots.txt.")
            return "", ""

        if robotstxt.status_code != 200:
            return "", ""

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(new_site + "/robots.txt")
        rp.read()
        sitemap = rp.site_maps()

        robotstxt_content = robotstxt.content.decode("utf-8")
        if sitemap is not None:
            sitemap_content = requests.get(sitemap[0]).content.decode("utf-8")
        else:
            sitemap_content = ""

        return robotstxt_content, sitemap_content

    def insert_html_content(self):
        #self.lock.acquire()
        updated_page = db.update_page_by_id(self.page_currently_crawling[0], self.page_currently_crawling[1],
                                            self.page_currently_crawling[2],
                                            self.page_currently_crawling[3], self.current_page_html,
                                            self.page_currently_crawling[5],
                                            self.page_currently_crawling[6], self.page_currently_crawling[7])
        self.page_currently_crawling = updated_page
        #self.lock.release()

    def insert_status_code(self):
        #self.lock.acquire()
        updated_page = db.update_page_by_id(self.page_currently_crawling[0], self.page_currently_crawling[1],
                                            self.page_currently_crawling[2],
                                            self.page_currently_crawling[3], self.page_currently_crawling[4],
                                            self.page_currently_crawling[5],
                                            self.status_code, self.page_currently_crawling[7])
        self.page_currently_crawling = updated_page
        #self.lock.release()

    def insert_accessed_time(self):
        #self.lock.acquire()
        updated_page = db.update_page_by_id(self.page_currently_crawling[0], self.page_currently_crawling[1],
                                            self.page_currently_crawling[2],
                                            self.page_currently_crawling[3], self.page_currently_crawling[4],
                                            self.page_currently_crawling[5],
                                            self.page_currently_crawling[6], self.accessed_time)
        self.page_currently_crawling = updated_page
        #self.lock.release()
