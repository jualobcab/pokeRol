import utils
import json

urlBase = "https://pokemonrpa.net/"

'''
url = "https://slaimuda.github.io/ectl/#/main/"
pages = ["bb","cv","ca","cl","dd","ss","other"]
pagesTam = len(pages)

jsonDatos = {}
jsonDatos["AzurLane"] = []

# hacer function
for index,page in enumerate(pages):
    print("=======================================")
    print("Analizando {} {}/{}".format(page,index+1,pagesTam))
    jsonDatos["AzurLane"].append(utils.sacarDatos(url + page,urlBase))

print(json.dumps(jsonDatos))
with open("web/static/datos/datos.json", "w") as write_file:
    json.dump(jsonDatos, write_file, indent=4, sort_keys=True)

'''