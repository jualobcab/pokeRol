import sqlite3

db_name = "../pokeRol.db"

def insertTypes(types):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT OR IGNORE INTO types (name) VALUES (?)",
        [(t,) for t in types]
    )

    conn.commit()
    conn.close()
