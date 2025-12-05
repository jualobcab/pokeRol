from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

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

        # Extraemos todas las tarjetas
        cards = page.query_selector_all(".pokemon-card")

        for card in cards:
            # Hacemos click en la tarjeta
            card.click()

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

            number = nameNumber[0].replace("#", "")
            name = nameNumber[1]

            typesSpan = pkmHeader.findAll("span",class_="type-badge")
            types = []
            for type in typesSpan:
                types.append(type.text)

            
            # stats 1 -> size, proficiencies, evasion, vitality, velocities[]
            pkmUnifiedStats = info.select_one(".unified-stats-section")

            pkmSizeProficiencies = pkmUnifiedStats.select_one(".pokemon-size").text.split(", ")

            size = pkmSizeProficiencies[0].split(" ")[1]

            proficiencies = []
            if len(pkmSizeProficiencies) == 2:
                proficiencies = [
                    p.strip()
                    for p in pkmSizeProficiencies[1].split("en ", 1)[1].split(" y ")
                ]

            # 0 -> evasion
            # 1 -> vitality
            pkmEvasionVitality = pkmUnifiedStats.findAll("div",class_="vital-stat-row")
            evasion = pkmEvasionVitality[0].select_one(".vital-stat-value").text
            vitality = pkmEvasionVitality[1].select_one(".vital-stat-value").text

            pkmVelocity = pkmUnifiedStats.select_one(".speeds-inline").text
            #TODO: esto hay que hacer un array y quitar los metros (m)

            print(number," - ",name," - ",types," - ",size," - ",
                  proficiencies," - ",evasion," - ",vitality," - ",pkmVelocity)

            results.append({
                "number": number,
                "name": name,
                "types": types,
                "size": size,
                "proficiencies": proficiencies,
            })

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