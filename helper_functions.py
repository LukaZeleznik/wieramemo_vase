import os
import psycopg2
import time
import random

time_accessed = {'http://gov.si': 0, 'http://evem.gov.si': 0, 'http://e-uprava.gov.si': 0, 'http://e-prostor.gov.si': 0}

def wait5sDelay(domain_name):
    if domain_name not in time_accessed:
        time_accessed[domain_name] = 0
    
    current_time = int(time.time())

    if (current_time > time_accessed[domain_name] + 5):
        time_accessed[domain_name] = current_time
    else:
        random_wait = random.randint(1, 5)
        time.sleep(random_wait)
        return wait5sDelay(random_wait)

    

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


