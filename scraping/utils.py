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
            name = "normal"

        # Quitar la "m" final del valor
        if value.endswith("m"):
            value = value[:-1].strip()
        result.append({
            "name": name,
            "value": int(value)
        })

    return result

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
            name = "habitat"
            value = value.split(", ")
        case "Sentidos":
            name = "senses"
            value = parse_sense(value)

    return name,value

def parse_sense(value):
    #TODO: 381 ['Visión en la oscuridad (100 m)', 'Ecolocalización (Todo el océano)']
    senses = []

    sensesSplit = value.split(", ")

    if sensesSplit[0] == "Ninguno":
        senses.append({
                "name": "Ninguno",
                "value": ""
            })
    elif "(" not in sensesSplit[0]:
        senses.append({
                "name": sensesSplit[0],
                "value": ""
            })
    else :
        print(sensesSplit)
        for sense in sensesSplit:
            if sense != "":
                if "." in sense:
                    sense = sense.replace(".","")
                dataSplit = sense.split(" (")
                senseName = dataSplit[0] 
                senseValue = int(dataSplit[1].replace(" m)",""))

                senses.append({
                    "name": senseName,
                    "value": senseValue
                })

    return senses

################################################
## DB
################################################
def prepare_pokemon_for_db(pokemon):
    return (
        int(pokemon["number"]),
        pokemon["name"],                 # size_id
        pokemon["evasion"].strip(),
        int(pokemon["vitality"]),
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

