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


# ----------> OTHER METHODS <---------- #
def close_connection():
    try:
        conn.close()
    except sqlite3.Error as error:
        print("DB error" + error.args[0])
