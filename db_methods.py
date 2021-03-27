import psycopg2

DBNAME = "wier"
USER = "postgres"
PASSWORD = "admin"
PORT = "5432"
LOCALHOST = "localhost"
CONN_DATA = "dbname=" + DBNAME + " user=" + USER + " host=" + LOCALHOST + " password=" + PASSWORD + " port=" + PORT


# ----------> SITE METHODS <---------- #
def insert_site(domain, robots, sitemap):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "INSERT INTO crawldb.site(domain, robots_content, sitemap_content) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING RETURNING *"
    data_to_insert = (domain, robots, sitemap)
    cur.execute(query, data_to_insert)
    conn.commit()

    inserted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return inserted_entry


def get_site_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.site WHERE id = %s"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    found_entry = cur.fetchone()

    cur.close()
    conn.close()

    return found_entry


def get_all_sites():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.site"
    cur.execute(query)
    conn.commit()

    all_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_entries


def delete_site_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.site WHERE id = %s RETURNING *"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    deleted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return deleted_entry


def delete_all_sites():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.site RETURNING *"
    cur.execute(query)
    conn.commit()

    all_deleted_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_deleted_entries


# ----------> PAGE METHODS <---------- #
def insert_page(site_id, page_type_code, url, html_content, hash_content, http_status_code, accessed_time):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, hash_content, http_status_code, accessed_time) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING *"
    data_to_insert = (site_id, page_type_code, url, html_content, hash_content, http_status_code, accessed_time)
    cur.execute(query, data_to_insert)
    conn.commit()

    inserted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return inserted_entry


def get_page_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.page WHERE id = %s"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    found_entry = cur.fetchone()

    cur.close()
    conn.close()

    return found_entry


def get_all_pages():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.page ORDER BY id ASC"
    cur.execute(query)
    conn.commit()

    all_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_entries


def update_page_by_id(id, site_id, page_type_code, url, html_content, hash_content, http_status_code, accessed_time):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "UPDATE crawldb.page SET site_id = %s, page_type_code = %s, url = %s, html_content = %s, hash_content = %s, http_status_code = %s, accessed_time = %s WHERE id = %s RETURNING *"
    data_to_insert = (site_id, page_type_code, url, html_content, hash_content, http_status_code, accessed_time, id)
    cur.execute(query, data_to_insert)
    conn.commit()

    updated_entry = cur.fetchone()

    cur.close()
    conn.close()

    return updated_entry


def delete_page_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.page WHERE id = %s RETURNING *"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    deleted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return deleted_entry


def delete_all_pages():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.page RETURNING *"
    cur.execute(query)
    conn.commit()

    all_deleted_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_deleted_entries


# ----------> IMAGE METHODS <---------- #
def insert_image(page_id, filename, content_type, data, accessed_time):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time) VALUES (%s, %s, %s, %s, to_timestamp(%s)) ON CONFLICT DO NOTHING RETURNING *"
    data_to_insert = (page_id, filename, content_type, data, accessed_time)
    cur.execute(query, data_to_insert)
    conn.commit()

    inserted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return inserted_entry


def get_image_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.image WHERE id = %s"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    found_entry = cur.fetchone()

    cur.close()
    conn.close()

    return found_entry


def get_all_images():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.image"
    cur.execute(query)
    conn.commit()

    all_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_entries


def delete_image_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.image WHERE id = %s RETURNING *"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    deleted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return deleted_entry


def delete_all_images():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.image RETURNING *"
    cur.execute(query)
    conn.commit()

    all_deleted_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_deleted_entries


# ----------> PAGE_DATA METHODS <---------- #
def insert_page_data(page_id, data_type_code, data):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "INSERT INTO crawldb.page_data(page_id, data_type_code, data) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING RETURNING *"
    data_to_insert = (page_id, data_type_code, data)
    cur.execute(query, data_to_insert)
    conn.commit()

    inserted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return inserted_entry


def get_page_data_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.page_data WHERE id = %s"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    found_entry = cur.fetchone()

    cur.close()
    conn.close()

    return found_entry


def get_all_page_data():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.page_data"
    cur.execute(query)
    conn.commit()

    all_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_entries


def delete_page_data_by_id(id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.page_data WHERE id = %s RETURNING *"
    data_to_insert = (id,)
    cur.execute(query, data_to_insert)
    conn.commit()

    deleted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return deleted_entry


def delete_all_page_data():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.page_data RETURNING *"
    cur.execute(query)
    conn.commit()

    all_deleted_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_deleted_entries


# ----------> LINK METHODS <---------- #
def insert_link(from_page_id, to_page_id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "INSERT INTO crawldb.link(from_page, to_page) VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING *"
    data_to_insert = (from_page_id, to_page_id)
    cur.execute(query, data_to_insert)
    conn.commit()

    inserted_entry = cur.fetchone()

    cur.close()
    conn.close()

    return inserted_entry


def get_all_links():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.link"
    cur.execute(query)
    conn.commit()

    all_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_entries


def delete_all_links():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "DELETE FROM crawldb.link RETURNING *"
    cur.execute(query)
    conn.commit()

    all_deleted_entries = cur.fetchall()

    cur.close()
    conn.close()

    return all_deleted_entries

# ----------> DUPLICATE FINDER METHODS <---------- #
def find_page_duplicate(hash_content):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT * FROM crawldb.page WHERE hash_content = %s"
    data_to_insert = (hash_content,)
    cur.execute(query, data_to_insert)
    conn.commit()

    page = cur.fetchone()

    cur.close()
    conn.close()

    return page is not None

def check_site_exists(domain):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "SELECT id FROM crawldb.site WHERE domain = %s"
    data_to_insert = ['http://e-uprava.gov.si']
    cur.execute(query, data_to_insert)
    conn.commit()

    res = cur.fetchone()
    cur.close()
    conn.close()

    #print("check site exists: ", res)

    if(res is None): return False

    return res[0]
