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
            if value == 116:
                value = 16
        case "Ratio de Captura":
            name = "capture_rate"
        case "Dieta":
            name = "diet"
            value = clean_diet(value)
        case "Sexo":
            name = "sex"
            value = clean_sex(value)
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

        match habitat:
            case "" | "???":
                habitat = "Desconocido"

            case "Río":
                habitat = "Ríos"
            
            case "Ruina":
                habitat = "Ruinas"
            
            case "Playa arenosa":
                habitat = "Playa"
            
            case "Lugar malidto":
                habitat = "Lugar maldito"
            
            case "Espacio":
                habitat = "Espacio exterior"
            
            case "Cueva":
                habitat = "Cuevas"
            
            case "Cualquier":
                habitat = "Cualquiera"
            
            case "Bosque":
                habitat = "Bosques"
        
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

def parse_tag(tag):
    tags = []

    tagsSplit = tag.split(", ")
    for t in tagsSplit:
        t = clean_string(t)
        match t:
            case '':
                t= '—'
            case 'Golpea múltiples veces':
                t= 'Golpea varias veces'
            case 'Golpea dos veces':
                t= 'Golpea 2 veces'
            case 'Golpea tres veces':
                t= 'Golpea 3 veces'
            case 'Res':
                t= '—'
            case 'Lengendario':
                t= 'Legendario'

        if not t == '—':
            if t not in dbUtils.tagsDB:
                dbUtils.insertTag(t)
            
            tags.append(dbUtils.tagsDB[t])

    return tags 

def addTag(tags,tag):
    tag = clean_string(tag)

    if tag not in dbUtils.tagsDB:
        dbUtils.insertTag(tag)
    
    tags.append(dbUtils.tagsDB[tag])

    return tags 

def parse_movements_pokemon(movements):
    res = []

    for move in movements:
        res.append(dbUtils.movementsDB[move])

    return res

def parse_movements_pokemon_mew():
    return dbUtils.getLearnsetMew()

def clean_damage(damage):
    damage = damage.replace("  "," ")

    if '8+' in damage:
        damage = damage.replace("8+","8 +")

    if damage == 'Descripción':
        damage = None

    return damage

def clean_cost(cost):
    cost = cost.strip().replace("  "," ")
    match cost:
        case 'A Voluntad':
            cost = 'A voluntad'

    return cost

def clean_sex(sex):
    match sex:
        case 'F':
            sex = 'H'
        case 'F/M':
            sex = 'M/H'
        case 'H/M':
            sex = 'M/H'
        case '':
            sex = '???'

    return sex

def clean_diet(diet):
    match diet:
        case 'Electr.':
            diet = 'Electricidad'
        case 'Hervívoro':
            diet = 'Herbívoro'
        case 'Hervíboro':
            diet = 'Herbívoro'
        case 'Carnivoro':
            diet = 'Carnívoro'
        case 'Omnivoro':
            diet = 'Omnívoro'
        case 'Mineral':
            diet = 'Minerales'
        case '':
            diet = '???'
        case 'Luz solar, herbívoro':
            diet = 'Luz solar, Herbívoro'

    return diet

def clean_type(type):
    match type:
        case 'Dragon':
            type = 'Dragón'


    return type

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

def prepare_abilities_for_db(abilities):
    return [
        (
            a["name"],
            a["description"],
            int(a["transformation"]),  # BOOLEAN → 0/1
            int(a["legendary"])        # BOOLEAN → 0/1
        )
        for a in abilities
    ]

def prepare_movements_for_db(movement):
    return (
            movement["name"],
            int(movement["type"]),
            movement["action"],
            movement["range"],
            movement["cost"],
            movement["associated_stats"],
            movement["damage"],
            movement["description"]
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