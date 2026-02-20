'''
=======================================================================================
Testovaci skript pro endpoint DELETE/barrels/{barrelId}
https://to-barrel-monitor.azurewebsites.net/barrels/{barrelId}
=======================================================================================
Skript nacita vstupni url ze souboru "config.json, vstupni data ze souboru "PostBarrelsData.json"
a pouziva custom knihovnu "common.py"
=> soubory musi byt ve stejnem repozitari jako script.
Pokud test projde, program vypise posledni odpoved preveditelnou na json do souboru log.txt
Pokud test neprojde, prislusna assert funkce ukonci program, vypise chybovou hlasku a 
posledni odpoved preveditelna na json bude vypsana do souboru "log.txt" 
=======================================================================================
Ucel testu: Zjistit, zda endpoint DELETE/barrels/{barrelId} vraci data spravne a ve spravnem formatu
=======================================================================================
Scenar:
=======
1) Nacteni url ze souboru
2) Provolani endpointu POST/barrels/
3) Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
   a prevedeni na json
4) Delete zaznamu
5) Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
6) Volani GET pro smazany barrel
7) Overeni zda byl barrel skutecne smazan
=======================================================================================
Ocekavany vysledek: skript projde 
Realny vysledek: Skript spadne na interni serverovou chybu v kroku 4
=======================================================================================
Komentar: Delete nefunguje spravne
'''
#import knihoven
import requests
import common

#nacteni testovacich dat ze souboru (krok 1)
barrels = common.load_data("PostBarrelsData.json")
connects = common.load_data("config.json")
url = connects["urlBarrels"]
header = connects["header"]

#vytvoreni barrelu (krok 2)
response = requests.post(url, json=barrels["inputsValid"][0], headers=header, timeout=3)

#test, zda je status odpovedi validni a prevedeni odpovedi na json (krok 3)
common.is_format_valid(response, 201)
responseJson = response.json()

#delete zaznamu (krok 4)
delete = requests.delete(url + f"/{responseJson["id"]}")

#overeni zda delete zaznamu probehl spravne (krok 5)
common.verify_status(delete, 204)

#volani GET pro konkretni barrel pro overeni ze barrel byl skutecne smazan (krok 6)
urlGetBarrel = url + f"/{responseJson["id"]}"
barrelGetResponse = requests.get(urlGetBarrel, timeout=3)

#overeni odpovedi pro GET (krok 7)
common.verify_status_negative(barrelGetResponse, 200)