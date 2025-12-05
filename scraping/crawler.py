import scrap
import dbUtils
import createDB

urlBase = "https://pokemonrpa.net/"
urlPokedex = "pokedex"
urlTypes = "tablatipos"

'''
print("scraping types")
types = scrap.scrap_tipos(urlBase, urlTypes)
print("inserting types")
dbUtils.insertTypes(types)
'''
'''
for type in types:
    print(type)
'''


pokemons = scrap.scrap_pokedex(urlBase, urlPokedex)
