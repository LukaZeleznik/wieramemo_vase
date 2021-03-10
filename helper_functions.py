import os
import psycopg2

DBNAME = "wier"
USER = "postgres"
PASSWORD = "admin"

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

def insert_site(id, domain, robots, sitemap):
    conn = psycopg2.connect("dbname="+DBNAME+" user="+USER+" password="+PASSWORD)
    cur = conn.cursor()

    query = "insert into crawldb.site(id, domain, robots_content, sitemap_content) VALUES ("+str(id)+", '"+domain+"', '"+robots+"', '"+sitemap+"')"

    cur.execute(query)
    conn.commit()
    cur.close()

def get_sites():
    conn = psycopg2.connect("dbname="+DBNAME+" user="+USER+" password="+PASSWORD)
    cur = conn.cursor()
    query = "SELECT * FROM crawldb.site"
    cur.execute(query)
    wier = cur.fetchall()
    cur.close()
    return wier