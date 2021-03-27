import psycopg2

DBNAME = "wier"
USER = "postgres"
PASSWORD = "admin"
PORT = "5432"
LOCALHOST = "localhost"
CONN_DATA = "dbname=" + DBNAME + " user=" + USER + " host=" + LOCALHOST + " password=" + PASSWORD + " port=" + PORT




conn = psycopg2.connect(CONN_DATA)
cur = conn.cursor()

query = "SELECT id FROM crawldb.site WHERE domain = %s"
data_to_insert = ['http://e-uprava.gov.si']
cur.execute(query, data_to_insert)
conn.commit()

res = cur.fetchone()
cur.close()
conn.close()

if(res is None): print(False)

print(res[0])