import sqlite3
import utils

db_name = "../pokeRol.db"

typesDB = {}

def insertTypes(types):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT OR IGNORE INTO types (name) VALUES (?)",
        [(t,) for t in types]
    )

    conn.commit()

    # Obtener todos los tipos y sus IDs
    cursor.execute("SELECT id, name FROM types")
    rows = cursor.fetchall()

    # Guardar en el diccionario
    global typesDB
    typesDB = {name: id for id, name in rows}


    conn.close()

def insertPokemons(pokemons):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for pokemon in pokemons:
        pokemonPrepared = utils.prepare_pokemon_for_db(pokemon)
        cursor.execute("""
            INSERT OR REPLACE INTO pokemons (
                dex_num, name, evasion, vitality,
                strength, agility, endurance, mind, spirit, presence,
                min_level, capture_rate, diet, sex, habitat
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, pokemonPrepared)

        pokemon_id = cursor.lastrowid
        for type in pokemon['types']:
            cursor.execute("""
                INSERT OR REPLACE INTO pokemon_types (
                    pokemon_id, type_id
                )
                VALUES (?, ?)
            """, (pokemon_id,type))


    conn.commit()

    conn.close()
