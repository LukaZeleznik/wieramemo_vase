import psycopg2

DBNAME = "wier"
USER = "postgres"
PASSWORD = "admin"
PORT = "5432"
LOCALHOST = "localhost"
CONN_DATA = "dbname=" + DBNAME + " user=" + USER + " host=" + LOCALHOST + " password=" + PASSWORD + " port=" + PORT
siteids1 = [(201,), (228,), (252,), (263,), (272,), (276,), (285,), (305,), (309,), (314,), (319,), (323,), (327,), (331,), (335,), (339,), (343,), (347,), (351,), (355,), (359,), (363,), (370,), (374,), (391,), (422,), (430,), 
(436,), (440,), (464,), (492,), (496,), (503,), (547,), (551,), (555,), (562,), (566,), (570,), (574,), (578,), (585,), (589,), (593,), (597,), (604,), (608,), (206,)]
siteids2 = [(202,), (229,), (253,), (264,), (273,), (277,), (286,), (306,), (310,), (315,), (320,), (324,), (328,), (332,), (336,), (340,), (344,), (348,), (352,), (356,), (360,), (364,), (371,), (375,), (392,), (423,), (431,), 
(437,), (441,), (465,), (493,), (497,), (504,), (548,), (552,), (556,), (563,), (567,), (571,), (575,), (579,), (586,), (590,), (594,), (598,), (605,), (609,), (368,)]
siteids4 = [(204,), (231,), (255,), (266,), (275,), (279,), (288,), (308,), (312,), (317,), (322,), (326,), (330,), (334,), (338,), (342,), (346,), (350,), (354,), (358,), (362,), (366,), (373,), (377,), (394,), (425,), (433,), 
(439,), (443,), (467,), (495,), (499,), (506,), (550,), (554,), (558,), (565,), (569,), (573,), (577,), (581,), (588,), (592,), (596,), (600,), (607,), (611,), (402,), (211,)]

where = "site_id = 202"
for siteid in siteids2:
    where += " OR site_id = "+ str(siteid[0])

#print(where)


conn = psycopg2.connect(CONN_DATA)
cur = conn.cursor()

#query = "SELECT id FROM crawldb.site WHERE domain = 'http://www.evem.gov.si'"
#query = "SELECT site_id FROM crawldb.page WHERE " + where + " AND page_type_code = 'HTML'"
#query = "SELECT site_id FROM crawldb.page WHERE site_id = 203 AND page_type_code = 'FRONTIER'"
query = "SELECT id FROM crawldb.page_data WHERE data_type_code = 'PPTX'"
#query = "SELECT * FROM crawldb.page INNER JOIN crawldb.page_data ON crawldb.page.id = page_id WHERE ("+where+") AND data_type_code = 'PDF'"
cur.execute(query)
conn.commit()

res = cur.fetchall()
cur.close()
conn.close()

print(len(res))
#print(res)

""" f = open("links.txt", "a")
f.write(str(res))
f.close() """