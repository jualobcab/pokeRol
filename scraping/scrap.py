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

            typesSpan = pkmHeader.findAll("span",class_="type-badge")
            types = []
            for type in typesSpan:
                if type.text != "Variable":
                    types.append(int(dbUtils.typesDB[type.text]))

            
            # stats 1 -> size, proficiencies, evasion, vitality, velocities[]
            pkmUnifiedStats = info.select_one(".unified-stats-section")

            pkmSizeProficiencies = pkmUnifiedStats.select_one(".pokemon-size").text.split(", ")

            size = utils.parse_size(pkmSizeProficiencies[0].split(" ")[1])

            #TODO: arceus -> Todas las habilidades
            proficiencies = []
            if len(pkmSizeProficiencies) == 2:
                proficiencies = utils.parse_proficiencies(pkmSizeProficiencies[1])

            pkmEvasionVitality = pkmUnifiedStats.findAll("div",class_="vital-stat-row")
            evasion = pkmEvasionVitality[0].select_one(".vital-stat-value").text
            vitality = pkmEvasionVitality[1].select_one(".vital-stat-value").text

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

            #TODO: habilidades

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
                "secondaryInfo":secondaryInfo
            }
            print(pokemon)

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

        results.append(typeName)

    return results


'''
def sacarDatos(url,urlBase):
    respuesta = {}

    this_session = HTMLSession()
    response = this_session.get(url)
    response.html.render()

    soup = BeautifulSoup(response.html.raw_html, "html.parser")

    # tipo de barco
    tipoBarco = soup.find_all("a", class_="active nav-link")[0].text
    respuesta["clase"] = tipoBarco

    respuesta["barcos"] = []

    divBody = soup.find_all("div", class_="card-body")
    divContenedor = divBody[0].find_all("div", class_="tab-pane active")
    divsBarcos = divContenedor[0].findChildren("div",recursive=False)

    # el primero es el filtro por tipos especiales
    divsBarcos.pop(0)

    for divsBarcosTier in divsBarcos:
        # Comprobar que no este vacio
        # tier
        tier = ""
        try:
            tier = divsBarcosTier.find("h3",class_="title").text.split(" ")[1]
        except:
            continue
        
        divsBarcos = divsBarcosTier.findChildren("div",recursive=False)[0].findChildren("div",recursive=False)
        for divBarco in divsBarcos:
            barco = {}

            # nombre
            nombre = divBarco.find("p").text

            print("-----------------------")
            print("Barco: "+nombre)

            # badges
            divBadges = divBarco.findChildren("div",recursive=False)[0]
            imgBadges = divBadges.find_all("img")
            badges = []
            if len(imgBadges)>0:
                for imgBadge in imgBadges:
                    badge = []
                    badge.append(imgBadge["src"])
                    badge.append(imgBadge["data-tip"])

                    badges.append(badge)

            # imagen barco
            imagenTag = divBarco.find("div",class_="img-raised").find("img")
            imagen = imagenTag["src"]
            imagenNombre = imagen.split("/")[-1]
            download_image(urlBase+urllib.parse.quote(imagen),imagenNombre)

            # rareza
            rareza = imagenTag.get_attribute_list('class')[-1]

            barco["nombre"] = nombre
            barco["tier"] = tier
            barco["imagen"] = imagenNombre
            barco["rareza"] = rareza
            barco["badges"] = badges

            respuesta["barcos"].append(barco)
            
    # print(json.dumps(respuesta))
    return respuesta

def download_image(url, file_name):
    full_path = "web/static/datos/img/" + file_name
    urllib.request.urlretrieve(url, full_path)

'''