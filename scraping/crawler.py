import scrap
import dbUtils
import createDB
import utils

modeJSON = False
modeDevelop = True

urlBase = "https://pokemonrpa.net/"
urlPokedex = "pokedex"
urlTypes = "tablatipos"
urlAbilities = "habilidades"
urlMovements = "movimientos"

jsonItems = './json/items.json'

createDB.initialice()

if modeDevelop:
    dbUtils.load_all_db_dicts()

    print("scraping pokemon")
    pokemons = scrap.scrap_pokedex(urlBase, urlPokedex)
    utils.save_json("./json/pokemons.json",pokemons)
    print("inserting pokemon")
    dbUtils.insertPokemons(pokemons)
    print("==============================================")

elif not modeJSON:
    print("scraping types")
    types = scrap.scrap_tipos(urlBase, urlTypes)
    print("inserting types")
    dbUtils.insertTypes(types)
    print("==============================================")

    print("scraping abilities")
    abilities = scrap.scrap_abilities(urlBase, urlAbilities)
    print("inserting abilities")
    dbUtils.insertAbilities(abilities)
    print("==============================================")

    print("scraping movements")
    movements = scrap.scrap_movements(urlBase, urlMovements)
    print("inserting movements")
    dbUtils.insertMovements(movements)
    print("==============================================")

    print("scraping items")
    items = scrap.scrap_items(jsonItems)
    print("inserting items")
    dbUtils.insertItems(items)
    print("==============================================")

    print("scraping pokemon")
    pokemons = scrap.scrap_pokedex(urlBase, urlPokedex)

    # Guardar en JSON
    utils.save_json("./json/pokemons.json",pokemons)
    dbUtils.save_all_db_dicts()
else:
    # cargar de los json
    pokemons = utils.load_json("./json/pokemons.json")
    dbUtils.load_all_db_dicts()

'''
print("inserting pokemon")
dbUtils.insertPokemons(pokemons)
print("==============================================")
'''
