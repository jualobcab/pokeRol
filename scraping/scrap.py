from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import utils
import dbUtils
import time

def scrap_pokedex(urlBase, urlPokedex):
    url = urlBase + urlPokedex
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Ir a la página
        page.goto(url)

        # Esperar a que se carguen los elementos del pokedex
        page.wait_for_selector(".pokemon-card")

        # Contamos cuántas tarjetas hay
        count = page.locator(".pokemon-card").count()

        for i in range(count):
            # Seleccionar la tarjeta POR ÍNDICE (siempre válida)
            card = page.locator(".pokemon-card").nth(i)
            # Hacemos click en la tarjeta
            card.click()

            time.sleep(0.1)

            # Esperar a que cargue el div con los datos (ajusta el selector)
            page.wait_for_selector(".details-section .pokemon-details")
            page.wait_for_selector(".abilities-container")

            # Obtener el HTML ahora que está cargado el panel
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Datos dentro del panel
            info = soup.select_one(".details-section .pokemon-details")

            # cabecera -> numero, nombre, tipos[]
            pkmHeader = info.select_one(".pokemon-title")

            nameNumber = pkmHeader.select_one("h2").text.split(" ",1)

            pkmNumber = nameNumber[0].replace("#", "")
            pkmName = nameNumber[1]

            print(pkmNumber+" "+pkmName)

            typesSpan = pkmHeader.findAll("span",class_="type-badge")
            types = []
            for type in typesSpan:
                if type.text != "Variable":
                    types.append(int(dbUtils.typesDB[type.text]))

            
            # stats 1 -> size, proficiencies, evasion, vitality, velocities[]
            pkmUnifiedStats = info.select_one(".unified-stats-section")

            pkmSizeProficiencies = pkmUnifiedStats.select_one(".pokemon-size").text.split(", ")

            size = utils.parse_size(pkmSizeProficiencies[0].split(" ")[1])

            proficiencies = []
            if len(pkmSizeProficiencies) == 2:
                proficiencies = utils.parse_proficiencies(pkmSizeProficiencies[1])

            pkmEvasionVitality = pkmUnifiedStats.findAll("div",class_="vital-stat-row")
            evasion = pkmEvasionVitality[0].select_one(".vital-stat-value").text.strip().replace("  "," ")
            vitality = pkmEvasionVitality[1].select_one(".vital-stat-value").text.strip()

            pkmVelocities = pkmUnifiedStats.select_one(".speeds-inline").text
            velocities = utils.parse_velocities(pkmVelocities)

            # stats 2 -> fue,agi,res,men,esp,pre
            pkmUnifiedStats = info.select_one(".stats-section")
            pkmStats = pkmUnifiedStats.findAll("tr")

            stats = {}
            for stat in pkmStats:
                pkmRow = stat.findAll("td")
                pkmStatName = pkmRow[0].text
                pkmStatValue = pkmRow[1].text

                statName,statValue = utils.parse_stat(pkmStatName,pkmStatValue)

                stats[statName] = statValue

            # abilities
            abilities = []
            hiddenAbilities = []
            pkmAbilities = info.select_one(".abilities-section .abilities-container").findAll("div",class_="ability-item")
            for pkmAbility in pkmAbilities:
                abilityName = pkmAbility.select_one(".ability-name").text.strip()
                abilityId = dbUtils.abilitiesDB[abilityName]

                if pkmAbility.select_one(".hidden-label") is not None:
                    hiddenAbilities.append(abilityId)
                else:
                    abilities.append(abilityId)

            #TODO: linea evolutiva

            # informacion secundaria
            pkmSecondaryInfo = info.select_one(".detail-section.otros .otros-table")
            pkmSecondaryInfoNames = pkmSecondaryInfo.findAll("span",class_="th")
            pkmSecondaryInfoValues = pkmSecondaryInfo.findAll("span",class_="td")

            secondaryInfo = {}
            for name, value in zip(pkmSecondaryInfoNames, pkmSecondaryInfoValues):
                siName,siValue =utils.parse_secondaryInfo(name.text, value.text)
                secondaryInfo[siName] = siValue


            #TODO: movimientos


            pokemon = {
                "number": pkmNumber,
                "name": pkmName,
                "types": types,
                "size": size,
                "proficiencies": proficiencies,
                "evasion": evasion,
                "vitality": vitality,
                "velocities": velocities,
                "stats":stats,
                "abilities":abilities,
                "hiddenAbilities":hiddenAbilities,
                "secondaryInfo":secondaryInfo
            }

            results.append(pokemon)

        # Obtener HTML renderizado
        html = page.content()
        browser.close()

    return results

def scrap_tipos(urlBase, urlTipos):
    url = urlBase + urlTipos
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Ir a la página
        page.goto(url)

        # Esperar a que se carguen los elementos del pokedex
        page.wait_for_selector("#tablaTipos")

        # Obtener HTML renderizado
        html = page.content()
        browser.close()

    # Parsear HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    types = soup.find_all("td", class_="tipo-nombre")

    for type in types:
        typeName = type.find("div").text.replace(" ", "")

        print(typeName)

        results.append(typeName)

    return results

def scrap_abilities(urlBase, urlAbilities):
    url = urlBase + urlAbilities
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Ir a la página
        page.goto(url)

        # Esperar a que se carguen las filas
        page.wait_for_selector(".div-tabla table tbody tr")
        time.sleep(1)

        # Obtener filas clicables desde Playwright
        row_elements = page.query_selector_all(".div-tabla table tbody tr")

        # Obtener HTML inicial para BS4
        html = page.content()

        # Parseo inicial
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one(".div-tabla table tbody")
        abilities = table.find_all("tr")

        # Recorremos filas por índice
        for i, ability in enumerate(abilities):
            # Hacer click en la fila real del navegador
            row_elements[i].click()
            time.sleep(0.3)

            # Esperar panel con los datos cargados
            page.wait_for_selector(".seleccionado")

            # HTML actualizado después del click
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Descripción
            abilityDescription = soup.select_one("div.descripcion p").text.strip()

            # Datos de la fila original
            abilityData = ability.find_all("td")
            abilityName = abilityData[0].text.strip()
            abilityLegendary = abilityData[1].text.strip() == "✔"
            abilityTransformation = abilityData[2].text.strip() == "✔"

            print(abilityName)

            # Añadir resultado
            results.append({
                'name': abilityName,
                'legendary': abilityLegendary,
                'transformation': abilityTransformation,
                'description': abilityDescription
            })

        browser.close()

    return results
