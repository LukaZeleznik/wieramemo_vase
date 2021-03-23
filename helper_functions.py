import os
import psycopg2
import time
import random


def can_domain_be_accessed_at_current_time(domain_url, time_accessed, time_between_calls):
    current_time = int(time.time())

    # if domain url has not yet been accessed, we can access it right away
    if domain_url not in time_accessed:
        time_accessed[domain_url] = current_time
        return True

    # else, we have to check if the appropriate amount of time has passed
    if current_time >= time_accessed[domain_url] + time_between_calls:
        # if enough time has passed, we can acces the domain
        time_accessed[domain_url] = current_time
        return True

    # if not enough time has passed, we cannot
    return False

def wait5sDelay(domain_name, time_accessed, lock):
    if domain_name not in time_accessed:
        time_accessed[domain_name] = 0    

    while True:
        current_time = int(time.time())
        if (current_time > time_accessed[domain_name] + 5):
            lock.acquire()
            time_accessed[domain_name] = current_time
            lock.release()
            # print("time_accessed: ", time_accessed)
            # print("time_accessed[domain_name]: ", time_accessed[domain_name])
            return
        random_wait = random.randint(1, 5)
        time.sleep(random_wait)
    

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

def delete_file_contents(path):
    with open(path, 'w'):
        pass

def create_data_files(base_url):
    frontier = 'frontier.txt'
    crawled = 'crawled.txt'

    # Create frontier txt file
    #if not os.path.isfile(frontier):
    f = open(frontier, 'w')
    f.write(base_url)
    f.close()
    # Create crawled txt file
    #if not os.path.isfile(crawled):
    f = open(crawled, 'w')
    f.write('')
    f.close()

# Read a file into a set
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Convert set of links to a file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)


