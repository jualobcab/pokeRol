import sqlite3
import os

# Nombre del archivo
db_name = "../pokeRol.db"

def initialice():
    # Borrar si existe
    if os.path.exists(db_name):
        os.remove(db_name)
        print("Archivo pokeRol.db eliminado.")

    # Crear la base de datos
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    with open("../database/pokeRol.sql") as file:
        sql = file.read()
        cursor.executescript(sql)

    conn.commit()
    conn.close()

    print("Base de datos pokeRol.db creada correctamente.")
