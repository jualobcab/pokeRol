import sqlite3
import utils

db_name = "../pokeRol.db"

typesDB = {}
sizesDB = {}
habitatsDB = {}
environmentsDB = {}
proficienciesDB = {}
sensesDB = {}
abilitiesDB = {"dataDB":[]}
tagsDB = {}
movementsDB = {"dataDB":[]}
itemTypesDB = {}
itemsDB = []

DB_FILES = {
    "typesDB": "./json/typesDB.json",
    "sizesDB": "./json/sizesDB.json",
    "habitatsDB": "./json/habitatsDB.json",
    "environmentsDB": "./json/environmentsDB.json",
    "proficienciesDB": "./json/proficienciesDB.json",
    "sensesDB": "./json/sensesDB.json",
    "abilitiesDB": "./json/abilitiesDB.json",
    "tagsDB": "./json/tagsDB.json",
    "movementsDB": "./json/movementsDB.json",
    "itemTypesDB": "./json/itemTypesDB.json",
    "itemsDB": "./json/itemsDB.json"
}

def save_all_db_dicts():
    global typesDB
    global sizesDB
    global habitatsDB
    global environmentsDB
    global proficienciesDB
    global sensesDB
    global abilitiesDB
    global tagsDB
    global movementsDB
    global itemTypesDB
    global itemsDB

    data_map = {
        "typesDB": typesDB,
        "sizesDB": sizesDB,
        "habitatsDB": habitatsDB,
        "environmentsDB": environmentsDB,
        "proficienciesDB": proficienciesDB,
        "sensesDB": sensesDB,
        "abilitiesDB": abilitiesDB,
        "tagsDB": tagsDB,
        "movementsDB": movementsDB,
        "itemTypesDB": itemTypesDB,
        "itemsDB": itemsDB
    }

    for key, filename in DB_FILES.items():
        utils.save_json(filename, data_map[key])

    print("\n[OK] Todos los diccionarios han sido guardados.\n")

def load_all_db_dicts():
    results = {}

    for key, filename in DB_FILES.items():
        data = utils.load_json(filename)
        results[key] = data if data is not None else {}

    print("\n[OK] Todos los diccionarios han sido cargados.\n")

    global typesDB
    typesDB = results["typesDB"]
    global sizesDB
    sizesDB = results["sizesDB"]
    global habitatsDB
    habitatsDB = results["habitatsDB"]
    global environmentsDB
    environmentsDB = results["environmentsDB"]
    global proficienciesDB
    proficienciesDB = results["proficienciesDB"]
    global sensesDB
    sensesDB = results["sensesDB"]
    global abilitiesDB
    abilitiesDB = results["abilitiesDB"]
    global tagsDB
    tagsDB = results["tagsDB"]
    global movementsDB
    movementsDB = results["movementsDB"]
    global itemTypesDB
    itemTypesDB = results["itemTypesDB"]
    global itemsDB
    itemsDB = results["itemsDB"]

    insert_all_dbs()

def insert_all_dbs():
    global typesDB, sizesDB, habitatsDB, environmentsDB, proficienciesDB, sensesDB, abilitiesDB, tagsDB, movementsDB, itemTypesDB, itemsDB

    insert_dict_into_table("types", typesDB)
    insert_dict_into_table("sizes", sizesDB)
    insert_dict_into_table("habitats", habitatsDB)
    insert_dict_into_table("environments", environmentsDB)
    insert_dict_into_table("proficiencies", proficienciesDB)
    insert_dict_into_table("senses", sensesDB)
    insert_dict_into_table("abilities", abilitiesDB)
    insert_dict_into_table("tags", tagsDB)
    insert_dict_into_table("movements", movementsDB)
    insert_dict_into_table("item_types", itemTypesDB)
    insert_dict_into_table("items", itemsDB)

    print("[OK] Todos los diccionarios han sido insertados y actualizados.")

