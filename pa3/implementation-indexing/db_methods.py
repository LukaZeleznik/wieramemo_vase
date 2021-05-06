import sqlite3

DB_FILE = "inverted-index.db"

conn = sqlite3.connect(DB_FILE)

# ----------> IndexWord METHODS <---------- #
def insert_IndexWord(word):
    cur = conn.cursor()
    query = "INSERT OR IGNORE INTO IndexWord(word) VALUES (?)"
    data_to_insert = (word,)
    try:
        ex = cur.execute(query, data_to_insert)
        conn.commit()
        return ex
    except sqlite3.Error as error:
        print("Error IndexWord: " + error.args[0])
    return

def delete_IndexWord():
    cur = conn.cursor()

    query = "DELETE FROM IndexWord"
    try:
        ex = cur.execute(query)
        conn.commit()
        return ex
    except sqlite3.Error as error:
        print("Error IndexWord: " + error.args[0])

    return

# ----------> Posting  METHODS <---------- #
def insert_Posting(word, documentName, frequency , indexes):
    cur = conn.cursor()
    query = "INSERT OR IGNORE INTO Posting(word, documentName, frequency, indexes) VALUES (?, ?, ?, ?)"
    data_to_insert = (word, documentName, frequency , indexes)
    try:
        ex = cur.execute(query, data_to_insert)
        conn.commit()
        return ex
    except sqlite3.Error as error:
        print("Error Posting: " + error.args[0])
    return

def delete_Posting():
    cur = conn.cursor()

    query = "DELETE FROM Posting"
    try:
        ex = cur.execute(query)
        conn.commit()
        return ex
    except sqlite3.Error as error:
        print("Error Posting: " + error.args[0])

    return

def search_Postings(query):
    c = conn.cursor()
    sql_query = '''
        SELECT p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
        FROM Posting p
        WHERE
            p.word IN ({seqe})
        GROUP BY p.documentName
        ORDER BY freq DESC;
    '''.format(
        seqe=','.join(['?'] * len(query)))
    data_to_insert = query

    #sql = "select * from sqlitetable where rowid in ({seq})".format(
     #   seq=','.join(['?'] * len(args)))

    try:
        res = c.execute(sql_query, data_to_insert)
        conn.commit()
        return res
    except sqlite3.Error as error:
        print("Error Search: " + error.args[0])
    return

# ----------> OTHER METHODS <---------- #
def close_connection():
    try:
        conn.close()
    except sqlite3.Error as error:
        print("DB error" + error.args[0])
