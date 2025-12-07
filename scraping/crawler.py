import scrap
import dbUtils
import createDB
import utils

urlBase = "https://pokemonrpa.net/"
urlPokedex = "pokedex"
urlTypes = "tablatipos"

createDB.initialice()

print("scraping types")
types = scrap.scrap_tipos(urlBase, urlTypes)
print("inserting types")
dbUtils.insertTypes(types)
print("==============================================")

'''
for type in types:
    print(type)
'''

print("scraping pokemon")
pokemons = scrap.scrap_pokedex(urlBase, urlPokedex)

# Guardar en JSON
utils.save_json("./json/pokemons.json",pokemons)
dbUtils.save_all_db_dicts()

# cargar de los json
pokemons = utils.load_json("./json/pokemons.json")
dbUtils.load_all_db_dicts()

print("inserting pokemon")
dbUtils.insertPokemons(pokemons)
print("==============================================")