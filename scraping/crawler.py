import scrap
import dbUtils
import createDB
import utils

modoJSON = True

urlBase = "https://pokemonrpa.net/"
urlPokedex = "pokedex"
urlTypes = "tablatipos"
urlAbilities = "habilidades"

createDB.initialice()

if not modoJSON:
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

    print("scraping pokemon")
    pokemons = scrap.scrap_pokedex(urlBase, urlPokedex)

    # Guardar en JSON
    utils.save_json("./json/pokemons.json",pokemons)
    dbUtils.save_all_db_dicts()
else:
    # cargar de los json
    pokemons = utils.load_json("./json/pokemons.json")
    dbUtils.load_all_db_dicts()

print("inserting pokemon")
dbUtils.insertPokemons(pokemons)
print("==============================================")