def insert_dict_into_table(table, data_dict):
    """
    Inserta todos los valores de un diccionario en una tabla SQLite.
    data_dict === { "nombre": id (opcional) }
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if table == 'abilities':
        # Preparar datos para executemany
        abilitiesPrepared = utils.prepare_abilities_for_db(data_dict["dataDB"])

        cursor.executemany(
            """
            INSERT OR IGNORE INTO abilities
            (name, description, transformation, legendary)
            VALUES (?, ?, ?, ?)
            """,
            abilitiesPrepared
        )
    elif table == 'movements':
        for movement in data_dict["dataDB"]:
            movementPrepared = utils.prepare_movements_for_db(movement)

            cursor.execute(
                """
                INSERT OR IGNORE INTO movements
                (name, type_id, action, range, cost, associated_stats, damage, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                movementPrepared
            )

            movement_id = cursor.lastrowid

            
            if len(movement['tag'])>0:
                for tag_id in movement['tag']:
                    cursor.execute("""
                        INSERT OR REPLACE INTO movement_tags (
                            movement_id, tag_id
                        )
                        VALUES (?, ?)
                    """, (movement_id,tag_id))
    elif table == 'items':
        # Preparar datos para executemany
        itemsPrepared = utils.prepare_items_for_db(data_dict)

        cursor.executemany(
            """
            INSERT OR IGNORE INTO items
            (name, type, rarity, cost, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            itemsPrepared
        )
    else:
        # Insertar todos los nombres sin duplicar
        cursor.executemany(
            f"INSERT OR IGNORE INTO {table} (name) VALUES (?)",
            [(name,) for name in data_dict.keys()]
        )

    conn.commit()
    conn.close()

def insertItemType(type):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO item_types (name) VALUES (?)",
        (type,)
    )

    conn.commit()

    type_id = cursor.lastrowid

    # Guardar en el diccionario
    global itemTypesDB
    itemTypesDB[type]= type_id

    conn.close()

def insertItems(items):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Preparar datos para executemany
    itemsPrepared = utils.prepare_items_for_db(items)
    print(itemsPrepared)

    cursor.executemany(
        """
        INSERT OR IGNORE INTO items
        (name, type, rarity, cost, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        itemsPrepared
    )

    conn.commit()

    # Recargar IDs desde la tabla
    cursor.execute("SELECT id, name, type, rarity, cost, description FROM items")
    rows = cursor.fetchall()

    global itemsDB
    for id, name, type, rarity, cost, description in rows:
        itemsDB.append({
            'id': id,
            'name': name,
            'type': type,
            'rarity': rarity,
            'cost': cost,
            'description': description
            })

    conn.close()

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

def insertAbilities(abilities):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Preparar datos para executemany
    abilitiesPrepared = utils.prepare_abilities_for_db(abilities)

    cursor.executemany(
        """
        INSERT OR IGNORE INTO abilities
        (name, description, transformation, legendary)
        VALUES (?, ?, ?, ?)
        """,
        abilitiesPrepared
    )

    conn.commit()

    # Recargar IDs desde la tabla
    cursor.execute("SELECT id, name, description, transformation, legendary FROM abilities")
    rows = cursor.fetchall()

    global abilitiesDB
    for id, name, description, transformation, legendary in rows:
        abilitiesDB[name] = id

        abilitiesDB['dataDB'].append({
            'id': id,
            'name': name,
            'description': description,
            'transformation': transformation,
            'legendary': legendary
            })

    conn.close()

def insertMovements(movements):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Preparar datos para executemany
    for movement in movements:
        movementPrepared = utils.prepare_movements_for_db(movement)

        cursor.execute(
            """
            INSERT OR IGNORE INTO movements
            (name, type_id, action, range, cost, associated_stats, damage, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            movementPrepared
        )

        movement_id = cursor.lastrowid

        
        if len(movement['tag'])>0:
            for tag_id in movement['tag']:
                cursor.execute("""
                    INSERT OR REPLACE INTO movement_tags (
                        movement_id, tag_id
                    )
                    VALUES (?, ?)
                """, (movement_id,tag_id))


    conn.commit()

    # Recargar IDs desde la tabla
    cursor.execute("SELECT id, name, type_id, action, range, cost, associated_stats, damage, description FROM movements")
    rows = cursor.fetchall()

    global movementsDB
    for id, name, type_id, action, range, cost, associated_stats, damage, description in rows:
        movementsDB[name] = id

        cursor.execute("SELECT tag_id, movement_id FROM movement_tags where movement_id=?", (id,))
        tags = []
        rowTags = cursor.fetchall()
        for tag_id,movement_id in rowTags:
            tags.append(tag_id)

        movementsDB['dataDB'].append({
            'id': id,
            'name': name,
            'type': type_id,
            'action': action,
            'range': range,
            'cost': cost,
            'associated_stats': associated_stats,
            'damage': damage,
            'description': description,
            'tag': tags
            })

    conn.close()

def insertSize(size):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sizes (name) VALUES (?)",
        (size,)
    )

    conn.commit()

    size_id = cursor.lastrowid

    # Guardar en el diccionario
    global sizesDB
    sizesDB[size]= size_id

    conn.close()

def insertHabitat(habitat):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO habitats (name) VALUES (?)",
        (habitat,)
    )

    conn.commit()

    habitat_id = cursor.lastrowid

    # Guardar en el diccionario
    global habitatsDB
    habitatsDB[habitat]= habitat_id

    conn.close()

def insertEnvironment(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO environments (name) VALUES (?)",
        (name,)
    )

    conn.commit()

    environment_id = cursor.lastrowid

    # Guardar en el diccionario
    global environmentsDB
    environmentsDB[name]= environment_id

    conn.close()

def insertProficiency(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO proficiencies (name) VALUES (?)",
        (name,)
    )

    conn.commit()

    proficiency_id = cursor.lastrowid

    # Guardar en el diccionario
    global proficienciesDB
    proficienciesDB[name]= proficiency_id

    conn.close()

def insertSense(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO senses (name) VALUES (?)",
        (name,)
    )

    conn.commit()

    sense_id = cursor.lastrowid

    # Guardar en el diccionario
    global sensesDB
    sensesDB[name]= sense_id

    conn.close()

def insertTag(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tags (name) VALUES (?)",
        (name,)
    )

    conn.commit()

    tag_id = cursor.lastrowid

    # Guardar en el diccionario
    global tagsDB
    tagsDB[name]= tag_id

    conn.close()

def insertPokemons(pokemons):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for pokemon in pokemons:
        pokemonPrepared = utils.prepare_pokemon_for_db(pokemon)
        cursor.execute("""
            INSERT OR REPLACE INTO pokemons (
                dex_num, name, size_id, evasion, vitality,
                strength, agility, endurance, mind, spirit, presence,
                min_level, capture_rate, diet, sex
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, pokemonPrepared)

        pokemon_id = cursor.lastrowid

        #types
        for type in pokemon['types']:
            cursor.execute("""
                INSERT OR REPLACE INTO pokemon_types (
                    pokemon_id, type_id
                )
                VALUES (?, ?)
            """, (pokemon_id,type))
        
        # abilities
        if len(pokemon['abilities'])>0:
            for abilityId in pokemon['abilities']:
                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_abilities (
                        pokemon_id, ability_id
                    )
                    VALUES (?, ?)
                """, (pokemon_id,abilityId))

        # hidden abilities
        if len(pokemon['hiddenAbilities'])>0:
            for hiddenAbilityId in pokemon['hiddenAbilities']:
                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_hidden_abilities (
                        pokemon_id, ability_id
                    )
                    VALUES (?, ?)
                """, (pokemon_id,hiddenAbilityId))

        # habitats
        if pokemon['secondaryInfo'].get('habitats'):
            for habitat in pokemon['secondaryInfo']['habitats']:
                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_habitats (
                        pokemon_id, habitat_id
                    )
                    VALUES (?, ?)
                """, (pokemon_id,habitat))

        # environments
        if pokemon.get('velocities'):
            for velocity in pokemon['velocities']:
                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_velocities (
                        pokemon_id, environment_id, quantity
                    )
                    VALUES (?, ?, ?)
                """, (pokemon_id,velocity['id'],velocity['value']))

        # proficiencies
        if pokemon.get('proficiencies'):
            for proficiency in pokemon['proficiencies']:
                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_proficiencies (
                        pokemon_id, proficiency_id
                    )
                    VALUES (?, ?)
                """, (pokemon_id,proficiency))

        # senses
        if pokemon['secondaryInfo'].get('senses'):
            for sense in pokemon['secondaryInfo']['senses']:
                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_senses (
                        pokemon_id, sense_id, quantity
                    )
                    VALUES (?, ?, ?)
                """, (pokemon_id,sense['id'],sense['value']))
        else:
            global sensesDB
            cursor.execute("""
                    INSERT OR REPLACE INTO pokemon_senses (
                        pokemon_id, sense_id
                    )
                    VALUES (?, ?)
                """, (pokemon_id,sensesDB['Ninguno']))

        # movements per level
        if pokemon.get('movesetPerLevel'):
            for moveset in pokemon['movesetPerLevel']:
                for move in moveset['movements']:
                    cursor.execute("""
                        INSERT OR REPLACE INTO moveset_per_level (
                            pokemon_id, movement_id, level
                        )
                        VALUES (?, ?, ?)
                    """, (pokemon_id,move,moveset['level']))
        
        # movements per level
        if pokemon.get('learnset'):
            for move in pokemon['learnset']:
                cursor.execute("""
                    INSERT OR REPLACE INTO learnset (
                        pokemon_id, movement_id
                    )
                    VALUES (?, ?)
                """, (pokemon_id,move))

    conn.commit()

    conn.close()


def getLearnsetMew():
    learnset = []
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("select m.id as 'id', m.name as 'name' from movements m, movement_tags mt, tags t where m.id=mt.movement_id and mt.tag_id=t.id and t.name is not 'Legendario'")
    rows = cursor.fetchall()

    for id,name in rows:
        learnset.append(id)

    conn.commit()
    conn.close()

    return learnset