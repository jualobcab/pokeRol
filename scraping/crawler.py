import scrap
import dbUtils
import createDB

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
print("inserting pokemon")
dbUtils.insertPokemons(pokemons)
print("==============================================")