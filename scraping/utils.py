import dbUtils
import json
import os
import re

################################################
## scraping
################################################
def parse_velocities(text):
    result = []

    # Separar elementos por coma
    items = text.split(", ")

    for item in items:
        item = item.strip()

        # Separar nombre y valor
        if ":" in item:
            firstSplit = item.split(": ", 1)
            
            if " " in firstSplit[1]:
                parts = firstSplit[1].strip().split(" ", 1)
                if len(parts) == 2:
                    name, value = parts
            else:
                name, value = item.split(":", 1)
        else:
            parts = item.split(" ", 1)
            if len(parts) == 2:
                name, value = parts
            else:
                continue  # si no tiene formato válido, se ignora

        name = name.strip()
        value = value.strip()
        
        # Cambiar "Velocidad" → "normal"
        if name.lower() == "velocidad":
            name = "Normal"

        # Quitar la "m" final del valor
        if value.endswith("m"):
            value = value[:-1].strip()

        if name not in dbUtils.environmentsDB:
            dbUtils.insertEnvironment(name)
    
        nameID = dbUtils.environmentsDB[name]

        result.append({
            "id": nameID,
            "value": int(value)
        })

    return result

def parse_size(size):
    if size not in dbUtils.sizesDB:
        dbUtils.insertSize(size)
    
    return dbUtils.sizesDB[size]

def parse_proficiencies(proficienciesText):
    proficiencies = []

    for p in proficienciesText.split("en ", 1)[1].split(" y "):
        p = clean_string(p)

        if p not in dbUtils.proficienciesDB:
            dbUtils.insertProficiency(p)
        
        proficiencies.append(dbUtils.proficienciesDB[p])

    return proficiencies

def parse_stat(name,value):
    match name:
        case "FUE":
            name = "strength"
        case "AGI":
            name = "agility"
        case "RES":
            name = "endurance"
        case "MEN":
            name = "mind"
        case "ESP":
            name = "spirit"
        case "PRE":
            name = "presence"
        case _:
            name = name  # por defecto

    return name,value

def parse_secondaryInfo(name,value):
    match name:
        case "Nivel mínimo":
            name = "min_level"
        case "Ratio de Captura":
            name = "capture_rate"
        case "Dieta":
            name = "diet"
        case "Sexo":
            name = "sex"
        case "Hábitat":
            name = "habitats"
            value = parse_habitats(value.split(", "))
        case "Sentidos":
            name = "senses"
            value = parse_sense(value)

    return name,value

def parse_habitats(habitats):
    habitatsClean = []

    for habitat in habitats:
        habitat = clean_string(habitat)

        if habitat == "" or habitat == "???":
            habitat = "Desconocido"

        if habitat not in dbUtils.habitatsDB:
            dbUtils.insertHabitat(habitat)

        habitatsClean.append(dbUtils.habitatsDB[habitat])

    return habitatsClean

def parse_sense(value):
    senses = []

    value = clean_string(value)

    sensesSplit = value.split(", ")

    if sensesSplit[0] == "Ninguno":
        senseName = "Ninguno"

        if senseName not in dbUtils.sensesDB:
            dbUtils.insertSense(senseName)
    
        nameID = dbUtils.sensesDB[senseName]

        senses.append({
                "id": nameID,
                "value": None
            })
    elif "(" not in sensesSplit[0]:
        senseName = sensesSplit[0].strip()

        if senseName != "":
            if senseName not in dbUtils.sensesDB:
                dbUtils.insertSense(senseName)
        
            nameID = dbUtils.sensesDB[senseName]
            senses.append({
                    "id": nameID,
                    "value": None
                })
    else:
        for sense in sensesSplit:
            if sense != "":
                if "cetitan" in sense:
                    senseName = "Percibir otros Cetitan"
                    senseValue = "4 km"
                else:
                    dataSplit = sense.split(" (")
                    senseName = clean_string(dataSplit[0])
                    
                    if "Electrorecepción" in senseName:
                        senseName = "Electrorrecepción"

                    if " m)" in sense:
                        senseValue = dataSplit[1].replace(")","")
                    else:
                        senseValue = dataSplit[1]

                if senseName not in dbUtils.sensesDB:
                    dbUtils.insertSense(senseName)
            
                nameID = dbUtils.sensesDB[senseName]

                senses.append({
                    "id": nameID,
                    "value": senseValue
                })

    return senses

################################################
## DB
################################################
def prepare_pokemon_for_db(pokemon):
    return (
        int(pokemon["number"]),
        pokemon["name"],
        pokemon["size"],
        pokemon["evasion"].strip(),
        pokemon["vitality"],
        pokemon["stats"]["strength"],
        pokemon["stats"]["agility"],
        pokemon["stats"]["endurance"],
        pokemon["stats"]["mind"],
        pokemon["stats"]["spirit"],
        pokemon["stats"]["presence"],
        int(pokemon["secondaryInfo"]["min_level"]),
        int(pokemon["secondaryInfo"]["capture_rate"]),
        pokemon["secondaryInfo"]["diet"],
        pokemon["secondaryInfo"]["sex"],
    )

################################################
## others
################################################
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[OK] Guardado {filename}")


def load_json(filename):
    if not os.path.exists(filename):
        print(f"[INFO] No existe {filename}, se omite.")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_string(text):
    if not text:
        return ""

    # Quitar espacios raros: \xa0, \t, \n, etc.
    text = text.replace("\xa0", " ")

    # Quitar espacios duplicados
    text = re.sub(r"\s+", " ", text)

    # Quitar espacios al inicio y al final
    text = text.strip()

    # Quitar puntos
    text = text.replace(".", "")

    # Convertir todo a minúsculas
    text = text.lower()

    # Primera letra en mayúsculas
    text = text.capitalize()

    return text