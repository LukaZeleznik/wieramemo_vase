import os
import psycopg2

DBNAME = "wier"
USER = "postgres"
PASSWORD = "admin"
CONN_DATA = "dbname="+DBNAME+" user="+USER+" password="+PASSWORD

def insert_site(domain, robots, sitemap):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "insert into crawldb.site(domain, robots_content, sitemap_content) VALUES ('"+domain+"', '"+robots+"', '"+sitemap+"') RETURNING *;"

    cur.execute(query)
    insertedid = cur.fetchone()
    conn.commit()
    cur.close()

    return insertedid

def get_sites():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()
    query = "SELECT * FROM crawldb.site"
    cur.execute(query)
    wier = cur.fetchall()
    cur.close()
    return wier

def insert_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "insert into crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time) VALUES ('"+str(site_id)+"', '"+page_type_code+"', '"+url+"', '"+html_content+"', '"+http_status_code+"', '"+accessed_time+"') RETURNING *;"

    cur.execute(query)
    insertedid = cur.fetchone()
    conn.commit()
    cur.close()

    return insertedid

def get_pages():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()
    query = "SELECT * FROM crawldb.page"
    cur.execute(query)
    wier = cur.fetchall()
    cur.close()
    return wier

def insert_image(page_id, filename, content_type, data, accessed_time):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "insert into crawldb.image(page_id, filename, content_type, data, accessed_time) VALUES ('"+str(page_id)+"', '"+filename+"', '"+content_type+"', '"+str(data)+"', '"+accessed_time+"') RETURNING *;"

    cur.execute(query)
    insertedid = cur.fetchone()
    conn.commit()
    cur.close()

    return insertedid

def get_images():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()
    query = "SELECT * FROM crawldb.image"
    cur.execute(query)
    wier = cur.fetchall()
    cur.close()
    return wier

def insert_page_data(page_id, data_type_code, data):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "insert into crawldb.page_data(page_id, data_type_code, data) VALUES ('"+str(page_id)+"', '"+data_type_code+"', '"+str(data)+"') RETURNING *;"

    cur.execute(query)
    insertedid = cur.fetchone()
    conn.commit()
    cur.close()

    return insertedid

def get_page_data():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()
    query = "SELECT * FROM crawldb.page_data"
    cur.execute(query)
    wier = cur.fetchall()
    cur.close()
    return wier

def insert_link(from_page_id, to_page_id):
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()

    query = "insert into crawldb.link(from_page, to_page) VALUES ('"+str(from_page_id)+"', '"+str(to_page_id)+"') RETURNING *;"

    cur.execute(query)
    insertedid = cur.fetchone()
    conn.commit()
    cur.close()

    return insertedid

def get_links():
    conn = psycopg2.connect(CONN_DATA)
    cur = conn.cursor()
    query = "SELECT * FROM crawldb.link"
    cur.execute(query)
    wier = cur.fetchall()
    cur.close()

    return wier